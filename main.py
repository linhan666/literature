import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog
import sqlite3
import fitz
import os
import shutil
import json
from datetime import datetime
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

try:
    from pypinyin import lazy_pinyin
except ImportError:
    lazy_pinyin = None

# ============ 配置 ============
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "literature.db")
PDF_STORAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdfs")

# LLM配置 - DeepSeek API
LLM_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
LLM_BASE_URL = "https://api.deepseek.com/v1"

# 可用模型
AVAILABLE_MODELS = {
    "deepseek-v4-pro": "deepseek-v4-pro",
    "deepseek-v4-flash": "deepseek-v4-flash"
}
LLM_MODEL = os.environ.get("LLM_MODEL", "deepseek-v4-pro")

os.makedirs(PDF_STORAGE, exist_ok=True)

# 预设分类
DEFAULT_CATEGORIES = [
    "药物筛选", "结构生物学", "分子生成", "分子（化学）语言模型",
    "蛋白语言模型", "分子属性预测", "蛋白属性预测", "蛋白质设计", "蛋白结构设计",
    "其他"
]

# ============ 数据库 ============
def get_db_conn():
    """获取数据库连接，启用WAL模式防止锁定"""
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA busy_timeout=5000')
    return conn

def init_db():
    conn = get_db_conn()
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS papers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        authors TEXT,
        abstract TEXT,
        keywords TEXT,
        doi TEXT,
        year TEXT,
        file_path TEXT NOT NULL,
        page_count INTEGER,
        added_date TEXT,
        tags TEXT DEFAULT '',
        category TEXT DEFAULT '',
        methods TEXT DEFAULT '',
        innovations TEXT DEFAULT ''
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )''')
    
    # 初始化预设分类
    for cat in DEFAULT_CATEGORIES:
        c.execute('INSERT OR IGNORE INTO categories (name) VALUES (?)', (cat,))
    
    conn.commit()
    conn.close()

def get_categories():
    conn = get_db_conn()
    c = conn.cursor()
    c.execute('SELECT name FROM categories ORDER BY name')
    cats = [row[0] for row in c.fetchall()]
    conn.close()
    return cats

def add_category(name):
    conn = get_db_conn()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO categories (name) VALUES (?)', (name,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def delete_category(name):
    conn = get_db_conn()
    c = conn.cursor()
    c.execute('DELETE FROM categories WHERE name=?', (name,))
    c.execute("UPDATE papers SET category='' WHERE category=?", (name,))
    conn.commit()
    conn.close()

# ============ PDF解析 ============
def extract_text_from_pdf(pdf_path, max_pages=5):
    """提取PDF文本，优先前5页找摘要"""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for i in range(min(max_pages, len(doc))):
            page = doc.load_page(i)
            text += page.get_text() + "\n"
        doc.close()
        return text
    except Exception as e:
        return f"解析失败: {str(e)}"

def extract_abstract(text):
    """从文本中提取摘要 - 增强版"""
    # 清理文本：移除页眉页脚、页码等
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        # 跳过纯数字行（页码）
        if line.isdigit():
            continue
        # 跳过短行（可能是页眉）
        if len(line) < 5 and line.isupper():
            continue
        cleaned_lines.append(line)
    cleaned_text = '\n'.join(cleaned_lines)
    
    # 常见摘要标记模式（增强）
    patterns = [
        # 标准 Abstract + Introduction 模式
        r'(?i)abstract[\s:]*\n(.*?)(?=\n\s*(?:introduction|1\s+introduction|background|i\s+introduction|methods|materials))',
        # Abstract 后跟大段文字
        r'(?i)abstract[\s:]*(.{100,8000}?)(?=\n\s*(?:introduction|background|methods|keywords|key\s+words))',
        # 中文摘要
        r'(?i)摘要[\s:]*\n(.*?)(?=\n\s*(?:关键词|引言|1\s|背景|方法))',
        # Abstract 带横线
        r'(?i)abstract\s*[-–—]\s*(.{100,8000}?)(?=\n\s*\d+\s|\n\s*introduction|\n\s*keywords)',
        # 无Abstract标记，找第一段长文本（假设是摘要）
        r'(?i)(^.{100,3000}?)\n\s*(?=introduction|background|1\s|methods)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, cleaned_text, re.DOTALL)
        if match:
            abstract = match.group(1).strip()
            # 清理
            abstract = re.sub(r'\n+', ' ', abstract)
            abstract = re.sub(r'\s+', ' ', abstract)
            # 移除可能的页眉残留
            abstract = re.sub(r'(?i)\b(journal|vol\.|no\.|pp\.|doi|copyright)\b[^.]*\.?', '', abstract)
            abstract = abstract.strip()
            if len(abstract) > 50:  # 确保摘要有意义的长度
                return abstract[:5000]
    
    # 如果没找到，尝试从文本前部提取长段落
    paragraphs = [p.strip() for p in cleaned_text.split('\n\n') if len(p.strip()) > 100]
    if paragraphs:
        # 返回第一个长段落（通常是摘要）
        fallback = paragraphs[0].replace('\n', ' ')
        return fallback[:2000]
    
    # 最终兜底
    fallback = cleaned_text[:1500].replace('\n', ' ')
    return fallback

def extract_keywords(text):
    """提取关键词"""
    patterns = [
        r'(?i)keywords?[\s:]*(.{0,500}?)(?=\n|$)',
        r'(?i)key words?[\s:]*(.{0,500}?)(?=\n|$)',
        r'(?i)关键词[\s:]*(.{0,500}?)(?=\n|$)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            kw = match.group(1).strip()
            kw = re.sub(r'[;；,，]', ', ', kw)
            return kw[:500]
    return ""

def extract_title_from_text(text):
    """从文本开头提取标题 - 增强版"""
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # 跳过模式：期刊名、页眉页脚、短行
    skip_patterns = [
        'journal', 'vol.', 'pp.', 'doi', 'http', '@', 
        'university', 'institute', 'department', 'correspond',
        'received', 'accepted', 'published', 'copyright',
        'figure', 'table', 'supplementary', 'appendix',
        'page', 'www.', 'email', 'tel:', 'fax:'
    ]
    
    candidates = []
    for i, line in enumerate(lines[:15]):
        # 跳过过短行
        if len(line) < 15:
            continue
        # 跳过包含跳过关键词的行
        if any(x in line.lower() for x in skip_patterns):
            continue
        # 跳过全大写（通常是期刊名或页眉）
        if line.isupper() and len(line) > 30:
            continue
        # 跳过纯数字
        if line.replace(' ', '').isdigit():
            continue
        # 跳过包含过多数字的行（可能是页眉页脚）
        if sum(c.isdigit() for c in line) / len(line) > 0.3:
            continue
        
        # 计算得分：长度适中、有实词、首字母大写
        score = 0
        if 30 <= len(line) <= 200:  # 标题通常在这个范围
            score += 10
        if len(line) > 20:
            score += 5
        # 有多个大写单词（可能是专有名词）
        words = line.split()
        capitalized = sum(1 for w in words if w and w[0].isupper())
        if capitalized >= 2:
            score += 5
        # 不包含常见标点（标题通常没有句末标点）
        if not line[-1] in '.,;:!?':
            score += 3
        # 位置靠前加分
        score += max(0, 5 - i)
        
        candidates.append((score, line))
    
    if candidates:
        candidates.sort(reverse=True)
        return candidates[0][1]
    
    # 兜底：返回第一个非空长行
    for line in lines[:10]:
        if len(line) > 20:
            return line
    return ""

# ============ LLM分析 ============
def call_llm(system_prompt, user_prompt, max_tokens=2000):
    """调用LLM API"""
    if not LLM_API_KEY:
        return None, "未设置API Key"
    
    try:
        import urllib.request
        import urllib.error
        
        data = {
            "model": LLM_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.3
        }
        
        req = urllib.request.Request(
            f"{LLM_BASE_URL}/chat/completions",
            data=json.dumps(data).encode('utf-8'),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {LLM_API_KEY}"
            },
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            return result['choices'][0]['message']['content'], None
            
    except Exception as e:
        return None, str(e)

def analyze_paper(title, abstract, keywords, categories):
    """用LLM分析论文主题、方法、创新点和分类"""
    categories_str = "\n".join([f"- {c}" for c in categories])
    
    system_prompt = """你是一个专业的AIDD（AI驱动药物发现）领域文献分析专家。
请严格按JSON格式输出，不要包含任何其他文字。"""

    user_prompt = f"""请分析以下论文，提取关键信息：

标题: {title}
摘要: {abstract[:3000]}
关键词: {keywords}

可用分类：
{categories_str}

请输出JSON格式：
{{
    "category": "最匹配的分类名称，必须从上面的列表中选择",
    "recommended_category": "如果以上分类都不合适，推荐一个更准确的分类名称；如果合适则留空",
    "methods": "主要研究方法，用2-3句话概括",
    "innovations": "核心创新点，用2-3句话概括",
    "keywords_enhanced": "从摘要中提取的额外关键词，逗号分隔"
}}

注意：
1. category必须从给定列表中选择，不要自创分类
2. 如果给定分类都不合适，category填"其他"，并在recommended_category中推荐新分类
3. 只输出JSON，不要markdown代码块"""

    content, error = call_llm(system_prompt, user_prompt, max_tokens=1500)
    if error:
        return {"category": "未分类", "methods": f"分析失败: {error}", "innovations": "", "keywords_enhanced": ""}
    
    try:
        # 清理可能的markdown代码块
        content = re.sub(r'^```json\s*', '', content)
        content = re.sub(r'```\s*$', '', content)
        result = json.loads(content.strip())
        
        # 验证分类是否合法
        if result.get('category') not in categories:
            result['category'] = '其他'
        
        # 如果分类是"其他"且LLM推荐了新分类，自动添加并应用
        recommended = result.get('recommended_category', '').strip()
        if result.get('category') == '其他' and recommended:
            add_category(recommended)
            result['category'] = recommended
            result['recommended_category'] = ''  # 清空，已处理
        
        return result
    except json.JSONDecodeError:
        # 尝试正则提取
        return {
            "category": extract_field(content, "category") or "未分类",
            "recommended_category": extract_field(content, "recommended_category") or "",
            "methods": extract_field(content, "methods") or content[:500],
            "innovations": extract_field(content, "innovations") or "",
            "keywords_enhanced": extract_field(content, "keywords_enhanced") or ""
        }

def extract_field(text, field):
    """从文本中提取JSON字段"""
    pattern = rf'"{field}"\s*:\s*"([^"]*)"'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    # 尝试单引号
    pattern = rf"'{field}'\s*:\s*'([^']*)'"
    match = re.search(pattern, text)
    return match.group(1) if match else None

# ============ LLM辅助解析 ============
def llm_extract_title_abstract(text, filename):
    """用LLM从PDF文本中提取标题和摘要"""
    # 截取前5000字符，覆盖前2页的标题+摘要+关键词区域
    sample = text[:5000]
    
    system_prompt = """你是学术论文元数据提取专家。你的任务是从PDF提取文本中准确识别论文标题和摘要。

常见PDF结构：
- 标题通常在第一页最前方，字体最大或位于顶部区域
- 摘要在Abstract/摘要标记之后，Introduction/引言之前
- 页眉(期刊名+卷号+页码)和页脚(页码+DOI)不是标题
- 作者名单和机构名不是标题

只输出JSON，不要任何额外文字。"""
    
    user_prompt = f"""请从以下PDF提取文本中识别论文的真实标题和完整摘要。

文件名: {filename}

PDF文本:
{sample}

输出JSON：
{{
    "title": "论文的真实完整标题（仅标题，不含作者机构）",
    "abstract": "完整的Abstract内容（保留原文语言和标点）"
}}

要求：
1. 标题：排除期刊名、卷号、页码、DOI、作者、机构等非标题内容
2. 摘要：从Abstract/摘要标记开始到Introduction/引言/Keywords之前的全部文字
3. 如果摘要很长，保留完整内容，不要截断
4. 只输出JSON，不要markdown代码块"""
    
    content, error = call_llm(system_prompt, user_prompt, max_tokens=1000)
    if error:
        return None
    
    try:
        content = re.sub(r'^```json\s*', '', content)
        content = re.sub(r'^```\s*', '', content)
        content = re.sub(r'```\s*$', '', content)
        result = json.loads(content.strip())
        return result
    except json.JSONDecodeError:
        # 尝试正则提取
        title = extract_field(content, "title") or ""
        abstract = extract_field(content, "abstract") or ""
        if title or abstract:
            return {"title": title, "abstract": abstract}
        return None

def llm_full_analysis(text, filename, keywords, categories):
    """一次LLM调用完成标题提取+摘要提取+分类分析"""
    categories_str = "\n".join([f"- {c}" for c in categories])
    sample = text[:5000]
    
    system_prompt = """你是AIDD领域的学术论文分析专家。从PDF提取文本中准确识别标题和摘要，并分析论文内容。

常见PDF结构：
- 标题通常在第一页最前方，字体最大或位于顶部
- 摘要在Abstract/摘要标记之后，Introduction/引言之前
- 页眉(期刊名+卷号+页码)和页脚不是标题

只输出JSON，不要任何额外文字或代码块。"""
    
    user_prompt = f"""请从以下PDF文本中：1)提取真实标题和完整摘要 2)分析论文内容

文件名: {filename}
关键词(正则提取): {keywords or '无'}
可用分类：
{categories_str}

PDF文本:
{sample}

输出JSON：
{{
    "title": "论文真实完整标题（仅标题，不含作者机构期刊名）",
    "abstract": "完整Abstract内容（保留原文语言）",
    "category": "最匹配的分类名称，必须从上面的列表中选择",
    "recommended_category": "如果以上分类都不合适，推荐更准确的分类名；合适则留空",
    "methods": "主要研究方法，2-3句话概括",
    "innovations": "核心创新点，2-3句话概括",
    "keywords_enhanced": "从摘要中提取的额外关键词，逗号分隔"
}}

要求：
1. 标题排除期刊名、卷号、页码、DOI、作者、机构等
2. 摘要从Abstract到Introduction之间，保留完整内容
3. category必须从给定列表选，都不合适填"其他"并推荐新分类
4. 只输出JSON，不要markdown代码块"""
    
    content, error = call_llm(system_prompt, user_prompt, max_tokens=2000)
    if error:
        return {"category": "未分类", "methods": f"分析失败: {error}", "innovations": "", "keywords_enhanced": ""}
    
    try:
        content = re.sub(r'^```json\s*', '', content)
        content = re.sub(r'^```\s*', '', content)
        content = re.sub(r'```\s*$', '', content)
        result = json.loads(content.strip())
        
        # 验证分类
        if result.get('category') not in categories:
            result['category'] = '其他'
        
        # 处理推荐分类
        recommended = result.get('recommended_category', '').strip()
        if result.get('category') == '其他' and recommended:
            add_category(recommended)
            result['category'] = recommended
            result['recommended_category'] = ''
        
        return result
    except json.JSONDecodeError:
        return {
            "title": extract_field(content, "title") or "",
            "abstract": extract_field(content, "abstract") or "",
            "category": extract_field(content, "category") or "未分类",
            "recommended_category": extract_field(content, "recommended_category") or "",
            "methods": extract_field(content, "methods") or content[:500],
            "innovations": extract_field(content, "innovations") or "",
            "keywords_enhanced": extract_field(content, "keywords_enhanced") or ""
        }

def is_bad_title(title, filename):
    """判断提取的标题质量是否可疑"""
    if not title:
        return True
    # 标题过短
    if len(title) < 10:
        return True
    # 标题就是文件名
    if title == filename.replace('.pdf', ''):
        return True
    # 标题包含大量数字（可能是页眉页脚）
    if sum(c.isdigit() for c in title) / len(title) > 0.3:
        return True
    # 标题以常见非标题词开头
    bad_starts = ['vol.', 'page', 'chapter', 'section', 'figure', 'table', 'pp.']
    if any(title.lower().startswith(x) for x in bad_starts):
        return True
    return False

def is_bad_abstract(abstract):
    """判断提取的摘要质量是否可疑"""
    if not abstract:
        return True
    # 摘要过短
    if len(abstract) < 50:
        return True
    # 摘要和标题相同（说明提取逻辑没有正确区分）
    return False

# ============ 去重检测 ============
def check_duplicate(file_path):
    """检测文献是否已存在。返回 (is_duplicate, reason, existing_id)"""
    filename = os.path.basename(file_path)
    
    conn = get_db_conn()
    c = conn.cursor()
    
    # 检测1：文件名重复（提取存储的文件名部分比较）
    c.execute('SELECT id, title, file_path FROM papers')
    for row in c.fetchall():
        existing_filename = os.path.basename(row[2])
        if existing_filename.lower() == filename.lower():
            conn.close()
            return True, f"文件名重复: {filename}", row[0]
    
    # 检测2：标题重复（先快速提取标题，不调用LLM）
    try:
        doc = fitz.open(file_path)
        metadata = doc.metadata
        text = ""
        for i in range(min(2, len(doc))):
            text += doc.load_page(i).get_text() + "\n"
        doc.close()
        
        title = metadata.get('title', '') or extract_title_from_text(text) or filename.replace('.pdf', '')
        title = title.strip().lower()
        
        if title and len(title) > 5:  # 标题有效才检测
            c.execute('SELECT id, title FROM papers')
            for row in c.fetchall():
                existing_title = (row[1] or '').strip().lower()
                # 精确匹配或包含关系
                if existing_title == title or title in existing_title or existing_title in title:
                    conn.close()
                    return True, f"标题重复: '{title}'", row[0]
    except Exception:
        pass
    
    conn.close()
    return False, "", None

# ============ 数据库操作 ============
def add_paper_to_db(file_path, tags='', force=False):
    """添加文献到数据库，自动解析全部信息
    
    Args:
        file_path: PDF文件路径
        tags: 标签
        force: 是否强制导入（跳过去重检测）
    
    Returns:
        (paper_id, analysis_result) 成功
        (None, error_message) 失败或重复
    """
    filename = os.path.basename(file_path)
    
    # 去重检测
    if not force:
        is_dup, reason, existing_id = check_duplicate(file_path)
        if is_dup:
            return None, f"重复文献 [{reason}] 已存在(ID: {existing_id})"
    
    dest_path = os.path.join(PDF_STORAGE, f"{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}_{filename}")
    shutil.copy2(file_path, dest_path)
    
    # 提取PDF元数据
    doc = fitz.open(dest_path)
    metadata = doc.metadata
    doc.close()
    
    # 提取文本（前5页足够覆盖标题+摘要+关键词）
    full_text = extract_text_from_pdf(dest_path)
    
    # 正则先提取基本信息作为初始值
    title = metadata.get('title', '') or extract_title_from_text(full_text) or filename.replace('.pdf', '')
    abstract = extract_abstract(full_text)
    keywords = extract_keywords(full_text)
    authors = metadata.get('author', '')
    
    # 获取当前分类列表
    categories = get_categories()
    
    # LLM可用时：一次调用完成标题+摘要提取+分类分析
    if LLM_API_KEY:
        analysis = llm_full_analysis(full_text, filename, keywords, categories)
        if analysis.get('title'):
            title = analysis['title']
        if analysis.get('abstract'):
            abstract = analysis['abstract']
    else:
        analysis = analyze_paper(title, abstract, keywords, categories)
    
    # 合并关键词
    all_keywords = keywords
    if analysis.get('keywords_enhanced'):
        all_keywords = f"{keywords}; {analysis['keywords_enhanced']}" if keywords else analysis['keywords_enhanced']
    
    # 获取页数（确保关闭文件句柄）
    page_count = 0
    try:
        doc_pc = fitz.open(dest_path)
        page_count = len(doc_pc)
        doc_pc.close()
    except Exception:
        pass
    
    conn = get_db_conn()
    c = conn.cursor()
    c.execute('''INSERT INTO papers 
    (title, authors, abstract, keywords, file_path, page_count, added_date, tags, category, methods, innovations)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
    (title, authors, abstract, all_keywords, dest_path, 
         page_count, datetime.now().isoformat(), tags,
         analysis.get('category', '未分类'),
         analysis.get('methods', ''),
         analysis.get('innovations', '')))
    conn.commit()
    paper_id = c.lastrowid
    conn.close()
    
    return paper_id, analysis

# ============ GUI ============
class LiteratureManager:
    def __init__(self, root):
        self.root = root
        self.root.title("文献管理器 - AIDD专用版")
        self.root.geometry("1400x800")
        
        # 菜单栏
        menubar = tk.Menu(root)
        cat_menu = tk.Menu(menubar, tearoff=0)
        cat_menu.add_command(label="管理分类...", command=self.manage_categories)
        menubar.add_cascade(label="分类", menu=cat_menu)
        
        # 模型选择菜单
        model_menu = tk.Menu(menubar, tearoff=0)
        self.model_var = tk.StringVar(value=LLM_MODEL)
        for name in AVAILABLE_MODELS:
            model_menu.add_radiobutton(label=name, variable=self.model_var, value=name, command=self.on_model_change)
        menubar.add_cascade(label="解析引擎", menu=model_menu)
        
        root.config(menu=menubar)
        
        # 搜索框
        search_frame = ttk.Frame(root)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(search_frame, text="搜索:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.refresh_list())
        ttk.Entry(search_frame, textvariable=self.search_var, width=40).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(search_frame, text="分类筛选:").pack(side=tk.LEFT, padx=(20,0))
        self.cat_filter = ttk.Combobox(search_frame, values=["全部"] + get_categories(), width=20, state="readonly")
        self.cat_filter.set("全部")
        self.cat_filter.bind('<<ComboboxSelected>>', lambda e: self.refresh_list())
        self.cat_filter.pack(side=tk.LEFT, padx=5)
        
        # 当前模型显示
        self.model_label = ttk.Label(search_frame, text=f"引擎: {LLM_MODEL}", foreground="gray")
        self.model_label.pack(side=tk.LEFT, padx=(20,0))
        
        ttk.Button(search_frame, text="导入PDF", command=self.import_pdf).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="打开PDF", command=self.open_pdf).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="删除", command=self.delete_paper).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="批量删除", command=self.delete_selected_papers).pack(side=tk.LEFT, padx=5)
        
        # 主区域
        paned = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 左侧列表
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        columns = ('title', 'category', 'authors', 'pages')
        self.tree = ttk.Treeview(left_frame, columns=columns, show='headings')
        self.sort_column = None
        self.sort_reverse = False
        self.column_titles = {
            'title': '标题',
            'category': '分类',
            'authors': '作者',
            'pages': '页数'
        }
        for col, text in self.column_titles.items():
            self.tree.heading(col, text=text, command=lambda c=col: self.sort_by_column(c))
        self.tree.column('title', width=280)
        self.tree.column('category', width=100)
        self.tree.column('authors', width=120)
        self.tree.column('pages', width=50)
        
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        self.tree.bind('<Double-1>', lambda e: self.open_pdf())
        
        # 右侧详情
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=2)
        
        # 基本信息
        info_frame = ttk.LabelFrame(right_frame, text="文献信息", padding=5)
        info_frame.pack(fill=tk.X, pady=5)
        
        self.info_title = ttk.Label(info_frame, text="标题: ", wraplength=600, justify=tk.LEFT)
        self.info_title.pack(anchor=tk.W)
        self.info_author = ttk.Label(info_frame, text="作者: ")
        self.info_author.pack(anchor=tk.W)
        self.info_category = ttk.Label(info_frame, text="分类: ")
        self.info_category.pack(anchor=tk.W)
        self.info_keywords = ttk.Label(info_frame, text="关键词: ", wraplength=600, justify=tk.LEFT)
        self.info_keywords.pack(anchor=tk.W)
        
        # 标签和分类编辑
        edit_frame = ttk.Frame(right_frame)
        edit_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(edit_frame, text="标签:").pack(side=tk.LEFT)
        self.tag_var = tk.StringVar()
        ttk.Entry(edit_frame, textvariable=self.tag_var, width=25).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(edit_frame, text="分类:").pack(side=tk.LEFT, padx=(15,0))
        self.cat_var = ttk.Combobox(edit_frame, values=get_categories(), width=20, state="readonly")
        self.cat_var.pack(side=tk.LEFT, padx=5)
        ttk.Button(edit_frame, text="保存", command=self.save_metadata).pack(side=tk.LEFT)
        
        # 方法与创新点
        analysis_frame = ttk.LabelFrame(right_frame, text="AI分析", padding=5)
        analysis_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(analysis_frame, text="主要方法:").pack(anchor=tk.W)
        self.methods_text = tk.Text(analysis_frame, height=3, wrap=tk.WORD)
        self.methods_text.pack(fill=tk.X)
        
        ttk.Label(analysis_frame, text="创新点:").pack(anchor=tk.W)
        self.innovations_text = tk.Text(analysis_frame, height=3, wrap=tk.WORD)
        self.innovations_text.pack(fill=tk.X)
        
        # 摘要
        abs_frame = ttk.LabelFrame(right_frame, text="摘要", padding=5)
        abs_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.abstract_text = scrolledtext.ScrolledText(abs_frame, wrap=tk.WORD)
        self.abstract_text.pack(fill=tk.BOTH, expand=True)
        
        self.current_paper_id = None
        self.refresh_list()
    
    def sort_by_column(self, column):
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False
        self.refresh_list()
    
    def get_sort_key(self, row):
        if self.sort_column == 'pages':
            return row[4] or 0
        if self.sort_column == 'category':
            text = row[2] or '未分类'
        elif self.sort_column == 'authors':
            text = row[3] or ''
        else:
            text = row[1] or ''
        
        text = str(text).strip()
        if lazy_pinyin:
            return ''.join(lazy_pinyin(text)).lower()
        return text.casefold()
    
    def update_sort_headings(self):
        for col, text in self.column_titles.items():
            marker = ''
            if self.sort_column == col:
                marker = ' ↓' if self.sort_reverse else ' ↑'
            self.tree.heading(col, text=text + marker, command=lambda c=col: self.sort_by_column(c))
    
    def refresh_list(self):
        search = self.search_var.get().lower()
        cat_filter = self.cat_filter.get()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn = get_db_conn()
        c = conn.cursor()
        
        query = '''SELECT id, title, category, authors, page_count, added_date FROM papers WHERE 1=1'''
        params = []
        
        if search:
            query += ''' AND (lower(title) LIKE ? OR lower(authors) LIKE ? 
                        OR lower(abstract) LIKE ? OR lower(keywords) LIKE ? 
                        OR lower(tags) LIKE ? OR lower(methods) LIKE ? 
                        OR lower(innovations) LIKE ?)'''
            params.extend([f'%{search}%'] * 7)
        
        if cat_filter != "全部":
            query += " AND category = ?"
            params.append(cat_filter)
        
        query += " ORDER BY added_date DESC"
        
        c.execute(query, params)
        rows = c.fetchall()
        conn.close()
        
        if self.sort_column:
            rows.sort(key=self.get_sort_key, reverse=self.sort_reverse)
        
        self.update_sort_headings()
        
        for row in rows:
            self.tree.insert('', tk.END, values=(row[1], row[2] or '未分类', row[3] or '', row[4] or 0), iid=row[0])
    
    def on_select(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        
        paper_id = selection[0]
        self.current_paper_id = paper_id
        
        conn = get_db_conn()
        c = conn.cursor()
        c.execute('''SELECT title, authors, category, keywords, abstract, tags, methods, innovations, file_path 
                     FROM papers WHERE id=?''', (paper_id,))
        row = c.fetchone()
        conn.close()
        
        if row:
            self.info_title.config(text=f"标题: {row[0]}")
            self.info_author.config(text=f"作者: {row[1] or '未知'}")
            self.info_category.config(text=f"分类: {row[2] or '未分类'}")
            self.info_keywords.config(text=f"关键词: {row[3] or '无'}")
            
            self.cat_var.set(row[2] or '未分类')
            self.tag_var.set(row[5] or '')
            
            self.methods_text.delete(1.0, tk.END)
            self.methods_text.insert(1.0, row[6] or '')
            
            self.innovations_text.delete(1.0, tk.END)
            self.innovations_text.insert(1.0, row[7] or '')
            
            self.abstract_text.delete(1.0, tk.END)
            self.abstract_text.insert(1.0, row[4] or '无摘要')
    
    def import_pdf(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        if not files:
            return
        
        progress = tk.Toplevel(self.root)
        progress.title("导入中...")
        progress.geometry("460x160")
        ttk.Label(progress, text=f"正在并行处理 {len(files)} 个文件...").pack(pady=10)
        progress_bar = ttk.Progressbar(progress, mode='determinate', maximum=len(files))
        progress_bar.pack(fill=tk.X, padx=20, pady=10)
        status_label = ttk.Label(progress, text="")
        status_label.pack()
        
        def import_one(file_path):
            filename = os.path.basename(file_path)
            try:
                result, info = add_paper_to_db(file_path)
                if result is None:
                    return False, filename, info
                return True, filename, info
            except Exception as e:
                import traceback
                err_detail = traceback.format_exc()
                print(f"导入失败 {file_path}: {e}\n{err_detail}")
                return False, filename, str(e)[:200]
        
        def import_task():
            success_count = 0
            skip_count = 0
            skip_details = []
            finished = 0
            max_workers = min(3, len(files))
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(import_one, file_path) for file_path in files]
                
                for future in as_completed(futures):
                    ok, filename, info = future.result()
                    finished += 1
                    
                    if ok:
                        success_count += 1
                    else:
                        skip_count += 1
                        skip_details.append(f"{filename}: {info}")
                    
                    self.root.after(
                        0,
                        lambda v=finished, name=filename: (
                            progress_bar.config(value=v),
                            status_label.config(text=f"已完成 {v}/{len(files)}：{name}")
                        )
                    )
            
            self.root.after(0, progress.destroy)
            self.root.after(0, self.refresh_list)
            
            msg = f"成功导入: {success_count} 个\n跳过/失败: {skip_count} 个"
            if skip_details:
                msg += "\n\n跳过/失败的文件:\n" + "\n".join(skip_details[:10])
                if len(skip_details) > 10:
                    msg += f"\n...等共 {len(skip_details)} 个"
            
            self.root.after(0, lambda: messagebox.showinfo("导入完成", msg))
        
        threading.Thread(target=import_task, daemon=True).start()
    
    def open_pdf(self):
        if not self.current_paper_id:
            return
        
        conn = get_db_conn()
        c = conn.cursor()
        c.execute('SELECT file_path FROM papers WHERE id=?', (self.current_paper_id,))
        row = c.fetchone()
        conn.close()
        
        if row and os.path.exists(row[0]):
            os.startfile(row[0])
    
    def delete_paper(self):
        if not self.current_paper_id:
            return
        
        if not messagebox.askyesno("确认", "确定删除这篇文献？"):
            return
        
        conn = get_db_conn()
        c = conn.cursor()
        c.execute('SELECT file_path FROM papers WHERE id=?', (self.current_paper_id,))
        row = c.fetchone()
        
        pdf_deleted = False
        if row and os.path.exists(row[0]):
            try:
                os.remove(row[0])
                pdf_deleted = True
            except PermissionError:
                # 文件被占用，尝试移到待删除目录
                try:
                    pending_dir = os.path.join(os.path.dirname(row[0]), '_pending_delete')
                    os.makedirs(pending_dir, exist_ok=True)
                    import time
                    new_name = f"{int(time.time())}_{os.path.basename(row[0])}"
                    os.rename(row[0], os.path.join(pending_dir, new_name))
                    pdf_deleted = True
                except Exception:
                    pass  # 文件删不掉，但数据库记录仍可删除
        
        try:
            c.execute('DELETE FROM papers WHERE id=?', (self.current_paper_id,))
            conn.commit()
        except sqlite3.OperationalError as e:
            conn.rollback()
            messagebox.showerror("数据库错误", f"删除失败: {e}")
            conn.close()
            return
        conn.close()
        
        self.current_paper_id = None
        self.refresh_list()
        self.clear_detail()
    
    def save_metadata(self):
        if not self.current_paper_id:
            return
        
        tags = self.tag_var.get()
        category = self.cat_var.get()
        methods = self.methods_text.get(1.0, tk.END).strip()
        innovations = self.innovations_text.get(1.0, tk.END).strip()
        
        conn = get_db_conn()
        c = conn.cursor()
        c.execute('''UPDATE papers SET tags=?, category=?, methods=?, innovations=? WHERE id=?''',
                  (tags, category, methods, innovations, self.current_paper_id))
        conn.commit()
        conn.close()
        
        self.refresh_list()
        messagebox.showinfo("完成", "已保存")
    
    def on_model_change(self):
        """切换解析引擎"""
        global LLM_MODEL
        LLM_MODEL = AVAILABLE_MODELS[self.model_var.get()]
        self.model_label.config(text=f"引擎: {LLM_MODEL}")
        messagebox.showinfo("引擎切换", f"已切换至: {LLM_MODEL}\n下次导入文献时生效")
    
    def delete_selected_papers(self):
        """批量删除选中的文献"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请先选择要删除的文献（按住Ctrl可多选）")
            return
        
        if not messagebox.askyesno("确认删除", f"确定删除选中的 {len(selected)} 篇文献？\n此操作不可恢复！"):
            return
        
        conn = get_db_conn()
        c = conn.cursor()
        
        deleted = 0
        for item_id in selected:
            c.execute('SELECT file_path FROM papers WHERE id=?', (item_id,))
            row = c.fetchone()
            
            if row:
                # 删除PDF文件
                if os.path.exists(row[0]):
                    try:
                        os.remove(row[0])
                    except PermissionError:
                        try:
                            pending_dir = os.path.join(os.path.dirname(row[0]), '_pending_delete')
                            os.makedirs(pending_dir, exist_ok=True)
                            import time
                            new_name = f"{int(time.time())}_{os.path.basename(row[0])}"
                            os.rename(row[0], os.path.join(pending_dir, new_name))
                        except Exception:
                            pass
                # 删除数据库记录
                try:
                    c.execute('DELETE FROM papers WHERE id=?', (item_id,))
                    deleted += 1
                except sqlite3.OperationalError:
                    pass
        
        try:
            conn.commit()
        except sqlite3.OperationalError:
            conn.rollback()
        conn.close()
        
        self.current_paper_id = None
        self.refresh_list()
        self.clear_detail()
        messagebox.showinfo("完成", f"已删除 {deleted} 篇文献")
    
    def manage_categories(self):
        """管理分类对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("管理分类")
        dialog.geometry("300x400")
        
        ttk.Label(dialog, text="现有分类:").pack(pady=5)
        
        listbox = tk.Listbox(dialog)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        for cat in get_categories():
            listbox.insert(tk.END, cat)
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        def add_new():
            name = simpledialog.askstring("新建分类", "分类名称:", parent=dialog)
            if name and add_category(name):
                listbox.insert(tk.END, name)
                self.cat_filter['values'] = ["全部"] + get_categories()
                self.cat_var['values'] = get_categories()
        
        def delete_selected():
            sel = listbox.curselection()
            if sel:
                name = listbox.get(sel[0])
                if messagebox.askyesno("确认", f"删除分类 '{name}'？\n该分类下的文献将变为'未分类'", parent=dialog):
                    delete_category(name)
                    listbox.delete(sel[0])
                    self.cat_filter['values'] = ["全部"] + get_categories()
                    self.cat_var['values'] = get_categories()
        
        ttk.Button(btn_frame, text="添加", command=add_new).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="删除", command=delete_selected).pack(side=tk.LEFT, padx=5)
    
    def clear_detail(self):
        self.info_title.config(text="标题: ")
        self.info_author.config(text="作者: ")
        self.info_category.config(text="分类: ")
        self.info_keywords.config(text="关键词: ")
        self.cat_var.set('')
        self.tag_var.set('')
        self.methods_text.delete(1.0, tk.END)
        self.innovations_text.delete(1.0, tk.END)
        self.abstract_text.delete(1.0, tk.END)

def ask_api_key(root):
    global LLM_API_KEY

    if LLM_API_KEY:
        return True

    key = simpledialog.askstring(
        "DeepSeek API Key",
        "请输入你的 DeepSeek API Key：",
        parent=root,
        show="*"
    )

    if not key:
        messagebox.showwarning("未设置 API Key", "未输入 API Key，AI 分析功能将不可用。")
        return False

    LLM_API_KEY = key.strip()
    return True


def main():
    init_db()
    root = tk.Tk()
    ask_api_key(root)
    app = LiteratureManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
