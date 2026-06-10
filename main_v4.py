import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog
import sqlite3
import fitz
import os
import sys
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


import customtkinter as ctk

# ============ Theme ============
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

C = {
    "bg":            "#f7f9fb",
    "sidebar":       "#edf2f5",
    "sidebar_hover": "#dde8ed",
    "surface":       "#ffffff",
    "card":          "#f2f6f8",
    "border":        "#d7e1e6",
    "primary":       "#287c7a",
    "primary_hover": "#1f6765",
    "accent":        "#3b6ea8",
    "text":          "#263238",
    "text_secondary": "#62727b",
    "text_muted":    "#8a9aa3",
    "success":       "#3f8f5f",
    "warning":       "#d7a23a",
    "error":         "#c95f5f",
    "tree_bg":       "#ffffff",
    "tree_alt":      "#f4f8fa",
    "tree_sel":      "#d8edf0",
    "input_bg":      "#f8fbfc",
    "input_border":  "#cfdde3",
    "input_focus":   "#287c7a",
}

FONT_TITLE  = ("Microsoft YaHei UI", 16, "bold")
FONT_HEADER = ("Microsoft YaHei UI", 13, "bold")
FONT_BODY   = ("Microsoft YaHei UI", 12)
FONT_SMALL  = ("Microsoft YaHei UI", 11)
FONT_MONO   = ("Consolas", 10)

"""
文献智能管理系统 v4
面向领域：结构生物学 (Structural Biology) / CADD (计算机辅助药物设计) / 细胞生物学 (Cell Biology)
基于 v2 (AIDD专用版) 改造，保持原有架构和设计模式，仅进行领域术语与方法论适配。

主要变更：
  - 文献分类体系：蛋白质结构/分子对接/细胞信号等三大领域交叉分类
  - LLM 分析框架：覆盖结构解析、虚拟筛选、信号通路分析等
  - 课题建议方法论：结构生物学×CADD×细胞生物学跨领域整合
  - 关键词体系与期刊偏好：Nature Structural & Molecular Biology, JCIM, Cell 等
"""

# ============ 配置 ============
APP_ICON_NAME = "app_icon.ico"
APP_ICON_SOURCE_PNG = ""  # 运行时从同目录查找 PNG，打包时仅需提供 ico


def resource_path(relative_path):
    """兼容源码运行和 PyInstaller 打包后的资源路径。"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


def set_app_icon(root):
    """设置窗口左上角和任务栏图标；优先使用打包进来的 ico。"""
    icon_path = resource_path(APP_ICON_NAME)
    if os.path.exists(icon_path):
        try:
            root.iconbitmap(icon_path)
            return
        except Exception:
            pass

    png_path = APP_ICON_SOURCE_PNG or resource_path("StructBioCADD_CellBio_文献系统图标.png")
    if png_path and os.path.exists(png_path):
        try:
            icon_img = tk.PhotoImage(file=png_path)
            root.iconphoto(True, icon_img)
            root._app_icon_ref = icon_img
        except Exception:
            pass


DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "literature.db")
PDF_STORAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdfs")

# 国家名常量（用于过滤作者提取中的地点行）
COUNTRY_NAMES = {
    'JAPAN', 'CHINA', 'KOREA', 'INDIA', 'BRAZIL', 'GERMANY',
    'FRANCE', 'ITALY', 'SPAIN', 'RUSSIA', 'UKRAINE', 'POLAND',
    'AUSTRALIA', 'CANADA', 'MEXICO', 'ARGENTINA', 'TURKEY',
    'EGYPT', 'IRAN', 'IRAQ', 'ISRAEL', 'PAKISTAN', 'BANGLADESH',
    'INDONESIA', 'THAILAND', 'VIETNAM', 'MALAYSIA', 'SINGAPORE',
    'PHILIPPINES', 'TAIWAN', 'HONG KONG', 'NETHERLANDS', 'BELGIUM',
    'SWEDEN', 'NORWAY', 'DENMARK', 'FINLAND', 'SWITZERLAND',
    'AUSTRIA', 'PORTUGAL', 'GREECE', 'CZECH', 'ROMANIA',
    'HUNGARY', 'IRELAND', 'NEW ZEALAND', 'SOUTH AFRICA',
    'NIGERIA', 'KENYA', 'CHILE', 'COLOMBIA', 'PERU',
    'VENEZUELA', 'CUBA', 'UK', 'USA', 'UAE',
    'UNITED STATES', 'UNITED KINGDOM', 'REPUBLIC OF KOREA',
    'PEOPLES REPUBLIC OF CHINA', 'RUSSIAN FEDERATION',
}

# LLM配置 - 默认 DeepSeek API，并支持本地自定义模型
MODEL_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model_config.json")
DEFAULT_MODEL_CONFIGS = {
    "deepseek-v4-pro": {
        "model": "deepseek-v4-pro",
        "base_url": "https://api.deepseek.com/v1",
        "api_key_env": "DEEPSEEK_API_KEY",
        "api_key": ""
    },
    "deepseek-v4-flash": {
        "model": "deepseek-v4-flash",
        "base_url": "https://api.deepseek.com/v1",
        "api_key_env": "DEEPSEEK_API_KEY",
        "api_key": ""
    }
}


def load_model_configs():
    configs = {name: cfg.copy() for name, cfg in DEFAULT_MODEL_CONFIGS.items()}
    if os.path.exists(MODEL_CONFIG_PATH):
        try:
            with open(MODEL_CONFIG_PATH, "r", encoding="utf-8") as f:
                saved = json.load(f)
            if isinstance(saved, dict):
                for name, cfg in saved.items():
                    if isinstance(cfg, dict) and name not in DEFAULT_MODEL_CONFIGS:
                        configs[name] = {
                            "model": (cfg.get("model") or name).strip(),
                            "base_url": (cfg.get("base_url") or "https://api.deepseek.com/v1").strip(),
                            "api_key_env": (cfg.get("api_key_env") or "").strip(),
                            "api_key": (cfg.get("api_key") or "").strip()
                        }
        except Exception:
            pass
    return configs


def save_model_configs():
    custom = {
        name: cfg for name, cfg in MODEL_CONFIGS.items()
        if name not in DEFAULT_MODEL_CONFIGS
    }
    with open(MODEL_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(custom, f, ensure_ascii=False, indent=2)


def refresh_available_models():
    global AVAILABLE_MODELS
    AVAILABLE_MODELS = {
        name: (cfg.get("model") or name)
        for name, cfg in MODEL_CONFIGS.items()
    }


MODEL_CONFIGS = load_model_configs()
AVAILABLE_MODELS = {}
refresh_available_models()
CURRENT_MODEL_NAME = os.environ.get("LLM_MODEL", "deepseek-v4-pro")
LLM_MODEL = CURRENT_MODEL_NAME
LLM_BASE_URL = ""
LLM_API_KEY = ""


def apply_model_config(model_name):
    """应用当前模型配置，兼容 OpenAI-style /chat/completions API。"""
    global CURRENT_MODEL_NAME, LLM_MODEL, LLM_BASE_URL, LLM_API_KEY
    if model_name not in MODEL_CONFIGS:
        model_name = "deepseek-v4-pro"
    cfg = MODEL_CONFIGS[model_name]
    CURRENT_MODEL_NAME = model_name
    LLM_MODEL = (cfg.get("model") or model_name).strip()
    LLM_BASE_URL = (cfg.get("base_url") or "https://api.deepseek.com/v1").strip().rstrip("/")

    env_name = (cfg.get("api_key_env") or "").strip()
    env_key = os.environ.get(env_name, "").strip() if env_name else ""
    configured_key = (cfg.get("api_key") or "").strip()
    generic_key = os.environ.get("LLM_API_KEY", "").strip()
    LLM_API_KEY = env_key or configured_key or generic_key
    return cfg


def remember_api_key_for_current_model(api_key):
    """保存本次会话输入的 API Key；默认 DeepSeek 模型共享同一个 Key。"""
    api_key = (api_key or "").strip()
    if not api_key:
        return
    if CURRENT_MODEL_NAME in DEFAULT_MODEL_CONFIGS:
        for name in DEFAULT_MODEL_CONFIGS:
            MODEL_CONFIGS[name]["api_key"] = api_key
    else:
        MODEL_CONFIGS[CURRENT_MODEL_NAME]["api_key"] = api_key
        save_model_configs()


apply_model_config(CURRENT_MODEL_NAME)

os.makedirs(PDF_STORAGE, exist_ok=True)

# 预设分类
DEFAULT_CATEGORIES = [
    # == 结构生物学 ==
    "蛋白质结构解析", "核酸结构", "复合物结构", "结构解析方法",
    "蛋白质-配体相互作用", "蛋白质-蛋白质相互作用", "构象动力学",
    # == CADD ==
    "分子对接", "虚拟筛选", "药效团建模", "QSAR模型",
    "分子动力学模拟", "ADMET预测", "结合自由能计算",
    # == 细胞生物学 ==
    "细胞信号通路", "细胞周期与增殖", "细胞凋亡与死亡",
    "细胞分化与发育", "细胞成像与分析", "基因表达调控",
    # == 通用 ==
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
    
    # Schema migration：补充旧版本数据库缺失的字段
    c.execute("PRAGMA table_info(papers)")
    existing_cols = {row[1] for row in c.fetchall()}
    for col, definition in [
        ("doi",         "TEXT DEFAULT ''"),
        ("year",        "TEXT DEFAULT ''"),
        ("tags",        "TEXT DEFAULT ''"),
        ("category",    "TEXT DEFAULT ''"),
        ("methods",     "TEXT DEFAULT ''"),
        ("innovations", "TEXT DEFAULT ''"),
    ]:
        if col not in existing_cols:
            c.execute(f"ALTER TABLE papers ADD COLUMN {col} {definition}")

    # 常用查询字段索引
    c.execute("CREATE INDEX IF NOT EXISTS idx_papers_lower_title ON papers (lower(title))")
    c.execute("CREATE INDEX IF NOT EXISTS idx_papers_category ON papers (category)")

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
        with fitz.open(pdf_path) as doc:
            text = ""
            for i in range(min(max_pages, len(doc))):
                page = doc.load_page(i)
                text += page.get_text() + "\n"
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

def extract_doi_from_text(text):
    """从PDF文本中提取DOI（增强版）
    支持格式：doi: / doi.org/ / 裸DOI / DX.DOI / 参考文献内DOI
    搜索范围扩大到前 30000 字符，覆盖页眉/页脚/参考文献首行。
    多轮搜索：标题页 → 前部 → 更大范围，优先返回标题页DOI。
    """
    # 清理文本中的零宽字符和不可见字符，避免阻断正则匹配
    cleaned = re.sub(r'[\u200b\u200c\u200d\ufeff\u00ad]', '', text)

    # DOI 尾部清理字符集（常见PDF排版会附加的标点）
    _STRIP = '.,;:）)》》」\'"'

    def _find_doi(sample):
        """在给定文本片段中搜索DOI，返回首个匹配或空字符串"""
        # 1) https://doi.org/10.xxx（含 http 和无s两种）
        m = re.search(r'https?://(?:dx\.)?doi\.org/(10\.\d{4,}/\S+)', sample, re.IGNORECASE)
        if m:
            return m.group(1).rstrip(_STRIP)
        # 2) doi: 10.xxx / doi 10.xxx / doi/10.xxx / DOI: 10.xxx
        m = re.search(r'(?<![\w/])doi[:\s/]+(10\.\d{4,}/\S+)', sample, re.IGNORECASE)
        if m:
            return m.group(1).rstrip(_STRIP)
        # 3) [DOI: 10.xxx] 或 (DOI 10.xxx)
        m = re.search(r'[\[(]?\s*DOI\s*[:\s]+\s*(10\.\d{4,}/\S+)', sample, re.IGNORECASE)
        if m:
            return m.group(1).rstrip(_STRIP + '])')
        # 4) dx.doi.org/10.xxx（旧格式）
        m = re.search(r'dx\.doi\.org/(10\.\d{4,}/\S+)', sample, re.IGNORECASE)
        if m:
            return m.group(1).rstrip(_STRIP)
        # 5) 裸 DOI：10.xxxx/xxx（最宽松匹配，放最后）
        #    排除紧跟的常见非DOI字符；DOI注册号目前4-6位
        m = re.search(r'\b(10\.\d{4,6}/[^\s,;\]）》」\'"\)]+)', sample)
        if m:
            candidate = m.group(1).rstrip(_STRIP)
            # 验证：DOI路径部分应至少有一个/
            if '/' in candidate and len(candidate) > 8:
                return candidate
        return ''

    # 多轮搜索：标题页 → 前部 → 更大范围
    # 优先在标题页区域（前5000字符）找DOI，这是最可靠的位置
    for sample in (cleaned[:5000], cleaned[:15000], cleaned[:30000]):
        result = _find_doi(sample)
        if result:
            return result

    # 最终兜底：搜索全文（应对DOI只在参考文献中出现的情况）
    # 只找带明确前缀的DOI，避免全文裸DOI误匹配
    m = re.search(r'(?:doi\.org/|doi[:\s/]+)(10\.\d{4,}/\S+)', cleaned, re.IGNORECASE)
    if m:
        return m.group(1).rstrip(_STRIP)

    return ''

def extract_authors_from_text(text):
    """从PDF文本前部提取作者列表（增强版多策略方法）。
    返回逗号分隔的作者字符串，无法识别时返回空字符串。
    
    改进点：
    - 扩大搜索范围至前5000字符
    - 增加中文作者名识别
    - 增加 affiliation 行过滤
    - 多策略互补：标记行 → 模式行 → 缩写名 → 中文姓名 → 分号格式 → 多行拼接
    - 清理上标编号、affiliation残留等噪音
    """
    # 扩大搜索范围（部分PDF标题+作者跨越前2页）
    sample = text[:5000]
    lines = [l.strip() for l in sample.split('\n') if l.strip()]

    # ── affiliation 检测关键词（用于过滤机构行）────────────────
    AFFIL_KEYWORDS = {
        'university', 'institute', 'department', 'laboratory', 'school',
        'college', 'hospital', 'center', 'centre', 'faculty',
        'academy', 'research', 'national', 'science', 'technology',
        'biological', 'medical', 'pharmaceutical', 'chemistry',
        'bioengineering', 'computational', 'genomics', 'proteomics',
        '大学', '学院', '研究院', '研究所', '实验室', '医院', '中心',
        '科室', '生物', '医学', '药学院', '生命科学'
    }

    # ── 跳过检测关键词（行内含这些词则不是作者行）────────────────
    SKIP_KEYWORDS = {
        'abstract', 'introduction', 'methods', 'results', 'conclusion',
        'keywords', 'background', 'discussion', 'received', 'accepted',
        'published', 'journal', 'doi', 'correspondence', 'email',
        'figure', 'table', 'copyright', 'license', 'arxiv', 'preprint',
        'vol', 'no.', 'pp.', 'page', 'supplementary', 'appendix'
    }

    # COUNTRY_NAMES 使用模块级定义

    def _is_affiliation_line(line):
        """判断一行是否是机构/单位信息行"""
        lower = line.lower()
        if '@' in line:
            return True
        if 'http' in lower or 'www.' in lower:
            return True
        # 检查是否是国家名行（如 "JAPAN."）
        stripped = line.rstrip('.;, ')
        if stripped.isupper() and stripped in COUNTRY_NAMES:
            return True
        affil_count = sum(1 for kw in AFFIL_KEYWORDS if kw in lower)
        if affil_count >= 2:
            return True
        if re.match(r'^[\w\s,]+(?:\d{5,})?[\s,]*$', line) and any(kw in lower for kw in AFFIL_KEYWORDS):
            return True
        return False

    def _clean_author_line(line):
        """清理作者行中的噪音：上标编号、affiliation标记、ORCID等"""
        # 移除上标编号 (1) (2) (1,2) 等
        cleaned = re.sub(r'\s*[\(\[]?\d+(?:[,，\s]+\d+)*[\)\]]?', '', line)
        # 移除 * 号（通讯作者标记）
        cleaned = re.sub(r'\s*\*+', '', cleaned)
        # 移除 ORCID 标记
        cleaned = re.sub(r'(?i)\s*orcid[:\s]*\d{4}-\d{4}-\d{4}-\d{3}[\dX]', '', cleaned)
        # 移除 "these authors contributed equally" 等注释
        cleaned = re.sub(r'(?i)these\s+authors\s+contributed.*', '', cleaned)
        cleaned = re.sub(r'(?i)equal\s+contribution.*', '', cleaned)
        # 移除末尾逗号/分号
        cleaned = cleaned.rstrip(',; ')
        # 合并多余空格
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned

    # ── 策略1：寻找 "Authors:" / "Author:" / "作者:" 标记行 ──────────────
    for i, line in enumerate(lines):
        if re.match(r'(?i)^(authors?|作者)\s*[:：]', line):
            rest = re.sub(r'(?i)^(authors?|作者)\s*[:：]\s*', '', line).strip()
            if rest and len(rest) > 3:
                return _clean_author_line(rest)[:300]
            if i + 1 < len(lines):
                nxt = lines[i + 1].strip()
                if nxt and len(nxt) > 3 and not _is_affiliation_line(nxt):
                    return _clean_author_line(nxt)[:300]

    # ── 策略2：寻找典型学术作者行（多单词姓名，逗号/and/&分隔）─────
    # 姓氏单元：至少3个字母，避免把 "JAPAN." 拆成 "JAP"+"AN."
    NAME_UNIT = r'[A-Z][a-zA-Z][a-zA-Z\w\-\'\.]*\.?'
    AUTHOR_PAT = re.compile(
        r'^(?:' + NAME_UNIT + r'(?:[\s,]+|\s+(?:and|&)\s+))*'
        + NAME_UNIT +
        r'[\s,\*\d]*$',
        re.UNICODE
    )

    candidates = []
    for line in lines[1:30]:
        lower = line.lower()
        if any(kw in lower for kw in SKIP_KEYWORDS):
            continue
        if len(line) < 5 or len(line) > 400:
            continue
        if '@' in line or 'http' in lower:
            continue
        if line.isupper() and len(line) > 40:
            continue
        if _is_affiliation_line(line):
            continue
        # 先清理上标编号再匹配，避免 "Ito1,2," 等编号混淆正则
        cleaned_for_match = _clean_author_line(line)
        if AUTHOR_PAT.match(cleaned_for_match):
            cleaned = cleaned_for_match
            if len(cleaned) > 5:
                # 后验：检查提取结果不像国家名/机构名/地点行
                # 1. 全大写结果直接排除
                # 2. 以国家名结尾的地点行排除（如 "Tokyo, JAPAN."）
                # 3. 清理后单词数过少排除
                if re.match(r'^[A-Z\.\s,;]+$', cleaned):
                    continue
                cleaned_upper = cleaned.rstrip('.;, ').upper()
                # 排除整个字符串就是国家名（如 "JAPAN"、"CHINA"）
                if cleaned_upper in COUNTRY_NAMES:
                    continue
                if any(cleaned_upper.endswith(cn) for cn in COUNTRY_NAMES if len(cn) > 2):
                    continue
                candidates.append(cleaned)

    if candidates:
        return max(candidates, key=len)[:300]

    # ── 策略3：寻找 "X. Surname, Y. Surname and Z. Surname" 模式 ────
    ABBREV_PAT = re.compile(
        r'((?:[A-Z]\.\s?[A-Z]?[a-zA-Z]\w*)(?:\s*[,;]\s*(?:[A-Z]\.\s?[A-Z]?[a-zA-Z]\w*)){1,})',
        re.UNICODE
    )
    for line in lines[1:25]:
        if _is_affiliation_line(line):
            continue
        m = ABBREV_PAT.search(line)
        if m and len(m.group()) > 10:
            return _clean_author_line(m.group().strip())[:300]

    # ── 策略4：中文作者名识别 ──────────────────────────────────────
    CN_AUTHOR_PAT = re.compile(
        r'([\u4e00-\u9fff]{2,4}(?:[，,、]\s*[\u4e00-\u9fff]{2,4}){1,})'
    )
    for line in lines[1:20]:
        if _is_affiliation_line(line):
            continue
        lower = line.lower()
        if any(kw in lower for kw in SKIP_KEYWORDS):
            continue
        m = CN_AUTHOR_PAT.search(line)
        if m and len(m.group()) > 5:
            names = re.findall(r'[\u4e00-\u9fff]{2,4}', m.group())
            if len(names) >= 2:
                return m.group().strip()[:300]

    # ── 策略5：寻找 "Surname1, FirstName1; Surname2, FirstName2" 格式 ─
    SEMICOLON_PAT = re.compile(
        r'((?:[A-Z][a-z]+,\s+[A-Z]\.?(?:\s+[A-Z]\.?)?)'
        r'(?:\s*[;]\s*(?:[A-Z][a-z]+,\s+[A-Z]\.?(?:\s+[A-Z]\.?)?)){1,})',
        re.UNICODE
    )
    for line in lines[1:25]:
        if _is_affiliation_line(line):
            continue
        m = SEMICOLON_PAT.search(line)
        if m and len(m.group()) > 10:
            return _clean_author_line(m.group().strip())[:300]

    # ── 策略6：多行作者拼接 ──────────────────────────────────────
    multi_line_authors = []
    consecutive_author_lines = 0
    for i, line in enumerate(lines[1:20]):
        if _is_affiliation_line(line):
            consecutive_author_lines = 0
            continue
        lower = line.lower()
        if any(kw in lower for kw in SKIP_KEYWORDS):
            consecutive_author_lines = 0
            continue
        if len(line) < 3 or len(line) > 200:
            consecutive_author_lines = 0
            continue
        if line.isupper() and len(line) > 40:
            consecutive_author_lines = 0
            continue
        words = line.split()
        capitalized_words = [w for w in words if w and w[0].isupper()]
        has_abbrev = bool(re.search(r'[A-Z]\.\s', line))
        # 跳过国家名行（如 "JAPAN"、"CHINA"）
        line_stripped = line.rstrip('.;, ')
        if line_stripped.isupper() and line_stripped in COUNTRY_NAMES:
            consecutive_author_lines = 0
            continue
        if (len(capitalized_words) >= 2 or has_abbrev) and not line.endswith('.'):
            consecutive_author_lines += 1
            multi_line_authors.append(_clean_author_line(line))
        else:
            if consecutive_author_lines >= 2 and multi_line_authors:
                break
            consecutive_author_lines = 0
            multi_line_authors = []

    if len(multi_line_authors) >= 2:
        combined = ', '.join(multi_line_authors)
        if len(combined) > 10:
            return combined[:300]

    return ''

def lookup_crossref(title, timeout=12):
    """通过 CrossRef API 按标题查询 DOI / 作者 / 年份。
    无需 API Key；失败或匹配度不足时返回 {}。
    """
    import urllib.request
    import urllib.parse

    title = (title or '').strip()
    if len(title) < 10:
        return {}

    try:
        params = urllib.parse.urlencode({
            'query.bibliographic': title,
            'rows': 1,
            'select': 'DOI,author,published,published-print,title',
        })
        url = f'https://api.crossref.org/works?{params}'
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'LiteratureManager/4.0 (mailto:researcher@structbio.local)'}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except Exception:
        return {}

    items = data.get('message', {}).get('items', [])
    if not items:
        return {}

    item = items[0]

    # ── 标题相似度校验（避免返回不相关文章）────────────────────
    cr_titles = item.get('title', [])
    cr_title = cr_titles[0] if cr_titles else ''

    def _words(t):
        return set(w.lower() for w in re.findall(r'[a-zA-Z0-9]+', t) if len(w) > 2)

    sw_q, sw_cr = _words(title), _words(cr_title)
    if sw_q and sw_cr:
        overlap = len(sw_q & sw_cr) / max(len(sw_q), len(sw_cr))
        if overlap < 0.45:
            return {}   # 相似度不足，拒绝

    result = {}

    # DOI
    doi = (item.get('DOI') or '').strip()
    if doi:
        result['doi'] = doi

    # 作者
    authors_list = item.get('author', [])
    if authors_list:
        names = []
        for a in authors_list[:12]:
            given  = (a.get('given')  or '').strip()
            family = (a.get('family') or '').strip()
            if family:
                names.append(f"{given} {family}".strip() if given else family)
        if names:
            result['authors'] = ', '.join(names)

    # 年份（优先 published，其次 published-print）
    for pub_key in ('published', 'published-print'):
        pub = item.get(pub_key) or {}
        parts = pub.get('date-parts', [[]])
        if parts and parts[0]:
            result['year'] = str(parts[0][0])
            break

    return result


def extract_year_from_text(text):
    """从PDF正文前3000字符中提取发表年份"""
    match = re.search(r'\b(20[0-2]\d|199\d)\b', text[:3000])
    return match.group(1) if match else ''


def extract_year_from_metadata(metadata):
    """从PDF元数据中提取年份（creationDate 格式如 D:20240315...）"""
    for key in ('creationDate', 'modDate'):
        val = (metadata.get(key) or '').strip()
        m = re.search(r'(20[0-2]\d|199\d)', val)
        if m:
            return m.group(1)
    return ''


def get_all_tags():
    """获取所有文献中出现过的标签去重列表"""
    conn = get_db_conn()
    c = conn.cursor()
    c.execute("SELECT tags FROM papers WHERE tags != '' AND tags IS NOT NULL")
    all_tags = set()
    for (tags_str,) in c.fetchall():
        for tag in re.split(r'[;,]', tags_str):
            tag = tag.strip()
            if tag:
                all_tags.add(tag)
    conn.close()
    return sorted(all_tags)


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
def call_llm(system_prompt, user_prompt, max_tokens=2000, temperature=0.3, timeout=60):
    """调用LLM API（兼容 OpenAI-style /chat/completions）"""
    if not LLM_API_KEY:
        return None, f"未设置 {CURRENT_MODEL_NAME} API Key（请在解析引擎中配置，或设置 LLM_API_KEY/对应环境变量）"

    import urllib.request
    import urllib.error

    try:
        data = {
            "model": LLM_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
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

        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            return result['choices'][0]['message']['content'], None

    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='ignore')[:200]
        return None, f"HTTP {e.code}：{body}"
    except urllib.error.URLError as e:
        return None, f"网络错误：{e.reason}"
    except Exception as e:
        return None, str(e)

def analyze_paper(title, abstract, keywords, categories):
    """用LLM分析论文主题、方法、创新点和分类"""
    categories_str = "\n".join([f"- {c}" for c in categories])
    
    system_prompt = """你是一个专业的结构生物学、CADD（计算机辅助药物设计）与细胞生物学领域文献分析专家。
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
    """一次LLM调用完成标题提取+摘要提取+分类分析（增强版）
    
    改进点：
    - 文本采样量从5000提升到8000字符，覆盖更完整的标题页
    - 强化作者提取prompt，指导LLM区分作者行与机构行
    - 增加DOI提取提示
    """
    categories_str = "\n".join([f"- {c}" for c in categories])
    # 扩大采样量，确保覆盖标题+作者+摘要+关键词区域
    sample = text[:8000]
    
    system_prompt = """你是结构生物学、CADD（计算机辅助药物设计）与细胞生物学领域的学术论文分析专家。从PDF提取文本中准确识别标题、作者和摘要，并分析论文内容。

常见PDF结构：
- 标题通常在第一页最前方，字体最大或位于顶部
- 作者在标题之后、摘要之前，通常是逗号或分号分隔的人名列表
- 摘要在Abstract/摘要标记之后，Introduction/引言之前
- 页眉(期刊名+卷号+页码)和页脚不是标题
- 机构/单位信息行（含University/Institute/Department等）不是作者行

只输出JSON，不要任何额外文字或代码块。"""
    
    user_prompt = f"""请从以下PDF文本中：1)提取真实标题、作者和完整摘要 2)分析论文内容

文件名: {filename}
关键词(正则提取): {keywords or '无'}
可用分类：
{categories_str}

PDF文本:
{sample}

输出JSON：
{{
    "title": "论文真实完整标题（仅标题，不含作者机构期刊名）",
    "authors": "作者列表，逗号分隔（如 John Smith, Jane Doe, Wei Zhang）；无法确定则留空",
    "abstract": "完整Abstract内容（保留原文语言）",
    "doi": "论文DOI（格式如 10.xxxx/xxx）；无法确定则留空",
    "year": "论文发表年份，4位数字如2024；无法确定则留空",
    "category": "最匹配的分类名称，必须从上面的列表中选择",
    "recommended_category": "如果以上分类都不合适，推荐更准确的分类名；合适则留空",
    "methods": "主要研究方法，2-3句话概括",
    "innovations": "核心创新点，2-3句话概括",
    "keywords_enhanced": "从摘要中提取的额外关键词，逗号分隔"
}}

要求：
1. 标题排除期刊名、卷号、页码、DOI、作者、机构等
2. authors：在标题之后、摘要之前的作者行，只含人名（姓+名），不含机构名、学位、职称
   - 英文名格式：Firstname Lastname 或 F. Lastname
   - 中文名格式：姓名（如 张三、李四）
   - 多个作者用逗号分隔
   - 不要把机构行（University/Institute/Department等）误认为作者
   - 如果作者行含上标编号(1)(2)等，请忽略编号只提取姓名
   - 无法识别则留空，不要编造
3. 摘要从Abstract到Introduction之间，保留完整内容
4. doi：从文本中查找DOI，常见格式如 doi:10.xxx/xxx 或 https://doi.org/10.xxx/xxx
5. year从文本中寻找发表年份，通常在期刊信息或版权行中
6. category必须从给定列表选，都不合适填"其他"并推荐新分类
7. 只输出JSON，不要markdown代码块"""
    
    content, error = call_llm(system_prompt, user_prompt, max_tokens=2000)
    if error:
        return {"category": "未分类", "methods": f"分析失败: {error}", "innovations": "", "keywords_enhanced": ""}
    
    try:
        content = re.sub(r'^```json\s*', '', content)
        content = re.sub(r'^```\s*', '', content)
        content = re.sub(r'^```\s*$', '', content)
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
            "authors": extract_field(content, "authors") or "",
            "doi": extract_field(content, "doi") or "",
            "abstract": extract_field(content, "abstract") or "",
            "category": extract_field(content, "category") or "未分类",
            "recommended_category": extract_field(content, "recommended_category") or "",
            "methods": extract_field(content, "methods") or content[:500],
            "innovations": extract_field(content, "innovations") or "",
            "keywords_enhanced": extract_field(content, "keywords_enhanced") or ""
        }

# ============ 课题建议 ============


def fetch_papers_for_suggestion(paper_ids):
    """从数据库读取选中论文，并保留 PDF 全文文本供逐篇 LLM 深读。"""
    n = len(paper_ids)
    if n <= 4:
        abstract_limit, methods_limit, innov_limit = 1000, 500, 500
    elif n <= 8:
        abstract_limit, methods_limit, innov_limit = 700, 350, 350
    else:
        abstract_limit, methods_limit, innov_limit = 400, 250, 250

    conn = get_db_conn()
    c = conn.cursor()
    papers_data = []
    for pid in paper_ids:
        c.execute(
            'SELECT title, abstract, keywords, methods, innovations, category, file_path '
            'FROM papers WHERE id=?', (pid,)
        )
        row = c.fetchone()
        if not row:
            continue
        title, abstract, keywords, methods, innovations, category, file_path = row
        abstract = (abstract or '').strip()
        methods = (methods or '').strip()
        innovations = (innovations or '').strip()
        keywords = (keywords or '').strip()
        category = (category or '未分类').strip()
        title = (title or '').strip()

        # 全空记录跳过
        if not title and not abstract and not methods and not innovations:
            continue

        if not innovations and abstract:
            innovations = abstract[:200] + '（由摘要推断）'
        if not methods:
            methods = '（未记录）'

        full_text = ''
        if file_path and os.path.exists(file_path):
            try:
                full_text = extract_text_from_pdf(file_path, max_pages=9999)
                full_text = re.sub(r'\s+', ' ', full_text).strip()
            except Exception:
                full_text = ''
        if not full_text:
            full_text = abstract

        papers_data.append({
            'title': title or '无标题',
            'abstract': abstract[:abstract_limit],
            'keywords': keywords[:200],
            'methods': methods[:methods_limit],
            'innovations': innovations[:innov_limit],
            'category': category,
            'file_path': file_path,
            'full_text': full_text
        })
    conn.close()
    return papers_data


def split_text_for_llm(text, chunk_size=12000):
    """按全文顺序切块，后续逐块交给 LLM 阅读，避免只取开头。"""
    text = re.sub(r'\s+', ' ', text or '').strip()
    if not text:
        return []
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]



def summarize_paper_chunk(paper, chunk, chunk_idx, total_chunks, research_topic=""):
    """让LLM阅读论文的一段全文，输出结构化分块摘要。"""
    topic_line = f"\n用户预设研究方向/主题：{research_topic}" if research_topic else ""
    system_prompt = (
        "你是结构生物学、CADD与细胞生物学领域的论文精读助手。请基于给定论文全文片段提取对后续课题建议有用的信息，"
        "不要编造片段中不存在的内容。"
    )
    user_prompt = f"""论文标题：{paper['title']}
分类：{paper['category']}
系统已分析主要方法：{paper.get('methods') or '未记录'}
系统已分析创新点：{paper.get('innovations') or '未记录'}{topic_line}

以下是该论文全文的第 {chunk_idx}/{total_chunks} 个片段：
{chunk}

请输出中文结构化摘要，包含：
1. 该片段涉及的具体工作/实验/模型/数据
2. 方法细节
3. 结果、指标或发现
4. 局限性、假设或未解决问题
5. 可迁移到新课题的技术点
"""
    content, error = call_llm(system_prompt, user_prompt, max_tokens=1800, temperature=0.25, timeout=120)
    if error:
        return f"片段{chunk_idx}分析失败：{error}"
    return content or ""


def build_single_paper_report(paper, research_topic=""):
    """对单篇论文进行全文分块精读，并合成为详细报告。"""
    full_text = paper.get('full_text') or paper.get('abstract') or ''
    chunks = split_text_for_llm(full_text)
    if not chunks:
        chunks = [paper.get('abstract') or paper.get('innovations') or '']

    chunk_reports = []
    for idx, chunk in enumerate(chunks, 1):
        chunk_reports.append(
            summarize_paper_chunk(paper, chunk, idx, len(chunks), research_topic)
        )

    chunk_block = "\n\n".join(
        f"【片段{idx}摘要】\n{report}"
        for idx, report in enumerate(chunk_reports, 1)
    )
    topic_line = f"\n用户预设研究方向/主题：{research_topic}" if research_topic else ""
    system_prompt = (
        "你是结构生物学、CADD与细胞生物学领域的资深科研顾问。请整合一篇论文的全文分块摘要和系统已有分析，"
        "生成供跨文献课题建议使用的单篇论文详细报告。"
    )
    user_prompt = f"""论文标题：{paper['title']}
分类：{paper['category']}
关键词：{paper.get('keywords') or '无'}
系统已分析主要方法：{paper.get('methods') or '未记录'}
系统已分析创新点：{paper.get('innovations') or '未记录'}
摘要：{paper.get('abstract') or '无'}{topic_line}

全文分块精读摘要：
{chunk_block}

请输出中文详细报告，必须覆盖但不限于：
1. 研究背景与研究意义
2. 核心科学问题
3. 具体工作内容
4. 研究方法和技术路线
5. 数据、实验设置、评价指标
6. 主要结果和工作成果
7. 关键创新点
8. 局限性与未解决问题
9. 可复用资源、模型、数据或技术模块
10. 与其他文献潜在互补点
"""
    report, error = call_llm(system_prompt, user_prompt, max_tokens=3200, temperature=0.25, timeout=120)
    if error:
        report = (
            f"单篇详细报告生成失败：{error}\n"
            f"系统已分析主要方法：{paper.get('methods') or '未记录'}\n"
            f"系统已分析创新点：{paper.get('innovations') or '未记录'}\n"
            f"摘要：{paper.get('abstract') or '无'}\n"
            f"分块摘要：{chunk_block[:4000]}"
        )
    paper = dict(paper)
    paper['detailed_report'] = report or ""
    paper.pop('full_text', None)
    return paper


def enrich_papers_with_detailed_reports(papers_data, research_topic=""):
    """并发为每篇选中文献生成详细报告。"""
    if not papers_data:
        return papers_data
    max_workers = min(4, len(papers_data))
    enriched = [None] * len(papers_data)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(build_single_paper_report, paper, research_topic): idx
            for idx, paper in enumerate(papers_data)
        }
        for future in as_completed(futures):
            idx = futures[future]
            try:
                enriched[idx] = future.result()
            except Exception as e:
                fallback = dict(papers_data[idx])
                fallback['detailed_report'] = (
                    f"单篇详细报告生成异常：{e}\n"
                    f"系统已分析主要方法：{fallback.get('methods') or '未记录'}\n"
                    f"系统已分析创新点：{fallback.get('innovations') or '未记录'}\n"
                    f"摘要：{fallback.get('abstract') or '无'}"
                )
                fallback.pop('full_text', None)
                enriched[idx] = fallback
    return enriched



def detect_domain_divergence(papers_data):
    """检测选中论文是否跨多个差异较大的领域"""
    categories = set(p['category'] for p in papers_data if p['category'] != '未分类')
    if len(categories) >= 5:
        cats_str = '、'.join(list(categories)[:4]) + '等'
        return (f"注意：所选论文涉及 {len(categories)} 个不同分类（{cats_str}），"
                "请重点关注方法层面的可迁移性，并在每个建议中说明如何整合不同领域的技术。")
    return ""


def get_paper_combinations(n):
    """生成候选论文组合槽位：全集始终第一位，然后按文献数递减排列子集组合。"""
    from itertools import combinations as _comb
    MAX_TOTAL = 20
    MIN_SLOTS = 6

    if n == 2:
        return [[1, 2] for _ in range(4)]

    result = []

    # 全集组合必须排在第一位，保证 LLM 先看到全集并必须为其生成课题
    full_combo = list(range(1, n + 1))
    result.append(full_combo)

    # 然后按文献数量从多到少排列子集组合（n-1, n-2, ... 2）
    for size in range(n - 1, 1, -1):
        for combo in _comb(range(1, n + 1), size):
            result.append(list(combo))
            if len(result) >= MAX_TOTAL - 1:
                break
        if len(result) >= MAX_TOTAL - 1:
            break

    # 补充到最少槽位数
    base_subsets = [c for c in result if len(c) < n] or [full_combo]
    i = 0
    while len(result) < min(MAX_TOTAL, max(MIN_SLOTS, len(result))):
        result.append(list(base_subsets[i % len(base_subsets)]))
        i += 1
    return result[:MAX_TOTAL]


def build_combination_prompt(papers_data, combinations, divergence_warning="", research_topic=""):
    """
    为候选论文组合构建 prompt。
    LLM 必须对每个组合槽位逐一判断并输出，无价值时填 has_value=false。
    """
    n = len(papers_data)
    research_topic = (research_topic or "").strip()

    # 单篇论文报告由并发 LLM 精读生成，后续组合分析只基于这些报告整合。
    if n <= 4:
        report_limit = 7000
    elif n <= 8:
        report_limit = 5000
    else:
        report_limit = 3200
    summaries = []
    for i, p in enumerate(papers_data, 1):
        report = (p.get('detailed_report') or '')[:report_limit]
        summaries.append(
            f"论文{i}｜{p['title']}（{p['category']}）\n"
            f"  单篇全文精读报告：\n{report}"
        )

    # 组合列表（显式编号，LLM 必须按顺序逐一处理）
    combo_lines = []
    for idx, combo in enumerate(combinations, 1):
        tag = "【全集】" if len(combo) == n else f"【{len(combo)}篇】"
        nums = "+".join(f"论文{i}" for i in combo)
        combo_lines.append(f"  {idx}. {tag} [{', '.join(map(str, combo))}] -> {nums}")

    k = len(combinations)
    divergence_note = f"\n注意：{divergence_warning}\n" if divergence_warning else ""
    topic_note = ""
    if research_topic:
        topic_note = (
            f"\n用户预设研究方向/主题：{research_topic}\n"
            "请以该主题为主线整合论文，但不要机械复述主题；需要结合论文内容提出可执行的新课题。\n"
        )

    system_prompt = (
        "你是结构生物学、CADD（计算机辅助药物设计）与细胞生物学领域的资深研究顾问，专注于：\n"
        "蛋白质结构解析（X射线晶体学/cryo-EM/NMR）、分子对接与虚拟筛选、药效团建模与QSAR、"
        "分子动力学模拟与结合自由能计算、细胞信号通路与基因表达调控、细胞功能实验与成像分析。\n\n"
        "【课题命名要求】direction_name 字段必须基于 LLM 对论文内容的深度理解独立命名，" 
        "禁止使用机械编号（如“论文1+2+3”或“组合A”），"
        "每个课题名应是对研究方向的精准概括（15字以内），体现出该组合论文间的独特交叉价值。\n\n"
        f"任务：对下方给出的 {k} 个论文组合槽位**逐一**分析，判断每个槽位是否存在"
        "有价值的交叉研究机会，若存在则提出一个具体新课题。相同 combination 可能重复出现，"
        "重复出现时必须提出不同的课题方向、科学问题或验证路径。\n\n"
        "强制规则：\n"
        "- 第一个槽位为全集组合（所有选中论文），必须生成 has_value=true 的课题建议\n"
        f"- 输出恰好 {k} 个 JSON 条目，与组合列表一一对应，顺序不变\n"
        f"- 至少给出 {max(6, n + 2)} 条 has_value=true 的课题建议（当前 {n} 篇论文→至少 {max(6, n + 2)} 条）；其中全集1条+至少 {max(5, n + 1)} 条非全集组合\n"
        "- 全集组合（槽位1）必须给出课题建议，在此基础上再提供子集组合建议\n"
        "- 相同 combination 可以产生多条不同建议，但 direction_name、scientific_rationale、methodology 必须明显不同\n"
        "- has_value=true 时填写所有字段；has_value=false 时其余字段可为空字符串\n"
        "- methodology 中用『论文N』标注每项技术的来源\n"
        "- scientific_rationale（科学依据）必须详细展开：说明每篇论文的具体贡献、彼此间的逻辑关联、"
        "整合后产生的新科学价值，不少于150字；不得用“组合了这些论文”等空泛表述\n"
        "- methodology（研究方法）必须分步骤详细阐述：每步包含具体技术路线、数据需求、评价指标，"
        "并明确标注每项技术来自哪篇论文（论文N），不少于200字\n"
        "- key_challenges（关键挑战）必须识别至少3个具体挑战，每个挑战附带可行的突破路径，不少于150字\n"
        "- research_value_score（1-5）综合评估科学意义、创新性、可行性\n"
        "- feasibility_score（1-5）单独评估工程可行性\n"
        "- 不得提出已在上述论文中完成的研究\n"
        "- 只输出 JSON 数组，禁止任何额外文字和 markdown 代码块"
    )

    user_prompt = (
        f"{divergence_note}"
        f"{topic_note}"
        f"以下 {n} 篇论文材料是前序并发 LLM 对每篇 PDF 全文分块精读后生成的单篇详细报告，并融合了系统预先分析的主要方法、创新点、摘要和关键词。请基于这些单篇报告进行跨文献整合。\n\n"
        + "\n\n".join(summaries)
        + f"\n\n请对以下 {k} 个组合逐一输出 JSON 条目（顺序必须与下方列表一致）：\n\n"
        + "\n".join(combo_lines)
        + "\n\n输出格式（JSON 数组，恰好 "
        + str(k)
        + " 个条目）：\n"
        + '[{"id":1,"combination":[1,2,3,4],"has_value":true,'
          '"direction_name":"精准学术课题名（15字内，如"多靶点深度学习筛选框架优化"）",'
          '"scientific_rationale":"科学依据（≥150字），说明每篇论文的具体贡献和交叉价值",'
          '"methodology":"研究方法（≥200字），分步骤并标注论文N来源",'
          '"key_challenges":"关键挑战（≥150字），至少3个具体挑战及突破路径",'
          '"feasibility_score":4,'
          '"feasibility_note":"数据/工具/算力可获取性",'
          '"hotspot_alignment":"与当前或未来热点的对齐",'
          '"expected_contribution":"预期贡献与适合期刊",'
          '"research_value_score":4}]'
    )
    return system_prompt, user_prompt


def normalize_combination(combo, n):
    """将 LLM 返回的组合字段统一成 1..n 范围内的有序整数列表。"""
    if not combo:
        return []
    values = []
    if isinstance(combo, str):
        values = re.findall(r'\d+', combo)
    elif isinstance(combo, (list, tuple, set)):
        for item in combo:
            if isinstance(item, int):
                values.append(item)
            elif isinstance(item, str):
                values.extend(re.findall(r'\d+', item))
    normalized = []
    for value in values:
        try:
            num = int(value)
        except (TypeError, ValueError):
            continue
        if 1 <= num <= n and num not in normalized:
            normalized.append(num)
    return sorted(normalized)


def build_fallback_suggestion(papers_data, combo, idx, variant=1, research_topic=""):
    """在 LLM 输出不足时，用论文元数据生成兜底建议，保证组合覆盖约束。"""
    selected = [(i, papers_data[i - 1]) for i in combo if 1 <= i <= len(papers_data)]
    categories = "、".join(sorted({p.get('category', '未分类') for _, p in selected}))
    methods = "；".join(
        f"论文{i}：{(p.get('methods') or '未记录')[:80]}"
        for i, p in selected
    )
    innovations = "；".join(
        f"论文{i}：{(p.get('innovations') or p.get('abstract') or '待挖掘')[:80]}"
        for i, p in selected
    )
    focus_options = ["机制验证", "模型迁移", "数据闭环", "多任务评估"]
    focus = focus_options[(variant - 1) % len(focus_options)]
    topic = (research_topic or "").strip()
    # 基于论文标题关键词和分类生成有意义的课题名
    cats = list({p.get('category', '') for _, p in selected if p.get('category')})
    cat_key = cats[0] if cats else "交叉研究"
    # 从论文标题中提取核心关键词作为命名素材
    title_words = []
    for _, p in selected:
        t = (p.get('title') or '').strip()
        # 提取有意义的英文缩写或中文关键词
        words = re.findall(r'[A-Z]{2,}|[一-鿿]{2,4}', t)
        title_words.extend(words[:2])
    # 取最频繁的关键词
    if title_words:
        from collections import Counter
        top_word = Counter(title_words).most_common(1)[0][0][:6]
    else:
        top_word = cat_key[:4]
    if topic:
        direction_name = f"{topic[:5]}-{top_word}{focus}"[:20]
    else:
        direction_name = f"{top_word}{focus}"[:20]

    return {
        "id": idx,
        "combination": combo,
        "papers_used": combo,
        "has_value": True,
        "direction_name": direction_name,
        "scientific_rationale": (
            f"该建议整合论文组合 {combo}，覆盖 {categories}。"
            f"可从创新点互补处形成新问题：{innovations}"
        ),
        "methodology": (
            f"1）梳理组合论文的可复用技术：{methods}；"
            f"2）围绕{topic or '共同科学问题'}设计{focus}实验；"
            "3）用独立数据集或外部基准验证跨论文整合后的增益。"
        ),
        "key_challenges": "核心挑战在于不同论文的数据定义、评价指标和模型假设不一致，需要统一任务表述并设计可复现实验。",
        "feasibility_score": 3,
        "feasibility_note": "基于已有论文方法和公开数据可先做原型验证，后续再补充湿实验或更大规模计算验证。",
        "hotspot_alignment": "与结构生物学-计算化学-细胞生物学交叉研究趋势一致，覆盖从原子结构到细胞表型的多尺度研究。",
        "expected_contribution": "预期形成可复用的交叉研究框架，并产出适合方法学或应用型期刊投稿的结果。",
        "research_value_score": 3
    }


def ensure_suggestion_coverage(suggestions, papers_data, combinations, warning=None, research_topic=""):
    """硬性保证课题建议不是单条全集建议，并补足多条组合建议。"""
    n = len(papers_data)
    full = tuple(range(1, n + 1))
    cleaned = []

    for item in suggestions or []:
        if not isinstance(item, dict) or not item.get('has_value', True):
            continue
        name = (item.get('direction_name') or '').strip()
        if not name or name.lower() == 'null' or name.startswith('（JSON解析'):
            continue
        combo = normalize_combination(item.get('combination') or item.get('papers_used'), n)
        if len(combo) < 2:
            continue
        item = dict(item)
        item['combination'] = combo
        item.setdefault('papers_used', combo)
        cleaned.append(item)

    def non_full_count(items):
        return sum(1 for s in items if tuple(s.get('combination', [])) != full)

    # 根据论文数量动态设定最低建议数：4篇→6条，5篇→7条，以此类推
    target_min = max(6, n + 2)
    added = 0
    candidate_combos = [normalize_combination(c, n) for c in combinations]
    candidate_combos = [c for c in candidate_combos if len(c) >= 2]
    # 全集和非全集都保留，全集优先排在前面
    if n >= 3:
        candidate_combos = [c for c in candidate_combos if tuple(c) == full] + [
            c for c in candidate_combos if tuple(c) != full
        ]
    if not candidate_combos:
        candidate_combos = [list(full)]

    attempts = 0
    combo_index = 0
    while attempts < 80:
        attempts += 1
        needs_more = len(cleaned) < target_min
        needs_non_full = n >= 3 and non_full_count(cleaned) < max(5, n + 1)
        if not (needs_more or needs_non_full):
            break

        combo = list(candidate_combos[combo_index % len(candidate_combos)])
        combo_index += 1
        if n >= 3 and needs_non_full and tuple(combo) == full:
            continue
        variant = 1 + sum(1 for s in cleaned if tuple(s.get('combination', [])) == tuple(combo))
        cleaned.append(build_fallback_suggestion(
            papers_data, combo, len(cleaned) + 1, variant, research_topic
        ))
        added += 1

    # 修复空泛或机械的课题名
    for s in cleaned:
        name = (s.get('direction_name') or '').strip()
        if not name or name.startswith('论文') or name.startswith('组合') or len(name) < 3:
            combo = s.get('combination', [])
            cats = list({papers_data[i-1].get('category', '') for i in combo if 1 <= i <= len(papers_data)})
            cat_key = cats[0][:6] if cats else "交叉研究"
            s['direction_name'] = f"{cat_key}整合研究"[:20]

    cleaned.sort(
        key=lambda x: (
            x.get('research_value_score', 0),
            x.get('feasibility_score', 0)
        ),
        reverse=True
    )
    if added:
        extra = f" 已自动补足 {added} 条组合建议以满足多组合约束。"
        warning = (warning or "") + extra
    return cleaned, warning


def parse_combination_response(raw_text, papers_data, combinations, research_topic=""):
    """解析批量组合响应：过滤无价值条目，并强制补足多组合建议。"""
    data, warning = parse_suggestion_response(raw_text)
    return ensure_suggestion_coverage(
        data or [], papers_data, combinations, warning, research_topic
    )


def build_suggestion_prompt(papers_data, n_suggestions, divergence_warning=""):
    """构建课题建议的 system_prompt 和 user_prompt（保留兼容，内部调用新函数）"""
    n = len(papers_data)
    paper_ids_str = "、".join([f"论文{i}" for i in range(1, n + 1)])

    system_prompt = f"""你是结构生物学、CADD（计算机辅助药物设计）与细胞生物学领域的资深研究顾问，专注于以下方向：
蛋白质结构解析（X射线晶体学/cryo-EM/NMR）、分子对接与虚拟筛选、药效团建模与QSAR、
分子动力学模拟与结合自由能计算、细胞信号通路与基因表达调控、细胞功能实验与成像分析。

你的任务：基于研究人员选择的 {n} 篇论文（{paper_ids_str}），通过发现技术互补性、研究空白和方法迁移机会，提出原创性新研究课题。

【强制性输出规则，违反则答案无效】
- 必须输出恰好 {n_suggestions} 个课题建议，不得多也不得少
- 第 1 个课题必须整合所有 {n} 篇论文（papers_used 字段填写全部论文编号）
- 其余课题覆盖不同的论文子集（每个至少整合 2 篇），所有论文编号至少各出现一次
- papers_used 字段列出该课题实际用到的论文编号列表，如 [1, 3]
- methodology 中用"论文N"明确标注每项技术的来源论文
- feasibility_score 为 1-5 整数（5 最高）
- 不得提出已在上述论文中完成的研究
- 只输出 JSON 数组，禁止任何额外文字和 markdown 代码块"""

    parts = []
    for i, p in enumerate(papers_data, 1):
        parts.append(
            f"【论文 {i}】\n"
            f"标题：{p['title']}\n"
            f"分类：{p['category']}\n"
            f"创新点：{p['innovations']}\n"
            f"研究方法：{p['methods']}\n"
            f"摘要节选：{p['abstract']}\n"
            f"关键词：{p['keywords']}"
        )

    papers_block = "\n\n".join(parts)
    divergence_note = f"{divergence_warning}\n\n" if divergence_warning else ""

    # 为 user_prompt 构造论文编号覆盖说明
    if n <= 4:
        coverage_hint = f"（第1条覆盖论文1-{n}；第2-{n_suggestions}条分别以不同的2-3篇组合为主）"
    else:
        coverage_hint = f"（第1条覆盖全部{n}篇；其余各条覆盖至少2篇，且每篇论文至少出现在1条建议中）"

    user_prompt = (
        f"{divergence_note}"
        f"以下是研究人员选择的 {n} 篇论文：\n\n"
        f"{papers_block}\n\n"
        f"请严格按照系统规则，输出 {n_suggestions} 个课题建议 {coverage_hint}。\n\n"
        f"JSON数组格式（每个对象包含以下字段）：\n"
        f'[{{'
        f'"id":1,'
        f'"direction_name":"课题名称（20字以内）",'
        f'"papers_used":[1,2,3],'
        f'"scientific_rationale":"科学依据，说明为何整合这几篇论文能产生新价值",'
        f'"methodology":"具体研究方法（分步骤，每步标注来自论文N的哪种技术）",'
        f'"key_challenges":"核心挑战及可能的突破路径",'
        f'"feasibility_score":4,'
        f'"feasibility_note":"可行性说明（数据/工具/算力可获取性）",'
        f'"hotspot_alignment":"与当前或未来研究热点的对齐情况",'
        f'"expected_contribution":"预期科学贡献及适合投稿的期刊/会议"'
        f'}}]'
    )
    return system_prompt, user_prompt


def _extract_balanced(text, open_ch, close_ch):
    """从 text 中提取第一个括号平衡的 JSON 片段（正确处理字符串内的括号）"""
    start = text.find(open_ch)
    if start == -1:
        return None
    depth = 0
    in_str = False
    escape = False
    for i, ch in enumerate(text[start:], start):
        if escape:
            escape = False
            continue
        if ch == '\\' and in_str:
            escape = True
            continue
        if ch == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    return None


def parse_suggestion_response(raw_text):
    """解析LLM返回的课题建议JSON，含三级fallback"""
    if not raw_text:
        return None, "LLM返回空响应"

    # 清除文本中所有 markdown 代码块标记（不只限于开头/结尾）
    text = re.sub(r'```(?:json)?\s*', '', raw_text).strip()

    # Level 1: 直接解析整段文本
    try:
        data = json.loads(text)
        if isinstance(data, list) and data:
            return data, None
        if isinstance(data, dict):
            return [data], None
    except json.JSONDecodeError:
        pass

    # Level 2: 括号计数提取 JSON 数组（避免贪婪正则越界）
    snippet = _extract_balanced(text, '[', ']')
    if snippet:
        try:
            data = json.loads(snippet)
            if isinstance(data, list) and data:
                return data, None
        except json.JSONDecodeError:
            pass

    # Level 3: 括号计数提取单个 JSON 对象并包装为数组
    snippet = _extract_balanced(text, '{', '}')
    if snippet:
        try:
            data = json.loads(snippet)
            if isinstance(data, dict):
                return [data], None
        except json.JSONDecodeError:
            pass

    # 降级：将原始文本包装为单条建议
    return [{
        "id": 1,
        "direction_name": "（JSON解析失败，请查看原始输出）",
        "scientific_rationale": raw_text[:3000],
        "methodology": "",
        "key_challenges": "",
        "feasibility_score": 0,
        "feasibility_note": "",
        "hotspot_alignment": "",
        "expected_contribution": ""
    }], "JSON解析失败，已降级展示原始文本"


def generate_research_suggestions(paper_ids, research_topic=""):
    """
    主入口：并发生成单篇全文精读报告 → 生成组合槽位 → LLM 逐一判断并生成课题 → 按研究价值排序返回。
    返回 (suggestions_list, warning_msg)。
    """
    if len(paper_ids) < 2:
        return None, "至少需要选择2篇论文"

    papers_data = fetch_papers_for_suggestion(paper_ids)
    if len(papers_data) < 2:
        return None, "有效论文不足2篇（部分ID在数据库中未找到或字段为空）"

    papers_data = enrich_papers_with_detailed_reports(papers_data, research_topic)
    divergence_warning = detect_domain_divergence(papers_data)
    n = len(papers_data)

    # 程序穷举所有组合（全集 + 子集，总数≤20）
    combinations = get_paper_combinations(n)

    # token 预算：每个组合约 500 tokens 输出，加 1000 余量
    max_tokens = min(len(combinations) * 550 + 1000, 8000)

    system_prompt, user_prompt = build_combination_prompt(
        papers_data, combinations, divergence_warning, research_topic
    )

    raw_text, error = call_llm(system_prompt, user_prompt, max_tokens=max_tokens, temperature=0.7, timeout=120)
    if error:
        return None, f"API调用失败：{error}"

    suggestions, parse_warning = parse_combination_response(
        raw_text, papers_data, combinations, research_topic
    )
    return suggestions, parse_warning


class ResearchSuggestionsDialog(tk.Toplevel):
    """课题建议结果展示弹窗"""

    SCORE_COLORS = {5: '#1a7a1a', 4: '#2e7d32', 3: '#e65100',
                    2: '#c62828', 1: '#b71c1c', 0: '#757575'}

    def __init__(self, parent, paper_ids, research_topic=""):
        super().__init__(parent)
        self.research_topic = (research_topic or "").strip()
        title_suffix = f"｜主题：{self.research_topic[:18]}" if self.research_topic else ""
        self.title(f"课题建议 — 基于 {len(paper_ids)} 篇论文{title_suffix}")
        self.geometry("920x720")
        self.resizable(True, True)
        self.paper_ids = paper_ids
        self.suggestions = []

        # 顶部状态栏
        status_frame = ttk.Frame(self, padding=(10, 8, 10, 4))
        status_frame.pack(fill=tk.X)
        self.status_label = ttk.Label(
            status_frame,
            text=f"正在并发精读 {len(paper_ids)} 篇论文全文并生成课题建议，请稍候...",
            foreground='blue'
        )
        self.status_label.pack(side=tk.LEFT)
        self.progress_bar = ttk.Progressbar(
            status_frame, mode='indeterminate', length=160
        )
        self.progress_bar.pack(side=tk.LEFT, padx=10)
        self.progress_bar.start(10)

        # Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)

        # Tab 1：课题卡片（滚动）
        cards_outer = ttk.Frame(self.notebook)
        self.notebook.add(cards_outer, text="课题建议")

        self.canvas = tk.Canvas(cards_outer, highlightthickness=0)
        vsb = ttk.Scrollbar(cards_outer, orient=tk.VERTICAL, command=self.canvas.yview)
        self.cards_inner = ttk.Frame(self.canvas)

        self._cwin = self.canvas.create_window((0, 0), window=self.cards_inner, anchor=tk.NW)
        self.canvas.configure(yscrollcommand=vsb.set)
        self.cards_inner.bind(
            '<Configure>',
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind(
            '<Configure>',
            lambda e: self.canvas.itemconfig(self._cwin, width=e.width)
        )
        self.canvas.bind_all(
            '<MouseWheel>',
            lambda e: self.canvas.yview_scroll(-1 * (e.delta // 120), 'units')
        )
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Tab 2：原始输出
        raw_frame = ttk.Frame(self.notebook)
        self.notebook.add(raw_frame, text="原始输出")
        self.raw_text = scrolledtext.ScrolledText(raw_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.raw_text.pack(fill=tk.BOTH, expand=True)

        # 底部按钮
        btn_frame = ttk.Frame(self, padding=(10, 4, 10, 8))
        btn_frame.pack(fill=tk.X)
        ttk.Button(btn_frame, text="复制全部建议", command=self._copy_all).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="导出 Markdown", command=self._export_md).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="关闭", command=self.destroy).pack(side=tk.RIGHT, padx=4)

        # 后台线程调用LLM
        threading.Thread(target=self._run_analysis, daemon=True).start()

    def _run_analysis(self):
        suggestions, error = generate_research_suggestions(
            self.paper_ids, self.research_topic
        )
        self.after(0, lambda: self._on_done(suggestions, error))

    def _on_done(self, suggestions, error):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()

        if error and not suggestions:
            self.status_label.config(text=f"分析失败：{error}", foreground='red')
            return

        if error:
            self.status_label.config(
                text=f"完成（{error}）", foreground='orange'
            )
        else:
            n_total = len(self.paper_ids)
            n_valid = len(suggestions)
            n_combos = len(get_paper_combinations(n_total))
            self.status_label.config(
                text=f"分析完成：{len(self.paper_ids)} 篇单篇精读报告 + {n_combos} 个组合 → {n_valid} 条有价值建议（按研究价值排序）",
                foreground='green'
            )

        self.suggestions = suggestions or []
        self._render_cards(self.suggestions)
        self._show_raw(self.suggestions)

    def _render_cards(self, suggestions):
        bg = self.cget('background')
        fields = [
            ("科学依据", 'scientific_rationale'),
            ("研究方法", 'methodology'),
            ("关键挑战", 'key_challenges'),
            ("可行性",   'feasibility_note'),
            ("热点对齐", 'hotspot_alignment'),
            ("预期贡献", 'expected_contribution'),
        ]
        for i, s in enumerate(suggestions, 1):
            f_score = s.get('feasibility_score', 0)
            v_score = s.get('research_value_score', f_score)
            color = self.SCORE_COLORS.get(f_score, '#757575')
            v_color = self.SCORE_COLORS.get(v_score, '#757575')
            name = s.get('direction_name', '（无标题）')

            card = ttk.LabelFrame(
                self.cards_inner,
                text=f"  #{i}  {name}",
                padding=8
            )
            card.pack(fill=tk.X, padx=8, pady=6)

            # 徽章行：论文组合 ＋ 研究价值 ＋ 工程可行性
            badge_frame = tk.Frame(card, bg=bg)
            badge_frame.pack(anchor=tk.W, fill=tk.X, pady=(0, 4))

            combo = s.get('combination') or s.get('papers_used', [])
            if combo:
                papers_str = "、".join([f"论文{p}" for p in combo])
                tk.Label(
                    badge_frame,
                    text=f"论文组合：{papers_str}",
                    foreground='#1565c0',
                    font=('', 9, 'bold'),
                    bg=bg
                ).pack(side=tk.LEFT, padx=(0, 18))

            v_stars = '★' * v_score + '☆' * (5 - v_score) if v_score > 0 else '—'
            tk.Label(
                badge_frame,
                text=f"研究价值：{v_stars} ({v_score}/5)",
                foreground=v_color,
                font=('', 9, 'bold'),
                bg=bg
            ).pack(side=tk.LEFT, padx=(0, 14))

            f_stars = '★' * f_score + '☆' * (5 - f_score) if f_score > 0 else '—'
            tk.Label(
                badge_frame,
                text=f"可行性：{f_stars} ({f_score}/5)",
                foreground=color,
                font=('', 9),
                bg=bg
            ).pack(side=tk.LEFT)

            for label, key in fields:
                value = (s.get(key) or '').strip()
                if not value:
                    continue
                row = ttk.Frame(card)
                row.pack(fill=tk.X, pady=2)
                ttk.Label(
                    row, text=f"{label}：",
                    font=('', 9, 'bold'), width=8, anchor=tk.NE
                ).pack(side=tk.LEFT, anchor=tk.N, padx=(0, 4))
                # 使用 ScrolledText 保证长内容完整可见且可滚动
                lines = max(3, value.count('\n') + 1, len(value) // 60 + 1)
                lines = min(lines, 12)  # 初始显示最多12行，超出可滚动
                t = scrolledtext.ScrolledText(
                    row, wrap=tk.WORD, height=lines,
                    font=('', 9), relief=tk.FLAT, bg=bg
                )
                t.insert(tk.END, value)
                t.config(state=tk.DISABLED)
                t.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def _show_raw(self, suggestions):
        raw = json.dumps(suggestions, ensure_ascii=False, indent=2)
        self.raw_text.config(state=tk.NORMAL)
        self.raw_text.delete(1.0, tk.END)
        self.raw_text.insert(1.0, raw)
        self.raw_text.config(state=tk.DISABLED)

    def _copy_all(self):
        if not self.suggestions:
            messagebox.showinfo("提示", "暂无内容可复制", parent=self)
            return
        lines = []
        for s in self.suggestions:
            lines.append(f"【{s.get('direction_name', '')}】")
            for k, v in s.items():
                if k not in ('id', 'direction_name', 'feasibility_score') and v:
                    lines.append(f"  {k}: {v}")
            lines.append("")
        self.clipboard_clear()
        self.clipboard_append("\n".join(lines))
        messagebox.showinfo("已复制", "已将所有建议复制到剪贴板", parent=self)

    def _export_md(self):
        if not self.suggestions:
            messagebox.showinfo("提示", "暂无内容可导出", parent=self)
            return
        path = filedialog.asksaveasfilename(
            parent=self,
            defaultextension=".md",
            filetypes=[("Markdown", "*.md"), ("文本", "*.txt")],
            title="导出课题建议"
        )
        if not path:
            return
        lines = [f"# 课题建议报告",
                 f"\n生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}  ",
                 f"基于 {len(self.paper_ids)} 篇论文\n"]
        for i, s in enumerate(self.suggestions, 1):
            lines.append(f"## #{i} {s.get('direction_name', '')}\n")
            combo = s.get('combination') or s.get('papers_used', [])
            papers_str = "、".join(f"论文{p}" for p in combo)
            lines.append(f"**论文组合：** {papers_str}  ")
            lines.append(f"**研究价值：** {s.get('research_value_score', '-')}/5  ")
            lines.append(f"**工程可行性：** {s.get('feasibility_score', '-')}/5\n")
            for label, key in [("科学依据", "scientific_rationale"),
                               ("研究方法", "methodology"),
                               ("关键挑战", "key_challenges"),
                               ("可行性说明", "feasibility_note"),
                               ("热点对齐", "hotspot_alignment"),
                               ("预期贡献", "expected_contribution")]:
                val = (s.get(key) or '').strip()
                if val:
                    lines.append(f"**{label}：**\n\n{val}\n")
            lines.append("---\n")
        with open(path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        messagebox.showinfo("完成", f"已导出到：\n{path}", parent=self)


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

def is_bad_abstract(abstract, title=""):
    """判断提取的摘要质量是否可疑"""
    if not abstract:
        return True
    if len(abstract) < 50:
        return True
    if title and abstract.strip().lower() == title.strip().lower():
        return True
    return False

# ============ 去重检测 ============
def check_duplicate(file_path):
    """检测文献是否已存在。返回 (is_duplicate, reason, existing_id)"""
    filename = os.path.basename(file_path)

    conn = get_db_conn()
    c = conn.cursor()

    # 检测1：文件名重复（存储路径末尾含原始文件名）
    c.execute("SELECT id FROM papers WHERE file_path LIKE ?", (f'%{filename}',))
    row = c.fetchone()
    if row:
        conn.close()
        return True, f"文件名重复: {filename}", row[0]

    # 检测2：标题重复（SQL 大小写不敏感精确匹配）
    try:
        with fitz.open(file_path) as doc:
            metadata = doc.metadata
            text = ""
            for i in range(min(2, len(doc))):
                text += doc.load_page(i).get_text() + "\n"

        title = (metadata.get('title', '') or extract_title_from_text(text) or
                 filename.replace('.pdf', '')).strip()

        if title and len(title) > 5:
            c.execute('SELECT id FROM papers WHERE lower(title) = lower(?)', (title,))
            row = c.fetchone()
            if row:
                conn.close()
                return True, f"标题重复: '{title}'", row[0]
    except Exception:
        pass

    conn.close()
    return False, "", None

# ============ 数据库操作 ============
def add_paper_to_db(file_path, tags='', force=False):
    """添加文献到数据库，自动解析全部信息（增强版）

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

    try:
        # 提取PDF元数据
        with fitz.open(dest_path) as doc:
            metadata = doc.metadata

        # 提取文本（前5页足够覆盖标题+摘要+关键词）
        full_text = extract_text_from_pdf(dest_path)

        # ── 第1轮: 正则/PDF元数据提取 ──────────────────────────────
        title = (metadata.get('title') or '').strip()
        if not title or len(title) < 5 or title == 'Unknown Title':
            title = extract_title_from_text(full_text) or filename.replace('.pdf', '')

        abstract = extract_abstract(full_text)
        keywords = extract_keywords(full_text)

        # 作者: 正则优先于PDF元数据（PDF metadata的author字段常为空或乱码）
        authors_pdf_meta = (metadata.get('author') or '').strip()
        authors_regex = extract_authors_from_text(full_text)

        # 只使用有意义的作者信息（排除乱码和纯机构名）
        # 已知的非作者关键词（期刊编辑、摘要标记、出版商标识等）
        _NON_AUTHOR_PATTERNS = [
            r'(?i)\bassociate\s+editor\b',
            r'(?i)\bacademic\s+editor\b',
            r'(?i)\beditor[:\s]',
            r'(?i)\bmotivation\b',
            r'(?i)\bview\s+citing\b',
            r'(?i)\bcrossmark\b',
            r'(?i)\bfull\s+terms\b',
            r'(?i)\bconditions\s+of\s+access\b',
            r'\bMDPI\b',
            r'\bAdministrator\b',
            r'(?i)\battention\s+mechanism',
            r'(?i)\bdiffusion[-\s]based\b',
            r'(?i)\bdrug[-\s]target\b.*\binteraction\b.*\bprediction\b',
        ]

        def _is_valid_author_string(s):
            if not s or len(s) < 3:
                return False
            # 排除期刊编辑/摘要标记/出版商标识等误识别
            for pat in _NON_AUTHOR_PATTERNS:
                if re.search(pat, s):
                    return False
            # 排除纯机构字符串（不含任何大写字母开头的姓名单元）
            if not re.search(r'[A-Z][a-z]', s) and not re.search(r'[\u4e00-\u9fff]{2,}', s):
                return False
            # 排除国家名（完全匹配或以国家名结尾的地点行）
            s_upper = s.rstrip('.;, ').upper()
            if s_upper in COUNTRY_NAMES:
                return False
            if any(s_upper.endswith(cn) for cn in COUNTRY_NAMES if len(cn) > 2):
                return False
            # 排除整串像标题的（含3+个连续大写词且长度>40）
            words = s.split()
            title_like = sum(1 for w in words if w and w[0].isupper() and len(w) > 4)
            if title_like >= 4 and len(s) > 40 and ',' not in s:
                return False
            # 排除单单词结果（如 "Review", "Article"）——至少含逗号或含2+个姓名单元
            if ',' not in s and ';' not in s and ' and ' not in s.lower() and '&' not in s:
                # 单个姓名必须包含空格（如 "John Smith"）
                if ' ' not in s:
                    return False
                # 单个全名但无分隔符，也要验证像人名
                name_parts = [w for w in words if w and not w.startswith('(')]
                if len(name_parts) < 2:
                    return False
            return True

        if _is_valid_author_string(authors_regex):
            authors = authors_regex
        elif _is_valid_author_string(authors_pdf_meta):
            authors = authors_pdf_meta
        else:
            authors = ''

        doi = extract_doi_from_text(full_text)
        year = extract_year_from_metadata(metadata) or extract_year_from_text(full_text)

        # ── 第2轮: LLM分析（覆盖标题/摘要/作者/分类/方法等）──────
        categories = get_categories()
        analysis = None

        if LLM_API_KEY:
            analysis = llm_full_analysis(full_text, filename, keywords, categories)

            # 标题: LLM结果优先（更准确）
            if analysis.get('title') and len(analysis['title']) > 5:
                title = analysis['title']

            # 摘要: LLM结果优先
            if analysis.get('abstract') and len(analysis['abstract']) > 50:
                abstract = analysis['abstract']

            # 年份: LLM结果优先
            if analysis.get('year'):
                year = analysis['year']

            # 作者: LLM结果优先于正则（Prompt已强化区分作者/机构）
            llm_authors = (analysis.get('authors') or '').strip()
            if _is_valid_author_string(llm_authors):
                authors = llm_authors

            # DOI: 从LLM分析结果中获取
            llm_doi = (analysis.get('doi') or '').strip()
            if llm_doi and not doi:
                doi = llm_doi

        if not analysis:
            analysis = {"category": "未分类", "methods": "", "innovations": "", "keywords_enhanced": ""}

        # ── 第3轮: CrossRef在线补全（兜底）────
        # 触发条件: 缺DOI 或 缺作者 或 缺年份 或 作者可能不完整
        def _count_authors(s):
            """估算作者数量"""
            if not s:
                return 0
            return max(s.count(',') + 1, s.count(';') + 1, s.count(' and ') + 1)
        
        authors_sparse = not authors or _count_authors(authors) <= 2
        need_crossref = not doi or not authors or not year or authors_sparse
        
        if need_crossref:
            query_title = title[:200] if title else ''
            if query_title and len(query_title) > 10:
                cr_result = lookup_crossref(query_title, timeout=10)
                if cr_result:
                    if not doi and cr_result.get('doi'):
                        doi = cr_result['doi']
                    # CrossRef作者更完整时优先使用
                    cr_authors = cr_result.get('authors', '')
                    if cr_authors:
                        if not authors:
                            if _is_valid_author_string(cr_authors):
                                authors = cr_authors
                        elif _count_authors(cr_authors) > _count_authors(authors):
                            if _is_valid_author_string(cr_authors):
                                authors = cr_authors
                    if not year and cr_result.get('year'):
                        year = cr_result['year']

        # ── 最终安全网: 作者字段再检查 ──────────────────────────────
        if authors:
            # 单个全大写单词（如 "JAPAN"）不是有效作者
            authors_stripped = authors.rstrip('.;, ').strip()
            if authors_stripped.isupper() and ' ' not in authors_stripped and ',' not in authors_stripped:
                authors = ''
            # 纯国家名
            elif authors_stripped.upper() in COUNTRY_NAMES:
                authors = ''

        # ── 合并关键词 ──────────────────────────────────────────
        all_keywords = keywords
        if analysis.get('keywords_enhanced'):
            all_keywords = f"{keywords}; {analysis['keywords_enhanced']}" if keywords else analysis['keywords_enhanced']

        # ── 获取页数 ────────────────────────────────────────────
        page_count = 0
        try:
            with fitz.open(dest_path) as doc_pc:
                page_count = len(doc_pc)
        except Exception:
            pass

        # ── 写入数据库 ─────────────────────────────────────────
        conn = get_db_conn()
        c = conn.cursor()
        c.execute('INSERT INTO papers (title, authors, abstract, keywords, doi, year, file_path, page_count, added_date, tags, category, methods, innovations) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (title, authors, abstract, all_keywords, doi, year, dest_path,
             page_count, datetime.now().isoformat(), tags,
             analysis.get('category', '未分类'),
             analysis.get('methods', ''),
             analysis.get('innovations', '')))
        conn.commit()
        paper_id = c.lastrowid
        conn.close()

        return paper_id, analysis

    except Exception:
        try:
            os.remove(dest_path)
        except OSError:
            pass
        raise

# ============ StatisticsDialog ============
class StatisticsDialog(tk.Toplevel):
    """美化的文献库统计弹窗：带颜色进度条、按分类/年份可视化。"""

    _CAT_PALETTE = [
        "#4f7ce8", "#5b86e5", "#3d6ad4", "#6b8ff0",
        "#4470cc", "#7a9bf5", "#5580e0", "#4f7ce8",
    ]
    _YEAR_PALETTE = [
        "#e05555", "#e87040", "#e8a840", "#e8c840",
        "#a0c850", "#4caf50", "#4cb870", "#4caf90",
        "#4f7ce8", "#6b8ff0", "#8f9fe0", "#b0b8e0",
    ]

    def __init__(self, parent, total, by_cat, by_year):
        super().__init__(parent)
        self.title("文献库统计")
        self.geometry("600x640")
        self.resizable(True, True)
        self.configure(bg=C["bg"])
        self._build_header(total, len(by_cat), len(by_year))
        self._build_body(total, by_cat, by_year)
        self._build_footer()
        self.grab_set()

    def _build_header(self, total, n_cat, n_year):
        hf = tk.Frame(self, bg=C["primary"])
        hf.pack(fill=tk.X)
        inner = tk.Frame(hf, bg=C["primary"])
        inner.pack(padx=24, pady=14)
        tk.Label(inner, text=str(total),
                 font=("Microsoft YaHei UI", 38, "bold"),
                 bg=C["primary"], fg="white").pack(side=tk.LEFT)
        right = tk.Frame(inner, bg=C["primary"])
        right.pack(side=tk.LEFT, padx=(10, 0))
        tk.Label(right, text="篇文献",
                 font=("Microsoft YaHei UI", 15),
                 bg=C["primary"], fg="white").pack(anchor="w", pady=(12, 0))
        tk.Label(right, text=f"{n_cat} 个分类  ·  {n_year} 个年份",
                 font=("Microsoft YaHei UI", 10),
                 bg=C["primary"], fg="#c5d8ff").pack(anchor="w")

    def _build_body(self, total, by_cat, by_year):
        outer = tk.Frame(self, bg=C["bg"])
        outer.pack(fill=tk.BOTH, expand=True)
        vsb = ttk.Scrollbar(outer, orient=tk.VERTICAL)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        canvas = tk.Canvas(outer, bg=C["bg"], highlightthickness=0,
                           yscrollcommand=vsb.set)
        vsb.config(command=canvas.yview)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        inner = tk.Frame(canvas, bg=C["bg"])
        cwin = canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>",
                   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig(cwin, width=e.width))
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))
        self._add_section(inner, "按分类分布", by_cat, total,
                          self._CAT_PALETTE, label_width=14)
        self._add_section(inner, "按年份分布", by_year, total,
                          self._YEAR_PALETTE, label_width=6)

    def _build_footer(self):
        tf = tk.Frame(self, bg=C["bg"])
        tf.pack(fill=tk.X, pady=(4, 10))
        tk.Button(tf, text="关闭", command=self.destroy,
                  bg=C["primary"], fg="white",
                  font=("Microsoft YaHei UI", 10), relief=tk.FLAT,
                  padx=28, pady=6, cursor="hand2",
                  activebackground=C["primary_hover"],
                  activeforeground="white").pack()

    def _add_section(self, parent, title, data, total, palette, label_width):
        sec = tk.Frame(parent, bg=C["bg"])
        sec.pack(fill=tk.X, padx=16, pady=(16, 4))
        tk.Label(sec, text=title,
                 font=("Microsoft YaHei UI", 11, "bold"),
                 bg=C["bg"], fg=C["text"]).pack(anchor="w")
        tk.Frame(sec, bg=C["border"], height=1).pack(fill=tk.X, pady=(4, 0))
        if not data:
            tk.Label(parent, text="暂无数据",
                     bg=C["bg"], fg=C["text_muted"]).pack(padx=16, pady=4)
            return
        max_cnt = max(cnt for _, cnt in data) or 1
        for idx, (label, count) in enumerate(data):
            color = palette[idx % len(palette)]
            pct = count / total * 100
            lbl_text = str(label or "未分类")
            if len(lbl_text) > label_width:
                lbl_text = lbl_text[:label_width - 1] + "…"
            row = tk.Frame(parent, bg=C["bg"])
            row.pack(fill=tk.X, padx=16, pady=2)
            tk.Label(row, text=lbl_text, width=label_width,
                     font=("Microsoft YaHei UI", 10),
                     bg=C["bg"], fg=C["text"], anchor="w").pack(side=tk.LEFT)
            tk.Label(row, text=f"{count:>4}",
                     font=("Microsoft YaHei UI", 10, "bold"),
                     bg=C["bg"], fg=color).pack(side=tk.LEFT, padx=(4, 8))
            bar_c = tk.Canvas(row, height=14, bg=C["card"], highlightthickness=0)
            bar_c.pack(side=tk.LEFT, fill=tk.X, expand=True)
            frac = count / max_cnt

            def redraw(event, canvas=bar_c, f=frac, cl=color):
                canvas.delete("all")
                bw = max(2, int(event.width * f))
                canvas.create_rectangle(0, 2, bw, 12, fill=cl, outline="")

            bar_c.bind("<Configure>", redraw)
            tk.Label(row, text=f"{pct:5.1f}%",
                     font=("Microsoft YaHei UI", 9),
                     bg=C["bg"], fg=C["text_muted"],
                     width=7).pack(side=tk.LEFT, padx=(6, 0))


# ============ ModelManagerDialog ============
class ModelManagerDialog(tk.Toplevel):
    """解析引擎模型管理：查看 / 添加 / 删除 / 设置 API Key。"""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.title("解析引擎管理")
        self.geometry("520x420")
        self.resizable(True, True)
        self.configure(bg=C["bg"])
        self._build()
        self.grab_set()

    def _build(self):
        hf = tk.Frame(self, bg=C["primary"])
        hf.pack(fill=tk.X)
        tk.Label(hf, text="解析引擎管理",
                 font=("Microsoft YaHei UI", 13, "bold"),
                 bg=C["primary"], fg="white").pack(padx=16, pady=11, anchor="w")
        list_frame = tk.Frame(self, bg=C["bg"])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=14, pady=10)
        vsb = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self._canvas = tk.Canvas(list_frame, bg=C["bg"],
                                 highlightthickness=0, yscrollcommand=vsb.set)
        vsb.config(command=self._canvas.yview)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._list_inner = tk.Frame(self._canvas, bg=C["bg"])
        cwin = self._canvas.create_window((0, 0), window=self._list_inner, anchor="nw")
        self._list_inner.bind(
            "<Configure>",
            lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")))
        self._canvas.bind("<Configure>",
                          lambda e: self._canvas.itemconfig(cwin, width=e.width))
        self._refresh_list()
        btn_frame = tk.Frame(self, bg=C["bg"])
        btn_frame.pack(fill=tk.X, padx=14, pady=(4, 12))
        tk.Button(btn_frame, text="＋ 添加自定义模型",
                  command=self._add_model,
                  bg=C["primary"], fg="white",
                  font=("Microsoft YaHei UI", 10), relief=tk.FLAT,
                  padx=16, pady=6, cursor="hand2",
                  activebackground=C["primary_hover"],
                  activeforeground="white").pack(side=tk.LEFT)
        tk.Button(btn_frame, text="关闭", command=self.destroy,
                  bg=C["card"], fg=C["text"],
                  font=("Microsoft YaHei UI", 10), relief=tk.FLAT,
                  padx=16, pady=6, cursor="hand2").pack(side=tk.RIGHT)

    def _refresh_list(self):
        for w in self._list_inner.winfo_children():
            w.destroy()
        for name in list(MODEL_CONFIGS.keys()):
            is_default = name in DEFAULT_MODEL_CONFIGS
            row = tk.Frame(self._list_inner, bg=C["card"],
                           highlightbackground=C["border"],
                           highlightthickness=1)
            row.pack(fill=tk.X, pady=3, ipady=2)
            badge_bg = C["border"] if is_default else C["primary"]
            badge_fg = C["text_muted"] if is_default else "white"
            tk.Label(row, text="预置" if is_default else "自定义",
                     font=("Microsoft YaHei UI", 8),
                     bg=badge_bg, fg=badge_fg,
                     padx=5, pady=2).pack(side=tk.LEFT, padx=(8, 6), pady=8)
            info = tk.Frame(row, bg=C["card"])
            info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=4)
            cfg = MODEL_CONFIGS[name]
            tk.Label(info, text=name,
                     font=("Microsoft YaHei UI", 11, "bold"),
                     bg=C["card"], fg=C["text"], anchor="w").pack(anchor="w")
            base = (cfg.get("base_url") or "")[:45]
            tk.Label(info, text=f"model={cfg.get('model', name)}  {base}",
                     font=("Microsoft YaHei UI", 8),
                     bg=C["card"], fg=C["text_muted"], anchor="w").pack(anchor="w")
            btns = tk.Frame(row, bg=C["card"])
            btns.pack(side=tk.RIGHT, padx=8, pady=8)

            def make_set_key(n=name):
                def _set():
                    key = simpledialog.askstring(
                        "API Key", f"{n} API Key（留空则不修改）：",
                        parent=self, show="*",
                        initialvalue=MODEL_CONFIGS[n].get("api_key", ""))
                    if key is not None and key.strip():
                        MODEL_CONFIGS[n]["api_key"] = key.strip()
                        save_model_configs()
                        if CURRENT_MODEL_NAME == n:
                            global LLM_API_KEY
                            LLM_API_KEY = key.strip()
                        messagebox.showinfo("完成",
                                            f"已保存 {n} 的 API Key",
                                            parent=self)
                return _set

            tk.Button(btns, text="API Key", command=make_set_key(),
                      bg=C["card"], fg=C["primary"],
                      font=("Microsoft YaHei UI", 9),
                      relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=2)

            if not is_default:
                def make_del(n=name):
                    def _del():
                        if messagebox.askyesno(
                                "确认删除",
                                f"确定删除自定义模型 '{n}'？",
                                parent=self):
                            del MODEL_CONFIGS[n]
                            refresh_available_models()
                            save_model_configs()
                            self.app.refresh_model_menu()
                            self._refresh_list()
                    return _del
                tk.Button(btns, text="删除", command=make_del(),
                          bg=C["card"], fg=C["error"],
                          font=("Microsoft YaHei UI", 9),
                          relief=tk.FLAT, cursor="hand2").pack(side=tk.LEFT, padx=2)

    def _add_model(self):
        self.app.configure_custom_model()
        self._refresh_list()


# ============ GUI ============
class LiteratureManager:
    def __init__(self, root):
        self.root = root
        self.root.title("结构/CADD/细胞生物学文献管家")
        self.root.geometry("1500x880")
        self.root.configure(fg_color=C["bg"])
        self.root.minsize(1100, 600)

        # ─── 全局网格 ───
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # ═══════ 侧边栏 ═══════
        self._build_sidebar()

        # ═══════ 主区域 ═══════
        self.main_area = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=6, pady=6)
        self.main_area.grid_rowconfigure(2, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)

        self._build_topbar()
        self._build_content()

        # ─── 模型选择菜单变量（保持兼容） ───
        self.model_var = tk.StringVar(value=CURRENT_MODEL_NAME)
        self.model_menu = None  # 菜单栏已移除，保留属性兼容

        self.current_paper_id = None
        self._category_dialog = None
        self.refresh_filter_options()
        self.refresh_list()

    # ═══════════════════ 侧边栏 ═══════════════════
    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(
            self.root, width=220, corner_radius=0,
            fg_color=C["sidebar"]
        )
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        # Logo - 简洁大字
        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_frame.pack(fill=tk.X, padx=18, pady=(22, 28))
        ctk.CTkLabel(
            logo_frame, text="StructCADD", font=("Microsoft YaHei UI", 22, "bold"),
            text_color=C["primary"]
        ).pack(anchor="w")
        ctk.CTkLabel(
            logo_frame, text="结构/CADD/细胞文献管家",
            font=("Microsoft YaHei UI", 11), text_color=C["text_muted"]
        ).pack(anchor="w", pady=(0, 0))

        # 分隔线
        self._sidebar_sep(C["border"])

        # 导航按钮 - Marvis 风格：极简，hover 微亮
        self.nav_btns = []
        nav_items = [
            ("📋  全部文献",   self._nav_all,     True),
            ("📂  分类管理",   self.manage_categories, False),
            ("📊  扫描报告",   self.open_scan_browser, False),
            ("🛠  路径修复",   self.repair_and_fill_metadata, False),
        ]
        self._nav_active_btn = None
        for label, cmd, is_active in nav_items:
            btn = ctk.CTkButton(
                sidebar, text=label, command=cmd,
                fg_color=C["sidebar_hover"] if is_active else "transparent",
                hover_color=C["sidebar_hover"],
                text_color=C["text"] if is_active else C["text_secondary"],
                font=("Microsoft YaHei UI", 12),
                anchor="w", corner_radius=6, height=36,
                border_width=0,
            )
            btn.pack(fill=tk.X, padx=10, pady=1)
            btn.bind("<Button-1>", lambda e, b=btn: self._nav_highlight(b), add="+")
            self.nav_btns.append(btn)
            if is_active:
                self._nav_active_btn = btn

        self._sidebar_sep(C["border"])

        # 解析引擎区
        ctk.CTkLabel(
            sidebar, text="解析引擎",
            font=("Microsoft YaHei UI", 10), text_color=C["text_muted"]
        ).pack(anchor="w", padx=18, pady=(12, 4))

        self._model_selector = ctk.CTkOptionMenu(
            sidebar,
            values=list(AVAILABLE_MODELS.keys()),
            command=self._on_sidebar_model_change,
            fg_color=C["sidebar_hover"], button_color=C["primary"],
            button_hover_color=C["primary_hover"],
            text_color=C["text"], font=("Microsoft YaHei UI", 11),
            dropdown_fg_color=C["surface"],
            dropdown_text_color=C["text"],
            dropdown_font=("Microsoft YaHei UI", 11),
            corner_radius=6, height=34,
        )
        self._model_selector.set(CURRENT_MODEL_NAME)
        self._model_selector.pack(fill=tk.X, padx=10, pady=2)

        self._sidebar_model_label = ctk.CTkLabel(
            sidebar, text=CURRENT_MODEL_NAME,
            font=("Microsoft YaHei UI", 9), text_color=C["text_muted"]
        )
        self._sidebar_model_label.pack(pady=(4, 0))


        ctk.CTkButton(
            sidebar, text="管理解析引擎",
            command=lambda: ModelManagerDialog(self.root, self),
            height=28, corner_radius=4,
            font=("Microsoft YaHei UI", 10),
            fg_color=C["sidebar_hover"], hover_color=C["border"],
            text_color=C["text_secondary"],
            border_width=1, border_color=C["border"]
        ).pack(fill=tk.X, padx=10, pady=(4, 0))
        spacer = ctk.CTkFrame(sidebar, fg_color="transparent")
        spacer.pack(fill=tk.BOTH, expand=True)

        # 底部
        self._sidebar_sep(C["border"])
        ctk.CTkLabel(
            sidebar,
            text="Structural Biology · CADD\nCell Biology Literature Intelligence",
            font=("Microsoft YaHei UI", 9), text_color=C["text_muted"],
            justify="center"
        ).pack(side=tk.BOTTOM, pady=14)

    def _sidebar_sep(self, color):
        """在侧边栏底部插入分隔线 - 简洁细线"""
        sidebar = self.root.winfo_children()[0]
        ctk.CTkFrame(
            sidebar, height=1, fg_color=color
        ).pack(fill=tk.X, padx=14, pady=3)

    def _nav_highlight(self, btn):
        if self._nav_active_btn:
            self._nav_active_btn.configure(
                fg_color="transparent", text_color=C["text_secondary"]
            )
        btn.configure(
            fg_color=C["sidebar_hover"], text_color=C["text"]
        )
        self._nav_active_btn = btn

    def _nav_all(self):
        self.cat_filter.set("全部")
        self.refresh_list()

    def _on_sidebar_model_change(self, value):
        self.model_var.set(value)
        self._sidebar_model_label.configure(text=f"当前: {value}")
        self.on_model_change()

    # ═══════════════════ 顶部工具栏 ═══════════════════
    def _build_topbar(self):
        # 大面积留白顶栏 - Marvis 风格
        topbar = ctk.CTkFrame(self.main_area, fg_color="transparent")
        topbar.grid(row=0, column=0, sticky="ew", pady=(4, 10))
        topbar.grid_columnconfigure(0, weight=1)

        # 搜索行
        search_row = ctk.CTkFrame(topbar, fg_color="transparent")
        search_row.grid(row=0, column=0, sticky="ew")

        # 大搜索框 - Marvis 核心交互入口
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.refresh_list())
        self._search_entry = ctk.CTkEntry(
            search_row, textvariable=self.search_var,
            placeholder_text="搜索标题、作者、摘要、结构/方法...",
            height=42,
            fg_color=C["input_bg"], border_color=C["input_border"],
            text_color=C["text"], font=("Microsoft YaHei UI", 13),
            corner_radius=8,
        )
        self._search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        # 分类筛选 - 紧凑在下
        self.cat_filter = ctk.CTkComboBox(
            search_row, values=["全部"] + get_categories(),
            command=lambda _: self.refresh_list(),
            width=130, height=42,
            fg_color=C["input_bg"], border_color=C["input_border"],
            button_color=C["primary"], button_hover_color=C["primary_hover"],
            text_color=C["text"], font=("Microsoft YaHei UI", 12),
            dropdown_fg_color=C["surface"],
            dropdown_text_color=C["text"],
            dropdown_font=("Microsoft YaHei UI", 12),
            corner_radius=8,
        )
        self.cat_filter.set("全部")
        self.cat_filter.pack(side=tk.LEFT)

        # 第二行 - 筛选 + 操作按钮
        action_row = ctk.CTkFrame(topbar, fg_color="transparent")
        action_row.grid(row=1, column=0, sticky="ew", pady=(8, 0))

        # 左侧筛选区
        filter_left = ctk.CTkFrame(action_row, fg_color="transparent")
        filter_left.pack(side=tk.LEFT)

        ctk.CTkLabel(
            filter_left, text="标签", font=("Microsoft YaHei UI", 11),
            text_color=C["text_muted"]
        ).pack(side=tk.LEFT, padx=(0, 4))
        self.tag_filter = ctk.CTkComboBox(
            filter_left, values=["全部"],
            command=lambda _: self.refresh_list(),
            width=110, height=30,
            fg_color=C["input_bg"], border_color=C["input_border"],
            button_color=C["primary"], button_hover_color=C["primary_hover"],
            text_color=C["text"], font=("Microsoft YaHei UI", 11),
            dropdown_fg_color=C["surface"],
            dropdown_text_color=C["text"],
            corner_radius=6,
        )
        self.tag_filter.set("全部")
        self.tag_filter.pack(side=tk.LEFT)

        ctk.CTkLabel(
            filter_left, text="年份", font=("Microsoft YaHei UI", 11),
            text_color=C["text_muted"]
        ).pack(side=tk.LEFT, padx=(14, 4))
        self.year_from_var = tk.StringVar()
        ctk.CTkEntry(
            filter_left, textvariable=self.year_from_var, width=52, height=30,
            placeholder_text="起始", fg_color=C["input_bg"],
            border_color=C["input_border"], text_color=C["text"],
            font=("Microsoft YaHei UI", 11), corner_radius=6,
        ).pack(side=tk.LEFT, padx=(0, 3))
        ctk.CTkLabel(
            filter_left, text="–", text_color=C["text_muted"],
            font=("Microsoft YaHei UI", 11)
        ).pack(side=tk.LEFT, padx=2)
        self.year_to_var = tk.StringVar()
        ctk.CTkEntry(
            filter_left, textvariable=self.year_to_var, width=52, height=30,
            placeholder_text="截止", fg_color=C["input_bg"],
            border_color=C["input_border"], text_color=C["text"],
            font=("Microsoft YaHei UI", 11), corner_radius=6,
        ).pack(side=tk.LEFT, padx=(3, 0))
        self.year_from_var.trace('w', lambda *_: self.refresh_list())
        self.year_to_var.trace('w', lambda *_: self.refresh_list())

        # 右侧操作按钮
        action_right = ctk.CTkFrame(action_row, fg_color="transparent")
        action_right.pack(side=tk.RIGHT)

        pill_style = {"height": 30, "font": ("Microsoft YaHei UI", 11), "corner_radius": 6}

        ctk.CTkButton(
            action_right, text="统计", command=self.show_statistics,
            fg_color=C["card"], hover_color=C["border"],
            text_color=C["text_secondary"], width=56, **pill_style
        ).pack(side=tk.RIGHT, padx=2)
        ctk.CTkButton(
            action_right, text="CSV", command=self.export_csv,
            fg_color=C["card"], hover_color=C["border"],
            text_color=C["text_secondary"], width=50, **pill_style
        ).pack(side=tk.RIGHT, padx=2)
        ctk.CTkButton(
            action_right, text="BibTeX", command=self.export_bibtex,
            fg_color=C["card"], hover_color=C["border"],
            text_color=C["text_secondary"], width=56, **pill_style
        ).pack(side=tk.RIGHT, padx=2)

        sep = ctk.CTkFrame(action_right, width=1, height=20, fg_color=C["border"])
        sep.pack(side=tk.RIGHT, padx=8)

        ctk.CTkButton(
            action_right, text="⭮ 重新分析", command=self.batch_reanalyze_papers,
            fg_color=C["warning"], hover_color="#d49420",
            text_color="#2c2c2c", width=90, **pill_style
        ).pack(side=tk.RIGHT, padx=2)

        # 第三个分隔 + 核心操作按钮
        sep2 = ctk.CTkFrame(action_right, width=1, height=20, fg_color=C["border"])
        sep2.pack(side=tk.RIGHT, padx=8)

        btn_main = {"height": 30, "font": ("Microsoft YaHei UI", 11), "corner_radius": 6, "width": 64}

        ctk.CTkButton(
            action_right, text="导入 PDF", command=self.import_pdf,
            fg_color=C["primary"], hover_color=C["primary_hover"], **btn_main
        ).pack(side=tk.RIGHT, padx=2)
        ctk.CTkButton(
            action_right, text="打开", command=self.open_pdf,
            fg_color=C["card"], hover_color=C["primary_hover"],
            text_color=C["text"], **btn_main
        ).pack(side=tk.RIGHT, padx=2)
        ctk.CTkButton(
            action_right, text="删除", command=self.delete_paper,
            fg_color="transparent", hover_color=C["error"],
            text_color=C["text_muted"], border_color=C["border"],
            border_width=1, **btn_main
        ).pack(side=tk.RIGHT, padx=2)
        ctk.CTkButton(
            action_right, text="批量删除", command=self.delete_selected_papers,
            fg_color="transparent", hover_color=C["error"],
            text_color=C["text_muted"], border_color=C["border"],
            border_width=1, **btn_main
        ).pack(side=tk.RIGHT, padx=2)

        self.suggest_btn = ctk.CTkButton(
            action_right, text="💡 课题建议", command=self.on_suggest_topics,
            fg_color=C["accent"], hover_color=C["primary_hover"],
            text_color="#ffffff", state=tk.DISABLED,
            width=90, height=30, font=("Microsoft YaHei UI", 11), corner_radius=6,
        )
        self.suggest_btn.pack(side=tk.RIGHT, padx=(2, 6))

    # ═══════════════════ 主内容区 ═══════════════════
    def _build_content(self):
        paned = tk.PanedWindow(
            self.main_area, orient=tk.HORIZONTAL,
            bg=C["bg"], bd=0, sashwidth=2, sashpad=0,
            sashrelief="flat",
        )
        paned.grid(row=2, column=0, sticky="nsew", pady=(4, 0))

        # ─── 左侧列表 ───
        left_card = ctk.CTkFrame(paned, corner_radius=10, fg_color=C["surface"])
        paned.add(left_card, width=520, minsize=400)

        self._build_treeview(left_card)

        # ─── 右侧详情 ───
        right_card = ctk.CTkFrame(paned, corner_radius=10, fg_color=C["surface"])
        paned.add(right_card, width=520, minsize=300)

        self._build_detail_panel(right_card)

    # ─── Treeview 构建 ───
    def _build_treeview(self, parent):
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill=tk.X, padx=14, pady=(12, 4))
        ctk.CTkLabel(
            header, text="文献列表",
            font=("Microsoft YaHei UI", 12, "bold"), text_color=C["text"]
        ).pack(side=tk.LEFT)
        self._list_count_label = ctk.CTkLabel(
            header, text="",
            font=("Microsoft YaHei UI", 10), text_color=C["text_muted"]
        )
        self._list_count_label.pack(side=tk.RIGHT)

        tree_frame = tk.Frame(parent, bg=C["surface"])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background=C["tree_bg"],
            foreground=C["text"],
            fieldbackground=C["tree_bg"],
            rowheight=32,
            font=("Microsoft YaHei UI", 11),
            borderwidth=0,
        )
        style.configure(
            "Treeview.Heading",
            background=C["surface"],
            foreground=C["text_muted"],
            font=("Microsoft YaHei UI", 10, "bold"),
            borderwidth=0,
            relief="flat",
        )
        style.map("Treeview",
            background=[("selected", C["tree_sel"])],
            foreground=[("selected", C["text"])],
        )
        style.map("Treeview.Heading",
            background=[("active", C["surface"])],
        )

        columns = ('title', 'category', 'year', 'authors', 'pages')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        self.sort_column = None
        self.sort_reverse = False
        self.column_titles = {
            'title': '标题',
            'category': '分类',
            'year': '年份',
            'authors': '作者',
            'pages': '页数'
        }
        for col, text in self.column_titles.items():
            self.tree.heading(col, text=text, command=lambda c=col: self.sort_by_column(c))
        self.tree.column('title', width=210)
        self.tree.column('category', width=70, anchor=tk.CENTER)
        self.tree.column('year', width=50, anchor=tk.CENTER)
        self.tree.column('authors', width=90)
        self.tree.column('pages', width=50, anchor=tk.CENTER)

        # 垂直滚动条
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        # 水平滚动条 - 兜底防止列内容溢出
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        self.tree.bind('<Double-1>', lambda e: self.open_pdf())
        self.tree.bind('<Delete>', lambda e: self.delete_selected_papers())

    # ─── 详情面板构建 ───
    def _build_detail_panel(self, parent):
        detail_scroll = ctk.CTkScrollableFrame(
            parent, fg_color="transparent",
            scrollbar_button_color=C["border"],
            scrollbar_button_hover_color=C["primary"],
        )
        detail_scroll.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.detail_scroll = detail_scroll

        # ─── 文献信息卡片 ───
        info_card = ctk.CTkFrame(
            detail_scroll, corner_radius=10, fg_color=C["card"]
        )
        info_card.pack(fill=tk.X, padx=6, pady=(6, 3))

        ctk.CTkLabel(
            info_card, text="文献信息",
            font=("Microsoft YaHei UI", 11, "bold"), text_color=C["primary"]
        ).pack(anchor="w", padx=14, pady=(12, 8))

        self.info_title = ctk.CTkLabel(
            info_card, text="标题: —",
            font=("Microsoft YaHei UI", 12), text_color=C["text"],
            wraplength=500, justify="left", anchor="w"
        )
        self.info_title.pack(anchor="w", padx=14, pady=2)

        self.info_author = ctk.CTkLabel(
            info_card, text="作者: —",
            font=("Microsoft YaHei UI", 11), text_color=C["text_secondary"], anchor="w"
        )
        self.info_author.pack(anchor="w", padx=14, pady=1)

        meta_row = ctk.CTkFrame(info_card, fg_color="transparent")
        meta_row.pack(fill=tk.X, padx=14, pady=(6, 2))
        self.info_year = ctk.CTkLabel(
            meta_row, text="年份: —",
            font=("Microsoft YaHei UI", 11), text_color=C["text_secondary"]
        )
        self.info_year.pack(side=tk.LEFT, padx=(0, 20))
        self.info_category = ctk.CTkLabel(
            meta_row, text="分类: —",
            font=("Microsoft YaHei UI", 11), text_color=C["text_secondary"]
        )
        self.info_category.pack(side=tk.LEFT)

        self.info_doi = ctk.CTkLabel(
            info_card, text="DOI: —",
            font=("Microsoft YaHei UI", 11), text_color=C["primary"], anchor="w",
            cursor="hand2"
        )
        self.info_doi.pack(anchor="w", padx=14, pady=(4, 0))
        self.info_doi.bind('<Button-1>', self._copy_doi)

        self.info_keywords = ctk.CTkLabel(
            info_card, text="关键词: —",
            font=("Microsoft YaHei UI", 11), text_color=C["text_secondary"],
            wraplength=500, justify="left", anchor="w"
        )
        self.info_keywords.pack(anchor="w", padx=14, pady=(2, 12))

        # ─── 编辑卡片 ───
        edit_card = ctk.CTkFrame(
            detail_scroll, corner_radius=10, fg_color=C["card"]
        )
        edit_card.pack(fill=tk.X, padx=6, pady=3)

        edit_row = ctk.CTkFrame(edit_card, fg_color="transparent")
        edit_row.pack(fill=tk.X, padx=14, pady=12)

        ctk.CTkLabel(
            edit_row, text="标签", font=("Microsoft YaHei UI", 11), text_color=C["text_muted"]
        ).pack(side=tk.LEFT)
        self.tag_var = tk.StringVar()
        ctk.CTkEntry(
            edit_row, textvariable=self.tag_var, width=140, height=30,
            placeholder_text="输入标签...",
            fg_color=C["input_bg"], border_color=C["input_border"],
            text_color=C["text"], font=("Microsoft YaHei UI", 11),
            corner_radius=6,
        ).pack(side=tk.LEFT, padx=6)

        ctk.CTkLabel(
            edit_row, text="分类", font=("Microsoft YaHei UI", 11), text_color=C["text_muted"]
        ).pack(side=tk.LEFT, padx=(14, 6))
        self.cat_var = ctk.CTkComboBox(
            edit_row, values=get_categories(),
            width=140, height=30,
            fg_color=C["input_bg"], border_color=C["input_border"],
            button_color=C["primary"], button_hover_color=C["primary_hover"],
            text_color=C["text"], font=("Microsoft YaHei UI", 11),
            dropdown_fg_color=C["surface"],
            dropdown_text_color=C["text"],
            corner_radius=6,
        )
        self.cat_var.pack(side=tk.LEFT, padx=4)

        ctk.CTkButton(
            edit_row, text="保存", command=self.save_metadata,
            width=56, height=30, font=("Microsoft YaHei UI", 11), corner_radius=6,
            fg_color=C["success"], hover_color="#43a047",
        ).pack(side=tk.LEFT, padx=(14, 0))

        # ─── AI 分析卡片 ───
        analysis_card = ctk.CTkFrame(
            detail_scroll, corner_radius=10, fg_color=C["card"]
        )
        analysis_card.pack(fill=tk.X, padx=6, pady=3)

        ctk.CTkLabel(
            analysis_card, text="AI 分析",
            font=("Microsoft YaHei UI", 11, "bold"), text_color=C["accent"]
        ).pack(anchor="w", padx=14, pady=(12, 6))

        ctk.CTkLabel(
            analysis_card, text="主要方法",
            font=("Microsoft YaHei UI", 10), text_color=C["text_muted"], anchor="w"
        ).pack(anchor="w", padx=14)
        self.methods_text = ctk.CTkTextbox(
            analysis_card, height=56, wrap="word",
            fg_color=C["input_bg"], border_color=C["border"],
            border_width=1, text_color=C["text"],
            font=("Microsoft YaHei UI", 11), corner_radius=6,
        )
        self.methods_text.pack(fill=tk.X, padx=14, pady=(2, 8))

        ctk.CTkLabel(
            analysis_card, text="创新点",
            font=("Microsoft YaHei UI", 10), text_color=C["text_muted"], anchor="w"
        ).pack(anchor="w", padx=14)
        self.innovations_text = ctk.CTkTextbox(
            analysis_card, height=56, wrap="word",
            fg_color=C["input_bg"], border_color=C["border"],
            border_width=1, text_color=C["text"],
            font=("Microsoft YaHei UI", 11), corner_radius=6,
        )
        self.innovations_text.pack(fill=tk.X, padx=14, pady=(2, 8))

        ctk.CTkButton(
            analysis_card, text="重新分析（LLM）", command=self.reanalyze_paper,
            width=130, height=28, font=("Microsoft YaHei UI", 10),
            corner_radius=6,
            fg_color="transparent", hover_color=C["card"],
            text_color=C["primary"], border_color=C["primary"],
            border_width=1,
        ).pack(anchor="w", padx=14, pady=(0, 12))

        # ─── 课题创新建议卡片 ───
        _topic_card = ctk.CTkFrame(
            detail_scroll, corner_radius=10, fg_color=C["card"]
        )
        _topic_card.pack(fill=tk.X, padx=6, pady=3)

        ctk.CTkLabel(
            _topic_card, text="课题创新建议",
            font=("Microsoft YaHei UI", 11, "bold"), text_color=C["accent"]
        ).pack(anchor="w", padx=14, pady=(12, 4))

        ctk.CTkLabel(
            _topic_card,
            text="输入您的研究方向／课题，AI 将基于当前结构/CADD/细胞生物学文献给出具体建议",
            font=("Microsoft YaHei UI", 9), text_color=C["text_muted"], anchor="w",
            wraplength=600, justify="left"
        ).pack(anchor="w", padx=14, pady=(0, 4))

        _topic_row = ctk.CTkFrame(_topic_card, fg_color="transparent")
        _topic_row.pack(fill=tk.X, padx=14, pady=(0, 8))
        _topic_row.columnconfigure(0, weight=1)

        self.topic_input = ctk.CTkEntry(
            _topic_row,
            placeholder_text="例：GPCR构象动力学与配体选择性机制",
            height=32, font=("Microsoft YaHei UI", 11),
            fg_color=C["input_bg"], border_color=C["border"],
            border_width=1, text_color=C["text"], corner_radius=6,
        )
        self.topic_input.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        self.topic_advice_btn = ctk.CTkButton(
            _topic_row, text="生成建议",
            command=self.suggest_for_my_topic,
            width=80, height=32, font=("Microsoft YaHei UI", 10),
            corner_radius=6, fg_color=C["primary"], hover_color=C["primary_hover"],
            state=tk.DISABLED,
        )
        self.topic_advice_btn.grid(row=0, column=1)

        ctk.CTkLabel(
            _topic_card, text="AI 建议",
            font=("Microsoft YaHei UI", 10), text_color=C["text_muted"], anchor="w"
        ).pack(anchor="w", padx=14)

        self.my_topic_advice_text = ctk.CTkTextbox(
            _topic_card, height=200, wrap="word",
            fg_color=C["input_bg"], border_color=C["border"],
            border_width=1, text_color=C["text"],
            font=("Microsoft YaHei UI", 11), corner_radius=6,
        )
        self.my_topic_advice_text.pack(fill=tk.X, padx=14, pady=(2, 12))

        # ─── 摘要卡片 ───
        abs_card = ctk.CTkFrame(
            detail_scroll, corner_radius=10, fg_color=C["card"]
        )
        abs_card.pack(fill=tk.BOTH, expand=True, padx=6, pady=(3, 6))

        ctk.CTkLabel(
            abs_card, text="摘要",
            font=("Microsoft YaHei UI", 11, "bold"), text_color=C["text"]
        ).pack(anchor="w", padx=14, pady=(12, 6))

        self.abstract_text = ctk.CTkTextbox(
            abs_card, wrap="word",
            fg_color=C["input_bg"], border_color=C["border"],
            border_width=1, text_color=C["text"],
            font=("Microsoft YaHei UI", 11), corner_radius=6,
        )
        self.abstract_text.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 12))
        self.root.after_idle(self._bind_detail_mousewheel)

    def _bind_detail_mousewheel(self):
        """把鼠标滚轮事件从所有子控件转发给详情面板的滚动容器。

        大文本框（摘要、AI建议）保留自身的滚动行为，不做转发。
        """
        try:
            canvas = self.detail_scroll._parent_canvas
        except AttributeError:
            return

        # 这两个大文本框保留自身滚动行为
        skip = set()
        for attr in ("abstract_text", "my_topic_advice_text"):
            w = getattr(self, attr, None)
            if w is not None:
                skip.add(w)

        def _scroll(event):
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

        def _bind(widget):
            if widget in skip:
                return
            try:
                widget.bind("<MouseWheel>", _scroll, add="+")
            except Exception:
                pass
            try:
                for child in widget.winfo_children():
                    _bind(child)
            except Exception:
                pass

        _bind(self.detail_scroll)

    def refresh_filter_options(self):
        """同步分类筛选、标签筛选、右侧分类下拉框。"""
        categories = get_categories()
        tags = get_all_tags()

        cur_cat_filter = self.cat_filter.get() if hasattr(self, 'cat_filter') else "全部"
        cur_cat = self.cat_var.get() if hasattr(self, 'cat_var') else ""
        cur_tag = self.tag_filter.get() if hasattr(self, 'tag_filter') else "全部"

        all_cats = ["全部"] + categories
        self.cat_filter.configure(values=all_cats)
        self.cat_var.configure(values=categories)
        all_tags = ["全部"] + tags
        self.tag_filter.configure(values=all_tags)

        self.cat_filter.set(cur_cat_filter if cur_cat_filter in all_cats else "全部")
        if cur_cat in categories:
            self.cat_var.set(cur_cat)
        self.tag_filter.set(cur_tag if cur_tag in all_tags else "全部")

    def refresh_category_options(self):
        """向后兼容别名。"""
        self.refresh_filter_options()

    def refresh_after_data_change(self):
        """数据库内容变化后刷新筛选选项和列表。"""
        self.refresh_filter_options()
        self.refresh_list()
    
    def sort_by_column(self, column):
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False
        self.refresh_list()
    
    def get_sort_key(self, row):
        # row: (id, title, category, year, authors, page_count, added_date)
        if self.sort_column == 'pages':
            return row[5] or 0
        if self.sort_column == 'year':
            return row[3] or ''
        if self.sort_column == 'category':
            text = row[2] or '未分类'
        elif self.sort_column == 'authors':
            text = row[4] or ''
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
        tag_filter = self.tag_filter.get() if hasattr(self, 'tag_filter') else "全部"
        year_from = (self.year_from_var.get() if hasattr(self, 'year_from_var') else '').strip()
        year_to   = (self.year_to_var.get()   if hasattr(self, 'year_to_var')   else '').strip()

        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = get_db_conn()
        c = conn.cursor()

        query = '''SELECT id, title, category, year, authors, page_count, added_date FROM papers WHERE 1=1'''
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

        if tag_filter and tag_filter != "全部":
            query += " AND tags LIKE ?"
            params.append(f'%{tag_filter}%')

        if year_from.isdigit():
            query += " AND CAST(year AS INTEGER) >= ?"
            params.append(int(year_from))

        if year_to.isdigit():
            query += " AND CAST(year AS INTEGER) <= ?"
            params.append(int(year_to))

        query += " ORDER BY added_date DESC"
        
        c.execute(query, params)
        rows = c.fetchall()
        conn.close()
        
        if self.sort_column:
            rows.sort(key=self.get_sort_key, reverse=self.sort_reverse)
        
        self.update_sort_headings()
        
        for row in rows:
            self.tree.insert('', tk.END, values=(row[1], row[2] or '未分类', row[3] or '', row[4] or '', row[5] or 0), iid=row[0])

        if hasattr(self, '_list_count_label'):
            self._list_count_label.configure(text=f"共 {len(rows)} 篇")
    
    def on_select(self, event):
        selection = self.tree.selection()
        # 多选≥2篇时激活课题建议按钮
        self.suggest_btn.configure(
            state=tk.NORMAL if len(selection) >= 2 else tk.DISABLED
        )
        if not selection:
            return

        paper_id = selection[0]
        self.current_paper_id = paper_id
        
        conn = get_db_conn()
        c = conn.cursor()
        c.execute('''SELECT title, authors, category, keywords, abstract, tags, methods, innovations, file_path, year, doi
                     FROM papers WHERE id=?''', (paper_id,))
        row = c.fetchone()
        conn.close()

        if row:
            self.info_title.configure(text=f"标题: {row[0]}")
            self.info_author.configure(text=f"作者: {row[1] or '未知'}")
            self.info_year.configure(text=f"年份: {row[9] or '未知'}")
            doi_val = row[10] or ''
            self.info_doi.configure(text=f"DOI: {doi_val or 'N/A'}")
            self.info_category.configure(text=f"分类: {row[2] or '未分类'}")
            self.info_keywords.configure(text=f"关键词: {row[3] or '无'}")

            self.cat_var.set(row[2] or '未分类')
            self.tag_var.set(row[5] or '')

            self.methods_text.delete("1.0", tk.END)
            self.methods_text.insert("1.0", ' '.join((row[6] or '').split()))

            self.innovations_text.delete("1.0", tk.END)
            self.innovations_text.insert("1.0", ' '.join((row[7] or '').split()))
            # 切换文献时清空课题建议区，激活生成按鈕
            if hasattr(self, "my_topic_advice_text"):
                self.my_topic_advice_text.delete("1.0", tk.END)
            if hasattr(self, "topic_advice_btn"):
                self.topic_advice_btn.configure(state=tk.NORMAL)

            self.abstract_text.delete("1.0", tk.END)
            self.abstract_text.insert("1.0", row[4] or '无摘要')

    def on_suggest_topics(self):
        """响应课题建议按钮点击"""
        paper_ids = list(self.tree.selection())
        if len(paper_ids) < 2:
            messagebox.showwarning("提示", "请至少选择2篇论文（Ctrl+点击多选）")
            return
        if len(paper_ids) > 15:
            if not messagebox.askyesno(
                "提示",
                f"已选择 {len(paper_ids)} 篇，建议5–10篇以获得更聚焦的建议。\n是否继续？"
            ):
                return
        research_topic = simpledialog.askstring(
            "研究主题（可选）",
            "可预设研究方向或研究主题；留空则按默认逻辑分析：",
            parent=self.root
        )
        if research_topic is None:
            return
        ResearchSuggestionsDialog(self.root, paper_ids, research_topic.strip())

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
            self.root.after(0, self.refresh_after_data_change)
            
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
        methods = self.methods_text.get("1.0", tk.END).strip()
        innovations = self.innovations_text.get("1.0", tk.END).strip()
        
        conn = get_db_conn()
        c = conn.cursor()
        c.execute('''UPDATE papers SET tags=?, category=?, methods=?, innovations=? WHERE id=?''',
                  (tags, category, methods, innovations, self.current_paper_id))
        conn.commit()
        conn.close()
        
        self.refresh_after_data_change()
        messagebox.showinfo("完成", "已保存")
    
    def refresh_model_menu(self):
        """刷新解析引擎菜单（侧边栏）。"""
        if not hasattr(self, '_model_selector'):
            return
        self._model_selector.configure(values=list(AVAILABLE_MODELS.keys()))
        self._model_selector.set(self.model_var.get())
        self._sidebar_model_label.configure(text=f"当前: {self.model_var.get()}")

    def configure_custom_model(self):
        """新增或更新自定义 OpenAI-style 模型配置。"""
        name = simpledialog.askstring(
            "自定义模型",
            "请输入模型显示名称（例如 gpt-4.1 或 qwen-max）：",
            parent=self.root
        )
        if not name:
            return
        name = name.strip()
        if name in DEFAULT_MODEL_CONFIGS:
            messagebox.showwarning("提示", "预设模型不可覆盖，请换一个显示名称。", parent=self.root)
            return

        existing = MODEL_CONFIGS.get(name, {})
        model_id = simpledialog.askstring(
            "模型ID",
            "请输入 API 请求中的 model 值：",
            parent=self.root,
            initialvalue=existing.get("model", name)
        )
        if not model_id:
            return
        base_url = simpledialog.askstring(
            "API Base URL",
            "请输入兼容 /chat/completions 的 Base URL：",
            parent=self.root,
            initialvalue=existing.get("base_url", "https://api.deepseek.com/v1")
        )
        if not base_url:
            return
        api_key = simpledialog.askstring(
            "API Key（可选）",
            "请输入该模型的 API Key；留空则使用 LLM_API_KEY 环境变量：",
            parent=self.root,
            show="*",
            initialvalue=existing.get("api_key", "")
        )
        if api_key is None:
            return

        MODEL_CONFIGS[name] = {
            "model": model_id.strip(),
            "base_url": base_url.strip().rstrip("/"),
            "api_key_env": "",
            "api_key": api_key.strip()
        }
        refresh_available_models()
        save_model_configs()
        self.refresh_model_menu()
        self.model_var.set(name)
        self.on_model_change()

    def on_model_change(self):
        """切换解析引擎"""
        global LLM_API_KEY
        apply_model_config(self.model_var.get())
        if not LLM_API_KEY:
            key = simpledialog.askstring(
                f"{CURRENT_MODEL_NAME} API Key",
                f"当前模型尚未配置 API Key。请输入 {CURRENT_MODEL_NAME} 的 API Key；留空则稍后再配置：",
                parent=self.root,
                show="*"
            )
            if key:
                LLM_API_KEY = key.strip()
                remember_api_key_for_current_model(LLM_API_KEY)
        if hasattr(self, '_sidebar_model_label'):
            self._sidebar_model_label.configure(text=f"当前: {CURRENT_MODEL_NAME}")
        messagebox.showinfo(
            "引擎切换",
            f"已切换至: {CURRENT_MODEL_NAME}\n模型ID: {LLM_MODEL}\nAPI: {LLM_BASE_URL}\n下次调用AI时生效"
        )
    
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

        placeholders = ','.join('?' * len(selected))
        c.execute(f'SELECT id, file_path FROM papers WHERE id IN ({placeholders})', list(selected))
        rows = c.fetchall()

        for _item_id, file_path in rows:
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except PermissionError:
                    try:
                        import time
                        pending_dir = os.path.join(os.path.dirname(file_path), '_pending_delete')
                        os.makedirs(pending_dir, exist_ok=True)
                        new_name = f"{int(time.time())}_{os.path.basename(file_path)}"
                        os.rename(file_path, os.path.join(pending_dir, new_name))
                    except Exception:
                        pass

        try:
            c.execute(f'DELETE FROM papers WHERE id IN ({placeholders})', list(selected))
            deleted = c.rowcount
            conn.commit()
        except sqlite3.OperationalError:
            conn.rollback()
            deleted = 0
        conn.close()

        self.current_paper_id = None
        self.refresh_after_data_change()
        self.clear_detail()
        messagebox.showinfo("完成", f"已删除 {deleted} 篇文献")
    
    def manage_categories(self):
        """管理分类对话框"""
        try:
            if self._category_dialog and self._category_dialog.winfo_exists():
                self._category_dialog.lift()
                self._category_dialog.focus_force()
                return

            dialog = ctk.CTkToplevel(self.root)
            self._category_dialog = dialog
            dialog.title("管理分类")
            dialog.geometry("360x480")
            dialog.configure(fg_color=C["surface"])
            dialog.transient(self.root)
            dialog.lift()
            dialog.focus_force()

            def close_dialog():
                self._category_dialog = None
                dialog.destroy()

            dialog.protocol("WM_DELETE_WINDOW", close_dialog)
        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("分类管理打开失败", str(e), parent=self.root)
            return
        
        ctk.CTkLabel(
            dialog, text="📂 分类管理",
            font=FONT_HEADER, text_color=C["primary"]
        ).pack(pady=(16, 8))
        ctk.CTkLabel(
            dialog, text="现有分类",
            font=FONT_SMALL, text_color=C["text_secondary"]
        ).pack(anchor="w", padx=20)
        
        list_frame = ctk.CTkFrame(dialog, fg_color=C["card"], corner_radius=8)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(4, 12))
        listbox = tk.Listbox(
            list_frame, bg=C["input_bg"], fg=C["text"],
            selectbackground=C["tree_sel"], selectforeground=C["text"],
            font=FONT_SMALL, borderwidth=0, highlightthickness=0
        )
        listbox.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        for cat in get_categories():
            listbox.insert(tk.END, cat)
        
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 16))
        
        def add_new():
            name = simpledialog.askstring("新建分类", "分类名称:", parent=dialog)
            if name and add_category(name):
                listbox.insert(tk.END, name)
                self.refresh_category_options()
        
        def delete_selected():
            sel = listbox.curselection()
            if sel:
                name = listbox.get(sel[0])
                if messagebox.askyesno("确认", f"删除分类 '{name}'？\n该分类下的文献将变为'未分类'", parent=dialog):
                    delete_category(name)
                    listbox.delete(sel[0])
                    self.refresh_category_options()
        
        ctk.CTkButton(
            btn_frame, text="添加", command=add_new,
            width=80, height=32, font=FONT_SMALL, corner_radius=6,
            fg_color=C["success"], hover_color="#43a047",
        ).pack(side=tk.LEFT, padx=4)
        ctk.CTkButton(
            btn_frame, text="删除", command=delete_selected,
            width=80, height=32, font=FONT_SMALL, corner_radius=6,
            fg_color="transparent", hover_color=C["error"],
            text_color=C["text_secondary"], border_color=C["border"],
            border_width=1,
        ).pack(side=tk.LEFT, padx=4)
        ctk.CTkButton(
            btn_frame, text="关闭", command=close_dialog,
            width=80, height=32, font=FONT_SMALL, corner_radius=6,
            fg_color=C["card"], hover_color=C["border"],
            text_color=C["text"],
        ).pack(side=tk.RIGHT, padx=4)
    
    def clear_detail(self):
        self.info_title.configure(text="标题: ")
        self.info_author.configure(text="作者: ")
        self.info_year.configure(text="年份: ")
        self.info_doi.configure(text="DOI: ")
        self.info_category.configure(text="分类: ")
        self.info_keywords.configure(text="关键词: ")
        self.cat_var.set('')
        self.tag_var.set('')
        self.methods_text.delete("1.0", tk.END)
        self.innovations_text.delete("1.0", tk.END)
        self.abstract_text.delete("1.0", tk.END)

    # ── 路径修复 + 元数据补全 ──────────────────────────────────
    def repair_and_fill_metadata(self):
        """
        分两步：
        1. 对路径断裂的文献，在多个候选目录按文件名重新匹配
        2. 对路径可访问但缺 DOI/year 的文献，从 PDF 正则提取
        均不调用 LLM，速度快。
        """
        # 收集所有包含可访问 PDF 的目录作为搜索范围
        search_dirs = {PDF_STORAGE}
        conn = get_db_conn()
        c = conn.cursor()
        c.execute('SELECT file_path FROM papers WHERE file_path IS NOT NULL')
        for (fp,) in c.fetchall():
            if fp and os.path.exists(fp):
                search_dirs.add(os.path.dirname(fp))
        conn.close()
        search_dirs = list(search_dirs)

        prog = tk.Toplevel(self.root)
        prog.title("修复路径 & 补全元数据")
        prog.geometry("500x180")
        prog.resizable(False, False)
        pbar = ttk.Progressbar(prog, mode='indeterminate', length=460)
        pbar.pack(padx=20, pady=16)
        pbar.start(12)
        slabel = ttk.Label(prog, text="正在扫描…")
        slabel.pack()

        def _task():
            conn2 = get_db_conn()
            c2 = conn2.cursor()
            c2.execute('SELECT id, file_path, doi, year, authors, page_count FROM papers')
            all_rows = c2.fetchall()

            fixed_paths = 0
            filled_meta = 0

            for pid, fp, cur_doi, cur_year, cur_authors, cur_page_count in all_rows:
                # ── Step 1: 路径修复 ──────────────────────────
                actual_fp = fp
                if fp and not os.path.exists(fp):
                    fname = os.path.basename(fp)
                    for d in search_dirs:
                        candidate = os.path.join(d, fname)
                        if os.path.exists(candidate):
                            c2.execute('UPDATE papers SET file_path=? WHERE id=?',
                                       (candidate, pid))
                            actual_fp = candidate
                            fixed_paths += 1
                            break

                if not actual_fp or not os.path.exists(actual_fp):
                    continue

                # ── Step 2: 补全 DOI / year / authors / page_count ──
                need_doi        = not (cur_doi     and cur_doi.strip())
                need_year       = not (cur_year    and cur_year.strip())
                need_authors    = not (cur_authors and cur_authors.strip())
                need_page_count = not cur_page_count or cur_page_count == 0
                if not need_doi and not need_year and not need_authors and not need_page_count:
                    continue

                try:
                    with fitz.open(actual_fp) as doc:
                        meta = doc.metadata
                        text = ''.join(
                            doc.load_page(i).get_text()
                            for i in range(min(5, len(doc)))
                        )
                        pdf_page_count = len(doc)
                except Exception:
                    continue

                fields, vals = [], []
                if need_page_count and pdf_page_count > 0:
                    fields.append('page_count=?'); vals.append(pdf_page_count)
                if need_doi:
                    doi = extract_doi_from_text(text)
                    if doi:
                        fields.append('doi=?'); vals.append(doi)
                if need_year:
                    year = (extract_year_from_metadata(meta)
                            or extract_year_from_text(text))
                    if year:
                        fields.append('year=?'); vals.append(year)
                if need_authors:
                    # 先查PDF元数据
                    authors = (meta.get('author') or '').strip()
                    if not authors:
                        authors = extract_authors_from_text(text)
                    if authors:
                        fields.append('authors=?'); vals.append(authors)

                if fields:
                    vals.append(pid)
                    c2.execute(f"UPDATE papers SET {', '.join(fields)} WHERE id=?", vals)
                    filled_meta += 1

            conn2.commit()   # 先提交路径修复 + PDF提取结果

            # ── Step 3: CrossRef 在线补全（仍缺失 DOI 或作者的记录）──
            self.root.after(0, lambda: slabel.config(text="CrossRef 在线查询中…"))
            import time as _time
            filled_crossref = 0

            # 重新查询仍有缺失的记录（已由步骤2更新的行会被自动排除）
            c2.execute(
                "SELECT id, title, doi, year, authors FROM papers "
                "WHERE title IS NOT NULL AND length(title) > 10 "
                "  AND (doi IS NULL OR doi = '' "
                "       OR authors IS NULL OR authors = '')"
            )
            cr_rows = c2.fetchall()
            n_cr = len(cr_rows)

            for cr_idx, (cr_pid, cr_title, cr_doi, cr_year, cr_authors) in enumerate(cr_rows):
                self.root.after(0,
                    lambda i=cr_idx: slabel.config(text=f"CrossRef [{i+1}/{n_cr}]…"))

                need_d = not (cr_doi     and cr_doi.strip())
                need_a = not (cr_authors and cr_authors.strip())
                need_y = not (cr_year    and cr_year.strip())
                if not need_d and not need_a:
                    _time.sleep(0.05)
                    continue

                cr = lookup_crossref(cr_title)
                f2, v2 = [], []
                if need_d and cr.get('doi'):
                    f2.append('doi=?');     v2.append(cr['doi'])
                if need_a and cr.get('authors'):
                    f2.append('authors=?'); v2.append(cr['authors'])
                if need_y and cr.get('year'):
                    f2.append('year=?');    v2.append(cr['year'])
                if f2:
                    v2.append(cr_pid)
                    c2.execute(f"UPDATE papers SET {', '.join(f2)} WHERE id=?", v2)
                    filled_crossref += 1

                _time.sleep(0.2)   # 礼貌延迟 200ms，避免触发 CrossRef 限流

            conn2.commit()
            conn2.close()

            self.root.after(0, prog.destroy)
            self.root.after(0, self.refresh_after_data_change)
            self.root.after(0, lambda: messagebox.showinfo(
                "完成",
                f"修复路径：{fixed_paths} 条\n"
                f"PDF提取补全：{filled_meta} 条\n"
                f"CrossRef补全：{filled_crossref} 条",
                parent=self.root
            ))

        threading.Thread(target=_task, daemon=True).start()

    # ── DOI 复制 ──────────────────────────────────────────────
    def _copy_doi(self, event=None):
        doi = self.info_doi.cget('text').replace('DOI: ', '').strip()
        if doi and doi != 'N/A':
            self.root.clipboard_clear()
            self.root.clipboard_append(doi)
            messagebox.showinfo("已复制", f"DOI 已复制：\n{doi}", parent=self.root)

    # ── 重新分析 ───────────────────────────────────────────────
    def reanalyze_paper(self):
        if not self.current_paper_id:
            return
        if not LLM_API_KEY:
            messagebox.showwarning("未配置", "请先配置 API Key（解析引擎菜单）", parent=self.root)
            return

        conn = get_db_conn()
        c = conn.cursor()
        c.execute('SELECT file_path, title, abstract, keywords FROM papers WHERE id=?',
                  (self.current_paper_id,))
        row = c.fetchone()
        conn.close()
        if not row:
            return

        file_path, title, abstract, keywords = row
        pid = self.current_paper_id

        def _task():
            categories = get_categories()
            year = ''
            doi = ''
            new_authors = ''
            if file_path and os.path.exists(file_path):
                full_text = extract_text_from_pdf(file_path, max_pages=5)
                filename_base = os.path.basename(file_path)
                doi = extract_doi_from_text(full_text)
                analysis = llm_full_analysis(full_text, filename_base, keywords or '', categories)
                year = analysis.get('year', '')
                new_authors = analysis.get('authors', '')
                if not year:
                    try:
                        with fitz.open(file_path) as doc:
                            year = extract_year_from_metadata(doc.metadata)
                    except Exception:
                        pass
                    year = year or extract_year_from_text(full_text)
                if not new_authors:
                    try:
                        with fitz.open(file_path) as doc:
                            meta_author = (doc.metadata.get('author') or '').strip()
                    except Exception:
                        meta_author = ''
                    new_authors = meta_author or extract_authors_from_text(full_text)
            else:
                analysis = analyze_paper(title or '', abstract or '', keywords or '', categories)
                year = analysis.get('year', '')
            self.root.after(0, lambda: self._apply_reanalysis(pid, analysis, year, doi, new_authors))

        threading.Thread(target=_task, daemon=True).start()
        messagebox.showinfo("提示", "正在后台重新分析，完成后自动刷新…", parent=self.root)

    def _apply_reanalysis(self, pid, analysis, year='', doi='', new_authors=''):
        conn = get_db_conn()
        c = conn.cursor()
        fields = ['category=?', 'methods=?', 'innovations=?', 'year=?']
        vals   = [analysis.get('category', '未分类'), ' '.join((analysis.get('methods') or '').split()),
                  ' '.join((analysis.get('innovations') or '').split()), year]
        llm_abstract = (analysis.get('abstract') or '').strip()
        if llm_abstract:
            fields.append('abstract=?')
            vals.append(llm_abstract)
        llm_keywords = (analysis.get('keywords_enhanced') or '').strip()
        if llm_keywords:
            fields.append('keywords=?')
            vals.append(llm_keywords)
        if doi:
            fields.append('doi=?')
            vals.append(doi)
        if new_authors:
            fields.append('authors=?')
            vals.append(new_authors)
        vals.append(pid)
        c.execute(f"UPDATE papers SET {', '.join(fields)} WHERE id=?", vals)
        conn.commit()
        conn.close()
        self.refresh_after_data_change()
        try:
            self.tree.selection_set(pid)
            self.on_select(None)
        except Exception:
            pass
        parts = ['分类/方法/创新点/年份']
        if llm_abstract: parts.append('摘要')
        if llm_keywords:  parts.append('关键词')
        if doi:           parts.append('DOI')
        if new_authors:   parts.append('作者')
        messagebox.showinfo("完成", f"重新分析完成，已更新：{'/ '.join(parts)}。", parent=self.root)

    def suggest_for_my_topic(self):
        """基于当前文献，为用户输入的课题生成创新建议。"""
        if not self.current_paper_id:
            messagebox.showwarning("提示", "请先选择一篇文献", parent=self.root)
            return
        topic = self.topic_input.get().strip()
        if not topic:
            messagebox.showwarning("提示", "请输入您的研究方向或课题内容", parent=self.root)
            return
        if not LLM_API_KEY:
            messagebox.showwarning(
                "未配置", "请先配置 API Key（解析引擎菜单）",
                parent=self.root
            )
            return

        conn = get_db_conn()
        c = conn.cursor()
        c.execute("SELECT title, abstract, methods, innovations FROM papers WHERE id=?",
                  (self.current_paper_id,))
        row = c.fetchone()
        conn.close()
        if not row:
            return

        title, abstract, methods, innovations = row

        self.my_topic_advice_text.delete("1.0", tk.END)
        self.my_topic_advice_text.insert("1.0", "正在生成建议，请稍候…")
        self.topic_advice_btn.configure(state=tk.DISABLED)

        topic_snap = topic
        pid_snap = self.current_paper_id

        def _task():
            system_prompt = (
                "你是一位资深科研导师，擅长结构生物学、CADD 与细胞生物学的跨领域创新迁移。"
                "用户将告知自己的课题，以及一篇参考文献的核心内容，"
                "你需要基于该文献，给出具体可操作的创新建议，"
                "帮助用户改进或扩展自己的课题。"
            )
            user_prompt = (
                f"我的课题/研究方向：{topic_snap}\n\n"
                f"参考文献标题：{title or '未知'}\n"
                f"文献摘要：{(abstract or '无')[:800]}\n"
                f"文献主要方法：{methods or '无'}\n"
                f"文献主要创新点：{innovations or '无'}\n\n"
                "请基于以上文献内容，为我的课题提出 3−5 条具体、可操作的创新建议。\n"
                "要求：\n"
                "1. 每条建议需明确说明从文献中借鉴了哪种技术或思路；\n"
                "2. 说明如何将其迁移或应用到我的课题中；\n"
                "3. 避免泛泛而谈，建议需有技术细节；\n"
                "4. 每条建议 120–220 字，按编号列出。"
            )
            advice, error, finish_reason = call_llm_ext(
                system_prompt, user_prompt,
                max_tokens=2000, temperature=0.5, timeout=90
            )
            if error:
                result_text = f"生成失败：{error}"
            else:
                raw = (advice or "").strip()
                raw_lines = raw.split("\n")
                normalized = []
                for ln in raw_lines:
                    normalized.append(" ".join(ln.split()) if ln.strip() else "")
                result_lines = []
                prev_empty = False
                for ln in normalized:
                    if ln == "":
                        if not prev_empty:
                            result_lines.append("")
                        prev_empty = True
                    else:
                        result_lines.append(ln)
                        prev_empty = False
                result_text = "\n".join(result_lines).strip()
                if finish_reason == "length":
                    result_text += "\n\n（输出已达 token 上限，建议可能不完整）"

            def _update():
                if self.current_paper_id != pid_snap:
                    self.topic_advice_btn.configure(state=tk.NORMAL)
                    return
                self.my_topic_advice_text.delete("1.0", tk.END)
                self.my_topic_advice_text.insert("1.0", result_text)
                self.topic_advice_btn.configure(state=tk.NORMAL)
            self.root.after(0, _update)

        threading.Thread(target=_task, daemon=True).start()

    # ── 批量重新分析 ───────────────────────────────────────────
    def batch_reanalyze_papers(self):
        selected = list(self.tree.selection())
        if not selected:
            messagebox.showwarning("提示", "请先选择要重新分析的文献（Ctrl+点击多选）", parent=self.root)
            return
        if not LLM_API_KEY:
            messagebox.showwarning("未配置", "请先配置 API Key（解析引擎菜单）", parent=self.root)
            return
        if not messagebox.askyesno(
            "确认",
            f"将对选中的 {len(selected)} 篇文献重新进行 LLM 分析。\n"
            "每篇约需 5-15 秒，可能较耗时。确认继续？",
            parent=self.root
        ):
            return

        prog = tk.Toplevel(self.root)
        prog.title("批量重新分析")
        prog.geometry("480x170")
        prog.resizable(False, False)
        ttk.Label(prog, text=f"正在分析 {len(selected)} 篇文献…").pack(pady=8)
        pbar = ttk.Progressbar(prog, mode='determinate', maximum=len(selected))
        pbar.pack(fill=tk.X, padx=20)
        slabel = ttk.Label(prog, text="准备中…")
        slabel.pack(pady=6)

        def _task():
            categories = get_categories()
            done = 0
            for pid in selected:
                conn = get_db_conn()
                c2 = conn.cursor()
                c2.execute('SELECT file_path, title, abstract, keywords FROM papers WHERE id=?', (pid,))
                row = c2.fetchone()
                conn.close()
                if not row:
                    done += 1
                    continue
                file_path, title, abstract, keywords = row

                self.root.after(0, lambda d=done, t=(title or '')[:38]:
                    (pbar.config(value=d), slabel.config(text=f"[{d+1}/{len(selected)}] {t}…")))

                year = doi = new_authors = ''
                try:
                    if file_path and os.path.exists(file_path):
                        full_text = extract_text_from_pdf(file_path, max_pages=5)
                        doi = extract_doi_from_text(full_text)
                        analysis = llm_full_analysis(
                            full_text, os.path.basename(file_path), keywords or '', categories)
                        year = analysis.get('year', '')
                        new_authors = analysis.get('authors', '')
                        if not year:
                            try:
                                with fitz.open(file_path) as doc:
                                    meta = doc.metadata
                                    year = extract_year_from_metadata(meta)
                                    if not new_authors:
                                        new_authors = (meta.get('author') or '').strip()
                            except Exception:
                                pass
                            year = year or extract_year_from_text(full_text)
                        if not new_authors:
                            new_authors = extract_authors_from_text(full_text)
                    else:
                        analysis = analyze_paper(title or '', abstract or '', keywords or '', categories)
                        year = analysis.get('year', '')
                except Exception as e:
                    analysis = {'category': '未分类', 'methods': '', 'innovations': ''}
                    year = ''

                llm_abstract = analysis.get('abstract', '')
                llm_keywords = analysis.get('keywords_enhanced', '')
                fields = ['category=?', 'methods=?', 'innovations=?', 'year=?',
                          'abstract=?', 'keywords=?']
                vals   = [analysis.get('category', '未分类'), ' '.join((analysis.get('methods') or '').split()),
                          ' '.join((analysis.get('innovations') or '').split()), year,
                          llm_abstract or abstract or '',
                          llm_keywords or keywords or '']
                if doi:
                    fields.append('doi=?')
                    vals.append(doi)
                if new_authors:
                    fields.append('authors=?')
                    vals.append(new_authors)
                vals.append(pid)
                conn2 = get_db_conn()
                c3 = conn2.cursor()
                c3.execute(f"UPDATE papers SET {', '.join(fields)} WHERE id=?", vals)
                conn2.commit()
                conn2.close()
                done += 1

            self.root.after(0, prog.destroy)
            self.root.after(0, self.refresh_after_data_change)
            self.root.after(0, lambda: messagebox.showinfo(
                "完成", f"批量重新分析完成，共处理 {done} 篇文献。", parent=self.root))

        threading.Thread(target=_task, daemon=True).start()

    # ── 统计概览 ───────────────────────────────────────────────
    def show_statistics(self):
        conn = get_db_conn()
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM papers')
        total = c.fetchone()[0]
        c.execute('SELECT category, COUNT(*) FROM papers GROUP BY category ORDER BY COUNT(*) DESC')
        by_cat = c.fetchall()
        c.execute("""SELECT year, COUNT(*) FROM papers
                     WHERE year IS NOT NULL AND year != ''
                     GROUP BY year ORDER BY year DESC""")
        by_year = c.fetchall()
        conn.close()
        StatisticsDialog(self.root, total, by_cat, by_year)

    def export_csv(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV 文件", "*.csv")],
            title="导出为 CSV"
        )
        if not path:
            return
        conn = get_db_conn()
        c = conn.cursor()
        c.execute('''SELECT title, authors, year, doi, category, keywords,
                            abstract, tags, methods, innovations, added_date
                     FROM papers ORDER BY added_date DESC''')
        rows = c.fetchall()
        conn.close()

        import csv
        with open(path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['标题', '作者', '年份', 'DOI', '分类', '关键词',
                             '摘要', '标签', '主要方法', '创新点', '导入时间'])
            writer.writerows(rows)
        messagebox.showinfo("完成", f"已导出 {len(rows)} 条记录：\n{path}")

    # ── 导出 BibTeX ────────────────────────────────────────────
    def export_bibtex(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".bib",
            filetypes=[("BibTeX 文件", "*.bib")],
            title="导出为 BibTeX"
        )
        if not path:
            return
        conn = get_db_conn()
        c = conn.cursor()
        c.execute('SELECT title, authors, year, doi, keywords, abstract FROM papers ORDER BY year DESC, title')
        rows = c.fetchall()
        conn.close()

        entries = []
        for i, (title, authors, year, doi, keywords, abstract) in enumerate(rows, 1):
            first_word = re.sub(r'[^\w]', '', (title or 'unknown').split()[0])[:12]
            key = f"{first_word}{year or 'XXXX'}{i}"
            lines = [f"@article{{{key},"]
            if title:    lines.append(f'  title     = {{{{{title}}}}},')
            if authors:  lines.append(f'  author    = {{{authors}}},')
            if year:     lines.append(f'  year      = {{{year}}},')
            if doi:      lines.append(f'  doi       = {{{doi}}},')
            if keywords: lines.append(f'  keywords  = {{{keywords}}},')
            if abstract: lines.append(f'  abstract  = {{{abstract[:400]}}},')
            lines.append("}")
            entries.append("\n".join(lines))

        with open(path, 'w', encoding='utf-8') as f:
            f.write("\n\n".join(entries))
        messagebox.showinfo("完成", f"已导出 {len(rows)} 条记录：\n{path}")

    def open_scan_browser(self):
        ScanReportBrowser(self.root, on_import_done=self.refresh_after_data_change)

# ============ 扫描报告浏览器 ============
class ScanReportBrowser(tk.Toplevel):
    """
    扫描报告浏览器窗口：
    1. 加载 StructBioCADD_CellBio_scan_*.md 报告并列出论文
    2. 用户勾选感兴趣的论文
    3. 下载 PDF（后台线程）并写入 literature.db
    """

    CHECK_ON  = '☑'
    CHECK_OFF = '☐'

    def __init__(self, parent, on_import_done=None):
        super().__init__(parent)
        self.title("扫描报告浏览器")
        self.geometry("1100x680")
        self.resizable(True, True)
        self.on_import_done = on_import_done

        self._papers = []          # List[ScannedPaper]
        self._item_checks = {}     # tree item_id -> bool

        self._build_ui()
        self._load_default_report()

    # ── UI 构建 ────────────────────────────────────────────
    def _build_ui(self):
        # ── 顶部文件选择 ──
        top = ttk.Frame(self)
        top.pack(fill=tk.X, padx=8, pady=6)

        ttk.Label(top, text="报告文件:").pack(side=tk.LEFT)
        self._file_var = tk.StringVar()
        ttk.Entry(top, textvariable=self._file_var, width=55).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="浏览...", command=self._browse_file).pack(side=tk.LEFT)
        ttk.Button(top, text="加载", command=self._load_report).pack(side=tk.LEFT, padx=4)

        # ── 工具栏 ──
        bar = ttk.Frame(self)
        bar.pack(fill=tk.X, padx=8, pady=2)
        ttk.Button(bar, text="全选", command=self._select_all).pack(side=tk.LEFT)
        ttk.Button(bar, text="取消全选", command=self._deselect_all).pack(side=tk.LEFT, padx=4)
        self._count_label = ttk.Label(bar, text="")
        self._count_label.pack(side=tk.LEFT, padx=12)

        # ── 论文列表 ──
        cols = ('check', 'title', 'source', 'category', 'date', 'type')
        self._tree = ttk.Treeview(self, columns=cols, show='headings', height=14)
        self._tree.heading('check',    text='选择', anchor=tk.CENTER)
        self._tree.heading('title',    text='标题')
        self._tree.heading('source',   text='来源')
        self._tree.heading('category', text='分类')
        self._tree.heading('date',     text='日期')
        self._tree.heading('type',     text='类型')
        self._tree.column('check',    width=40,  stretch=False, anchor=tk.CENTER)
        self._tree.column('title',    width=440)
        self._tree.column('source',   width=160)
        self._tree.column('category', width=130)
        self._tree.column('date',     width=80,  anchor=tk.CENTER)
        self._tree.column('type',     width=70,  anchor=tk.CENTER)

        vsb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8, 0), pady=4)
        vsb.pack(side=tk.LEFT, fill=tk.Y, pady=4, padx=(0, 4))

        self._tree.bind('<ButtonRelease-1>', self._on_click)
        self._tree.bind('<<TreeviewSelect>>', self._on_select)

        # ── 详情面板 ──
        detail = ttk.LabelFrame(self, text="核心方法 / 详情", padding=6)
        detail.pack(fill=tk.X, padx=8, pady=4)
        self._detail_text = tk.Text(detail, height=4, wrap=tk.WORD, state=tk.DISABLED,
                                    background='#f5f5f5')
        self._detail_text.pack(fill=tk.X)

        # ── 操作按钮 ──
        btn_row = ttk.Frame(self)
        btn_row.pack(fill=tk.X, padx=8, pady=4)
        ttk.Button(btn_row, text="下载并导入选中",
                   command=self._download_and_import).pack(side=tk.LEFT)
        ttk.Button(btn_row, text="仅导入元数据（不下载PDF）",
                   command=self._import_metadata_only).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_row, text="复制选中链接",
                   command=self._copy_links).pack(side=tk.LEFT)

        # ── 进度条 ──
        prog_frame = ttk.Frame(self)
        prog_frame.pack(fill=tk.X, padx=8, pady=(0, 6))
        self._progress = ttk.Progressbar(prog_frame, mode='determinate', length=400)
        self._progress.pack(side=tk.LEFT)
        self._status_label = ttk.Label(prog_frame, text="")
        self._status_label.pack(side=tk.LEFT, padx=8)

    # ── 默认加载今日或最新报告 ──────────────────────────────
    def _load_default_report(self):
        lit_dir = os.path.dirname(os.path.abspath(__file__))
        today = datetime.now().strftime('%Y-%m-%d')
        default = os.path.join(lit_dir, f'StructBioCADD_CellBio_scan_{today}.md')
        if not os.path.isfile(default):
            # 找最新的扫描报告
            candidates = sorted(
                [f for f in os.listdir(lit_dir)
                 if re.match(r'(?:StructBioCADD_CellBio|AIDD)_scan_\d{4}-\d{2}-\d{2}\.md$', f)],
                reverse=True
            )
            if candidates:
                default = os.path.join(lit_dir, candidates[0])
            else:
                return
        self._file_var.set(default)
        self._load_report()

    # ── 文件操作 ───────────────────────────────────────────
    def _browse_file(self):
        lit_dir = os.path.dirname(os.path.abspath(__file__))
        path = filedialog.askopenfilename(
            parent=self,
            title="选择扫描报告",
            initialdir=lit_dir,
            filetypes=[("Markdown", "*.md"), ("所有文件", "*.*")]
        )
        if path:
            self._file_var.set(path)
            self._load_report()

    def _load_report(self):
        path = self._file_var.get().strip()
        if not path or not os.path.isfile(path):
            messagebox.showwarning("文件不存在", f"找不到报告文件:\n{path}", parent=self)
            return
        try:
            from parse_scan import parse_scan_report
            self._papers = parse_scan_report(path)
        except ImportError:
            lit_dir = os.path.dirname(os.path.abspath(__file__))
            messagebox.showerror(
                "缺少模块",
                f"找不到 parse_scan.py。\n\n"
                f"请将 parse_scan.py 放置到以下目录后重试：\n{lit_dir}",
                parent=self
            )
            return
        except Exception as e:
            messagebox.showerror("解析失败", str(e), parent=self)
            return
        self._populate_tree()
        self._count_label.config(text=f"共找到 {len(self._papers)} 篇论文")
        self._set_status("")

    # ── 列表填充 ───────────────────────────────────────────
    def _populate_tree(self):
        self._tree.delete(*self._tree.get_children())
        self._item_checks.clear()
        for p in self._papers:
            preprint_tag = '预印本' if p.is_preprint else '期刊'
            iid = self._tree.insert('', tk.END, values=(
                self.CHECK_ON if p.selected else self.CHECK_OFF,
                p.title[:80],
                p.source[:30],
                p.category_code,
                p.date,
                preprint_tag,
            ))
            self._item_checks[iid] = p.selected

    # ── 复选框交互 ─────────────────────────────────────────
    def _on_click(self, event):
        region = self._tree.identify_region(event.x, event.y)
        col    = self._tree.identify_column(event.x)
        iid    = self._tree.identify_row(event.y)
        if region == 'cell' and col == '#1' and iid:
            self._toggle(iid)

    def _toggle(self, iid):
        current = self._item_checks.get(iid, True)
        new_val = not current
        self._item_checks[iid] = new_val
        vals = list(self._tree.item(iid, 'values'))
        vals[0] = self.CHECK_ON if new_val else self.CHECK_OFF
        self._tree.item(iid, values=vals)
        # 同步到 paper 对象
        idx = list(self._tree.get_children()).index(iid)
        if 0 <= idx < len(self._papers):
            self._papers[idx].selected = new_val

    def _select_all(self):
        for iid in self._tree.get_children():
            self._item_checks[iid] = True
            vals = list(self._tree.item(iid, 'values'))
            vals[0] = self.CHECK_ON
            self._tree.item(iid, values=vals)
        for p in self._papers:
            p.selected = True

    def _deselect_all(self):
        for iid in self._tree.get_children():
            self._item_checks[iid] = False
            vals = list(self._tree.item(iid, 'values'))
            vals[0] = self.CHECK_OFF
            self._tree.item(iid, values=vals)
        for p in self._papers:
            p.selected = False

    # ── 详情展示 ───────────────────────────────────────────
    def _on_select(self, _event):
        sel = self._tree.selection()
        if not sel:
            return
        iid = sel[0]
        idx = list(self._tree.get_children()).index(iid)
        if 0 <= idx < len(self._papers):
            p = self._papers[idx]
            text = (f"标题：{p.title}\n"
                    f"作者：{p.authors}\n"
                    f"来源：{p.source}  URL：{p.url}\n"
                    f"方法：{p.method_highlight}")
            self._detail_text.config(state=tk.NORMAL)
            self._detail_text.delete(1.0, tk.END)
            self._detail_text.insert(tk.END, text)
            self._detail_text.config(state=tk.DISABLED)

    # ── 入库辅助 ───────────────────────────────────────────
    def _insert_paper_to_db(self, p, file_path: str) -> bool:
        """将 ScannedPaper 写入 literature.db，已存在则跳过（按 DOI 或标题去重）"""
        conn = get_db_conn()
        c = conn.cursor()
        try:
            if p.doi:
                c.execute('SELECT id FROM papers WHERE doi=?', (p.doi,))
                if c.fetchone():
                    return False   # 已存在
            else:
                c.execute('SELECT id FROM papers WHERE lower(title) = lower(?)', (p.title,))
                if c.fetchone():
                    return False

            year = p.date[:4] if p.date and len(p.date) >= 4 else ''
            tags = f"{p.category_code}; {p.source}"
            c.execute('''INSERT INTO papers
                (title, authors, abstract, keywords, doi, year,
                 file_path, page_count, added_date, tags, category, methods, innovations)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (p.title, p.authors, '', '', p.doi, year,
                 file_path, 0, datetime.now().isoformat(),
                 tags, p.category_name, p.method_highlight, ''))
            conn.commit()
            return True
        finally:
            conn.close()

    def _selected_papers(self):
        return [p for p in self._papers if p.selected]

    def _set_status(self, msg: str):
        self._status_label.config(text=msg)
        self.update_idletasks()

    # ── 仅导入元数据 ────────────────────────────────────────
    def _import_metadata_only(self):
        selected = self._selected_papers()
        if not selected:
            messagebox.showinfo("提示", "请先勾选论文。", parent=self)
            return
        added = skipped = 0
        for p in selected:
            ok = self._insert_paper_to_db(p, p.url or '')
            if ok:
                added += 1
            else:
                skipped += 1
        if self.on_import_done:
            self.on_import_done()
        messagebox.showinfo("导入完成",
                            f"元数据导入完成：新增 {added} 篇，跳过重复 {skipped} 篇。",
                            parent=self)

    # ── 复制链接 ────────────────────────────────────────────
    def _copy_links(self):
        selected = self._selected_papers()
        if not selected:
            messagebox.showinfo("提示", "请先勾选论文。", parent=self)
            return
        text = '\n'.join(
            f"{p.title}\n  {p.url}" for p in selected if p.url
        )
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("已复制", f"已复制 {len(selected)} 篇论文链接到剪贴板。", parent=self)

    # ── 下载并导入（后台线程）──────────────────────────────
    def _download_and_import(self):
        selected = self._selected_papers()
        if not selected:
            messagebox.showinfo("提示", "请先勾选论文。", parent=self)
            return

        pdf_dir = PDF_STORAGE
        total = len(selected)
        self._progress['maximum'] = total
        self._progress['value'] = 0

        def worker():
            added = skipped = failed = 0
            for i, p in enumerate(selected):
                self.after(0, lambda i=i, t=p.title[:40]: self._set_status(
                    f"[{i+1}/{total}] {t}..."))
                try:
                    from download_papers import download_paper
                    ok, result = download_paper(
                        p.source_type, p.arxiv_id, p.doi, p.url,
                        p.title, pdf_dir,
                        callback=lambda s: self.after(0, lambda s=s: self._set_status(s))
                    )
                except ImportError:
                    lit_dir = os.path.dirname(os.path.abspath(__file__))
                    ok, result = False, f"找不到 download_papers.py，请将其放至：{lit_dir}"

                local_path = result if ok else (p.url or '')
                inserted = self._insert_paper_to_db(p, local_path)

                if inserted:
                    added += 1
                else:
                    skipped += 1
                if not ok:
                    failed += 1

                self.after(0, lambda v=i+1: self._progress.config(value=v))

            summary = f"完成：新增 {added} 篇，跳过重复 {skipped} 篇，PDF下载失败 {failed} 篇（已保存元数据）。"
            self.after(0, lambda: self._set_status(summary))
            self.after(0, lambda: messagebox.showinfo("导入完成", summary, parent=self))
            if self.on_import_done:
                self.after(0, self.on_import_done)

        threading.Thread(target=worker, daemon=True).start()


def ask_api_key(root):
    global LLM_API_KEY

    if LLM_API_KEY:
        return True

    key = simpledialog.askstring(
        f"{CURRENT_MODEL_NAME} API Key",
        f"请输入 {CURRENT_MODEL_NAME} 的 API Key：",
        parent=root,
        show="*"
    )

    if not key:
        messagebox.showwarning("未设置 API Key", "未输入 API Key，AI 分析功能将不可用。")
        return False

    LLM_API_KEY = key.strip()
    remember_api_key_for_current_model(LLM_API_KEY)
    return True


def main():
    init_db()
    root = ctk.CTk()
    set_app_icon(root)
    ask_api_key(root)
    app = LiteratureManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
