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

APP_ICON_NAME = "app_icon.ico"
APP_ICON_SOURCE_PNG = ""

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

def set_app_icon(root):
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
                    if name == "_apikeys_":
                        continue
                    if isinstance(cfg, dict) and name not in DEFAULT_MODEL_CONFIGS:
                        configs[name] = {
                            "model": (cfg.get("model") or name).strip(),
                            "base_url": (cfg.get("base_url") or "https://api.deepseek.com/v1").strip(),
                            "api_key_env": (cfg.get("api_key_env") or "").strip(),
                            "api_key": (cfg.get("api_key") or "").strip()
                        }

                saved_keys = saved.get("_apikeys_", {})
                if isinstance(saved_keys, dict):
                    for name, key in saved_keys.items():
                        if name in configs and key:
                            configs[name]["api_key"] = key.strip()
        except Exception:
            pass
    return configs

def save_model_configs():
    out: dict = {
        name: cfg for name, cfg in MODEL_CONFIGS.items()
        if name not in DEFAULT_MODEL_CONFIGS
    }

    default_keys = {
        name: MODEL_CONFIGS[name]["api_key"]
        for name in DEFAULT_MODEL_CONFIGS
        if MODEL_CONFIGS.get(name, {}).get("api_key")
    }
    if default_keys:
        out["_apikeys_"] = default_keys
    with open(MODEL_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    try:
        os.chmod(MODEL_CONFIG_PATH, 0o600)
    except OSError:
        pass

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
LLM_THINKING_MODE = False

def apply_model_config(model_name):
    global CURRENT_MODEL_NAME, LLM_MODEL, LLM_BASE_URL, LLM_API_KEY, LLM_THINKING_MODE
    if model_name not in MODEL_CONFIGS:
        model_name = "deepseek-v4-pro"
    cfg = MODEL_CONFIGS[model_name]
    CURRENT_MODEL_NAME = model_name
    LLM_MODEL = (cfg.get("model") or model_name).strip()
    LLM_BASE_URL = (cfg.get("base_url") or "https://api.deepseek.com/v1").strip().rstrip("/")
    LLM_THINKING_MODE = bool(cfg.get("thinking", False))

    env_name = (cfg.get("api_key_env") or "").strip()
    env_key = os.environ.get(env_name, "").strip() if env_name else ""
    configured_key = (cfg.get("api_key") or "").strip()
    generic_key = os.environ.get("LLM_API_KEY", "").strip()
    LLM_API_KEY = env_key or configured_key or generic_key
    return cfg

def remember_api_key_for_current_model(api_key):
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

DEFAULT_CATEGORIES = [

    "蛋白质结构解析", "核酸结构", "复合物结构", "结构解析方法",
    "蛋白质-配体相互作用", "蛋白质-蛋白质相互作用", "构象动力学",

    "分子对接", "虚拟筛选", "药效团建模", "QSAR模型",
    "分子动力学模拟", "ADMET预测", "结合自由能计算",

    "细胞信号通路", "细胞周期与增殖", "细胞凋亡与死亡",
    "细胞分化与发育", "细胞成像与分析", "基因表达调控",

    "其他"
]

def get_db_conn():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA busy_timeout=5000')
    return conn

def init_db():
    conn = get_db_conn()
    try:
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

        c.execute("PRAGMA table_info(papers)")
        existing_cols = {row[1] for row in c.fetchall()}
        for col, definition in [
            ("doi",           "TEXT DEFAULT ''"),
            ("year",          "TEXT DEFAULT ''"),
            ("tags",          "TEXT DEFAULT ''"),
            ("category",      "TEXT DEFAULT ''"),
            ("methods",       "TEXT DEFAULT ''"),
            ("innovations",   "TEXT DEFAULT ''"),
            ("read_status",   "TEXT DEFAULT 'unread'"),
            ("personal_notes","TEXT DEFAULT ''"),
        ]:
            if col not in existing_cols:
                c.execute(f"ALTER TABLE papers ADD COLUMN {col} {definition}")

        c.execute("CREATE INDEX IF NOT EXISTS idx_papers_lower_title ON papers (lower(title))")
        c.execute("CREATE INDEX IF NOT EXISTS idx_papers_category ON papers (category)")

        for cat in DEFAULT_CATEGORIES:
            c.execute('INSERT OR IGNORE INTO categories (name) VALUES (?)', (cat,))

        conn.commit()
    finally:
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

def extract_text_from_pdf(pdf_path, max_pages=5):
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

    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        line = line.strip()

        if line.isdigit():
            continue

        if len(line) < 5 and line.isupper():
            continue
        cleaned_lines.append(line)
    cleaned_text = '\n'.join(cleaned_lines)

    patterns = [

        r'(?i)abstract[\s:]*\n(.*?)(?=\n\s*(?:introduction|1\s+introduction|background|i\s+introduction|methods|materials))',

        r'(?i)abstract[\s:]*(.{100,8000}?)(?=\n\s*(?:introduction|background|methods|keywords|key\s+words))',

        r'(?i)摘要[\s:]*\n(.*?)(?=\n\s*(?:关键词|引言|1\s|背景|方法))',

        r'(?i)abstract\s*[-–—]\s*(.{100,8000}?)(?=\n\s*\d+\s|\n\s*introduction|\n\s*keywords)',

        r'(?i)(^.{100,3000}?)\n\s*(?=introduction|background|1\s|methods)',
    ]

    for pattern in patterns:
        match = re.search(pattern, cleaned_text, re.DOTALL)
        if match:
            abstract = match.group(1).strip()

            abstract = re.sub(r'\n+', ' ', abstract)
            abstract = re.sub(r'\s+', ' ', abstract)

            abstract = re.sub(r'(?i)\b(journal|vol\.|no\.|pp\.|doi|copyright)\b[^.]*\.?', '', abstract)
            abstract = abstract.strip()
            if len(abstract) > 50:
                return abstract[:5000]

    paragraphs = [p.strip() for p in cleaned_text.split('\n\n') if len(p.strip()) > 100]
    if paragraphs:

        fallback = paragraphs[0].replace('\n', ' ')
        return fallback[:2000]

    fallback = cleaned_text[:1500].replace('\n', ' ')
    return fallback

def extract_keywords(text):
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

    cleaned = re.sub(r'[\u200b\u200c\u200d\ufeff\u00ad]', '', text)

    _STRIP = '.,;:）)》》」\'"'

    def _find_doi(sample):

        m = re.search(r'https?://(?:dx\.)?doi\.org/(10\.\d{4,}/\S+)', sample, re.IGNORECASE)
        if m:
            return m.group(1).rstrip(_STRIP)

        m = re.search(r'(?<![\w/])doi[:\s/]+(10\.\d{4,}/\S+)', sample, re.IGNORECASE)
        if m:
            return m.group(1).rstrip(_STRIP)

        m = re.search(r'[\[(]?\s*DOI\s*[:\s]+\s*(10\.\d{4,}/\S+)', sample, re.IGNORECASE)
        if m:
            return m.group(1).rstrip(_STRIP + '])')

        m = re.search(r'dx\.doi\.org/(10\.\d{4,}/\S+)', sample, re.IGNORECASE)
        if m:
            return m.group(1).rstrip(_STRIP)

        m = re.search(r'\b(10\.\d{4,6}/[^\s,;\]）》」\'"\)]+)', sample)
        if m:
            candidate = m.group(1).rstrip(_STRIP)

            if '/' in candidate and len(candidate) > 8:
                return candidate
        return ''

    for sample in (cleaned[:5000], cleaned[:15000], cleaned[:30000]):
        result = _find_doi(sample)
        if result:
            return result

    m = re.search(r'(?:doi\.org/|doi[:\s/]+)(10\.\d{4,}/\S+)', cleaned, re.IGNORECASE)
    if m:
        return m.group(1).rstrip(_STRIP)

    return ''

def extract_authors_from_text(text):

    sample = text[:5000]
    lines = [l.strip() for l in sample.split('\n') if l.strip()]

    AFFIL_KEYWORDS = {
        'university', 'institute', 'department', 'laboratory', 'school',
        'college', 'hospital', 'center', 'centre', 'faculty',
        'academy', 'research', 'national', 'science', 'technology',
        'biological', 'medical', 'pharmaceutical', 'chemistry',
        'bioengineering', 'computational', 'genomics', 'proteomics',
        '大学', '学院', '研究院', '研究所', '实验室', '医院', '中心',
        '科室', '生物', '医学', '药学院', '生命科学'
    }

    SKIP_KEYWORDS = {
        'abstract', 'introduction', 'methods', 'results', 'conclusion',
        'keywords', 'background', 'discussion', 'received', 'accepted',
        'published', 'journal', 'doi', 'correspondence', 'email',
        'figure', 'table', 'copyright', 'license', 'arxiv', 'preprint',
        'vol', 'no.', 'pp.', 'page', 'supplementary', 'appendix'
    }

    def _is_affiliation_line(line):
        lower = line.lower()
        if '@' in line:
            return True
        if 'http' in lower or 'www.' in lower:
            return True

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

        cleaned = re.sub(r'\s*[\(\[]?\d+(?:[,，\s]+\d+)*[\)\]]?', '', line)

        cleaned = re.sub(r'\s*\*+', '', cleaned)

        cleaned = re.sub(r'(?i)\s*orcid[:\s]*\d{4}-\d{4}-\d{4}-\d{3}[\dX]', '', cleaned)

        cleaned = re.sub(r'(?i)these\s+authors\s+contributed.*', '', cleaned)
        cleaned = re.sub(r'(?i)equal\s+contribution.*', '', cleaned)

        cleaned = cleaned.rstrip(',; ')

        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned

    for i, line in enumerate(lines):
        if re.match(r'(?i)^(authors?|作者)\s*[:：]', line):
            rest = re.sub(r'(?i)^(authors?|作者)\s*[:：]\s*', '', line).strip()
            if rest and len(rest) > 3:
                return _clean_author_line(rest)[:300]
            if i + 1 < len(lines):
                nxt = lines[i + 1].strip()
                if nxt and len(nxt) > 3 and not _is_affiliation_line(nxt):
                    return _clean_author_line(nxt)[:300]

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

        cleaned_for_match = _clean_author_line(line)
        if AUTHOR_PAT.match(cleaned_for_match):
            cleaned = cleaned_for_match
            if len(cleaned) > 5:

                if re.match(r'^[A-Z\.\s,;]+$', cleaned):
                    continue
                cleaned_upper = cleaned.rstrip('.;, ').upper()

                if cleaned_upper in COUNTRY_NAMES:
                    continue
                if any(cleaned_upper.endswith(cn) for cn in COUNTRY_NAMES if len(cn) > 2):
                    continue
                candidates.append(cleaned)

    if candidates:
        return max(candidates, key=len)[:300]

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

    cr_titles = item.get('title', [])
    cr_title = cr_titles[0] if cr_titles else ''

    def _words(t):
        return set(w.lower() for w in re.findall(r'[a-zA-Z0-9]+', t) if len(w) > 2)

    sw_q, sw_cr = _words(title), _words(cr_title)
    if sw_q and sw_cr:
        overlap = len(sw_q & sw_cr) / max(len(sw_q), len(sw_cr))
        if overlap < 0.45:
            return {}

    result = {}

    doi = (item.get('DOI') or '').strip()
    if doi:
        result['doi'] = doi

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

    for pub_key in ('published', 'published-print'):
        pub = item.get(pub_key) or {}
        parts = pub.get('date-parts', [[]])
        if parts and parts[0]:
            result['year'] = str(parts[0][0])
            break

    return result

def extract_year_from_text(text):
    match = re.search(r'\b(20[0-2]\d|199\d)\b', text[:3000])
    return match.group(1) if match else ''

def extract_year_from_metadata(metadata):
    for key in ('creationDate', 'modDate'):
        val = (metadata.get(key) or '').strip()
        m = re.search(r'(20[0-2]\d|199\d)', val)
        if m:
            return m.group(1)
    return ''

def get_all_tags():
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
    lines = [l.strip() for l in text.split('\n') if l.strip()]

    skip_patterns = [
        'journal', 'vol.', 'pp.', 'doi', 'http', '@',
        'university', 'institute', 'department', 'correspond',
        'received', 'accepted', 'published', 'copyright',
        'figure', 'table', 'supplementary', 'appendix',
        'page', 'www.', 'email', 'tel:', 'fax:'
    ]

    candidates = []
    for i, line in enumerate(lines[:15]):

        if len(line) < 15:
            continue

        if any(x in line.lower() for x in skip_patterns):
            continue

        if line.isupper() and len(line) > 30:
            continue

        if line.replace(' ', '').isdigit():
            continue

        if sum(c.isdigit() for c in line) / len(line) > 0.3:
            continue

        score = 0
        if 30 <= len(line) <= 200:
            score += 10
        if len(line) > 20:
            score += 5

        words = line.split()
        capitalized = sum(1 for w in words if w and w[0].isupper())
        if capitalized >= 2:
            score += 5

        if not line[-1] in '.,;:!?':
            score += 3

        score += max(0, 5 - i)

        candidates.append((score, line))

    if candidates:
        candidates.sort(reverse=True)
        return candidates[0][1]

    for line in lines[:10]:
        if len(line) > 20:
            return line
    return ""

def call_llm(system_prompt, user_prompt, max_tokens=2000, temperature=0.3, timeout=60):
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

def call_llm_ext(system_prompt, user_prompt, max_tokens=2000, temperature=0.3, timeout=60):
    if not LLM_API_KEY:
        return None, f"未设置 {CURRENT_MODEL_NAME} API Key", None

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
        if LLM_THINKING_MODE:
            data["thinking"] = {"type": "enabled"}
            data["reasoning_effort"] = "high"

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
            choice = result['choices'][0]
            return choice['message']['content'], None, choice.get('finish_reason', 'stop')

    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='ignore')[:200]
        return None, f"HTTP {e.code}：{body}", None
    except urllib.error.URLError as e:
        return None, f"网络错误：{e.reason}", None
    except Exception as e:
        return None, str(e), None

def call_llm_long(system_prompt, user_prompt, max_tokens=4000,
                  temperature=0.3, timeout=120, max_rounds=3):
    import urllib.request
    import urllib.error

    if not LLM_API_KEY:
        return None, f"未设置 {CURRENT_MODEL_NAME} API Key"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": user_prompt},
    ]
    full_content = ""

    for _ in range(max_rounds):
        try:
            data = {
                "model": LLM_MODEL,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
            }
            if LLM_THINKING_MODE:
                data["thinking"] = {"type": "enabled"}
                data["reasoning_effort"] = "high"

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
            choice = result["choices"][0]
            chunk = choice["message"]["content"] or ""
            full_content += chunk

            if choice.get("finish_reason") != "length":
                return full_content, None

            messages.append({"role": "assistant", "content": chunk})
            messages.append({"role": "user", "content": "请继续。"})

        except urllib.error.HTTPError as e:
            err = f"HTTP {e.code}：{e.read().decode('utf-8', errors='ignore')[:200]}"
            return full_content or None, err
        except urllib.error.URLError as e:
            return full_content or None, f"网络错误：{e.reason}"
        except Exception as e:
            return full_content or None, str(e)

    return full_content, None

def analyze_paper(title, abstract, keywords, categories):
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

        content = re.sub(r'^```json\s*', '', content)
        content = re.sub(r'```\s*$', '', content)
        result = json.loads(content.strip())

        if result.get('category') not in categories:
            result['category'] = '其他'

        recommended = result.get('recommended_category', '').strip()
        if result.get('category') == '其他' and recommended:
            add_category(recommended)
            result['category'] = recommended
            result['recommended_category'] = ''

        return result
    except json.JSONDecodeError:

        return {
            "category": extract_field(content, "category") or "未分类",
            "recommended_category": extract_field(content, "recommended_category") or "",
            "methods": extract_field(content, "methods") or content[:500],
            "innovations": extract_field(content, "innovations") or "",
            "keywords_enhanced": extract_field(content, "keywords_enhanced") or ""
        }

def extract_field(text, field):
    pattern = rf'"{field}"\s*:\s*"([^"]*)"'
    match = re.search(pattern, text)
    if match:
        return match.group(1)

    pattern = rf"'{field}'\s*:\s*'([^']*)'"
    match = re.search(pattern, text)
    return match.group(1) if match else None

def llm_extract_title_abstract(text, filename):

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

        title = extract_field(content, "title") or ""
        abstract = extract_field(content, "abstract") or ""
        if title or abstract:
            return {"title": title, "abstract": abstract}
        return None

def llm_full_analysis(text, filename, keywords, categories):
    categories_str = "\n".join([f"- {c}" for c in categories])

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

        if result.get('category') not in categories:
            result['category'] = '其他'

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

def fetch_papers_for_suggestion(paper_ids):
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
    text = re.sub(r'\s+', ' ', text or '').strip()
    if not text:
        return []
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def summarize_paper_chunk(paper, chunk, chunk_idx, total_chunks, research_topic=""):
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
    categories = set(p['category'] for p in papers_data if p['category'] != '未分类')
    if len(categories) >= 5:
        cats_str = '、'.join(list(categories)[:4]) + '等'
        return (f"注意：所选论文涉及 {len(categories)} 个不同分类（{cats_str}），"
                "请重点关注方法层面的可迁移性，并在每个建议中说明如何整合不同领域的技术。")
    return ""

def get_paper_combinations(n):
    from itertools import combinations as _comb
    MAX_TOTAL = 20
    MIN_SLOTS = 6

    if n == 2:
        return [[1, 2] for _ in range(4)]

    result = []

    full_combo = list(range(1, n + 1))
    result.append(full_combo)

    for size in range(n - 1, 1, -1):
        for combo in _comb(range(1, n + 1), size):
            result.append(list(combo))
            if len(result) >= MAX_TOTAL - 1:
                break
        if len(result) >= MAX_TOTAL - 1:
            break

    base_subsets = [c for c in result if len(c) < n] or [full_combo]
    i = 0
    while len(result) < min(MAX_TOTAL, max(MIN_SLOTS, len(result))):
        result.append(list(base_subsets[i % len(base_subsets)]))
        i += 1
    return result[:MAX_TOTAL]

def build_combination_prompt(papers_data, combinations, divergence_warning="", research_topic=""):
    n = len(papers_data)
    research_topic = (research_topic or "").strip()

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

    cats = list({p.get('category', '') for _, p in selected if p.get('category')})
    cat_key = cats[0] if cats else "交叉研究"

    title_words = []
    for _, p in selected:
        t = (p.get('title') or '').strip()

        words = re.findall(r'[A-Z]{2,}|[一-鿿]{2,4}', t)
        title_words.extend(words[:2])

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

    target_min = max(6, n + 2)
    added = 0
    candidate_combos = [normalize_combination(c, n) for c in combinations]
    candidate_combos = [c for c in candidate_combos if len(c) >= 2]

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
    data, warning = parse_suggestion_response(raw_text)
    return ensure_suggestion_coverage(
        data or [], papers_data, combinations, warning, research_topic
    )

def build_suggestion_prompt(papers_data, n_suggestions, divergence_warning=""):
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
    if not raw_text:
        return None, "LLM返回空响应"

    text = re.sub(r'```(?:json)?\s*', '', raw_text).strip()

    try:
        data = json.loads(text)
        if isinstance(data, list) and data:
            return data, None
        if isinstance(data, dict):
            return [data], None
    except json.JSONDecodeError:
        pass

    snippet = _extract_balanced(text, '[', ']')
    if snippet:
        try:
            data = json.loads(snippet)
            if isinstance(data, list) and data:
                return data, None
        except json.JSONDecodeError:
            pass

    snippet = _extract_balanced(text, '{', '}')
    if snippet:
        try:
            data = json.loads(snippet)
            if isinstance(data, dict):
                return [data], None
        except json.JSONDecodeError:
            pass

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
    if len(paper_ids) < 2:
        return None, "至少需要选择2篇论文"

    papers_data = fetch_papers_for_suggestion(paper_ids)
    if len(papers_data) < 2:
        return None, "有效论文不足2篇（部分ID在数据库中未找到或字段为空）"

    papers_data = enrich_papers_with_detailed_reports(papers_data, research_topic)
    divergence_warning = detect_domain_divergence(papers_data)
    n = len(papers_data)

    combinations = get_paper_combinations(n)

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

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)

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

        raw_frame = ttk.Frame(self.notebook)
        self.notebook.add(raw_frame, text="原始输出")
        self.raw_text = scrolledtext.ScrolledText(raw_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.raw_text.pack(fill=tk.BOTH, expand=True)

        btn_frame = ttk.Frame(self, padding=(10, 4, 10, 8))
        btn_frame.pack(fill=tk.X)
        ttk.Button(btn_frame, text="复制全部建议", command=self._copy_all).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="导出 Markdown", command=self._export_md).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="关闭", command=self.destroy).pack(side=tk.RIGHT, padx=4)

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

                lines = max(3, value.count('\n') + 1, len(value) // 60 + 1)
                lines = min(lines, 12)
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
    if not title:
        return True

    if len(title) < 10:
        return True

    if title == filename.replace('.pdf', ''):
        return True

    if sum(c.isdigit() for c in title) / len(title) > 0.3:
        return True

    bad_starts = ['vol.', 'page', 'chapter', 'section', 'figure', 'table', 'pp.']
    if any(title.lower().startswith(x) for x in bad_starts):
        return True
    return False

def is_bad_abstract(abstract, title=""):
    if not abstract:
        return True
    if len(abstract) < 50:
        return True
    if title and abstract.strip().lower() == title.strip().lower():
        return True
    return False

def check_duplicate(file_path):
    filename = os.path.basename(file_path)

    conn = get_db_conn()
    c = conn.cursor()

    c.execute("SELECT id FROM papers WHERE file_path LIKE ?", (f'%{filename}',))
    row = c.fetchone()
    if row:
        conn.close()
        return True, f"文件名重复: {filename}", row[0]

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

def add_paper_to_db(file_path, tags='', force=False):
    filename = os.path.basename(file_path)

    if not force:
        is_dup, reason, existing_id = check_duplicate(file_path)
        if is_dup:
            return None, f"重复文献 [{reason}] 已存在(ID: {existing_id})"

    dest_path = os.path.join(PDF_STORAGE, f"{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}_{filename}")
    shutil.copy2(file_path, dest_path)

    try:

        with fitz.open(dest_path) as doc:
            metadata = doc.metadata

        full_text = extract_text_from_pdf(dest_path)

        title = (metadata.get('title') or '').strip()
        if not title or len(title) < 5 or title == 'Unknown Title':
            title = extract_title_from_text(full_text) or filename.replace('.pdf', '')

        abstract = extract_abstract(full_text)
        keywords = extract_keywords(full_text)

        authors_pdf_meta = (metadata.get('author') or '').strip()
        authors_regex = extract_authors_from_text(full_text)

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

            for pat in _NON_AUTHOR_PATTERNS:
                if re.search(pat, s):
                    return False

            if not re.search(r'[A-Z][a-z]', s) and not re.search(r'[\u4e00-\u9fff]{2,}', s):
                return False

            s_upper = s.rstrip('.;, ').upper()
            if s_upper in COUNTRY_NAMES:
                return False
            if any(s_upper.endswith(cn) for cn in COUNTRY_NAMES if len(cn) > 2):
                return False

            words = s.split()
            title_like = sum(1 for w in words if w and w[0].isupper() and len(w) > 4)
            if title_like >= 4 and len(s) > 40 and ',' not in s:
                return False

            if ',' not in s and ';' not in s and ' and ' not in s.lower() and '&' not in s:

                if ' ' not in s:
                    return False

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

        categories = get_categories()
        analysis = None

        if LLM_API_KEY:
            analysis = llm_full_analysis(full_text, filename, keywords, categories)

            if analysis.get('title') and len(analysis['title']) > 5:
                title = analysis['title']

            if analysis.get('abstract') and len(analysis['abstract']) > 50:
                abstract = analysis['abstract']

            if analysis.get('year'):
                year = analysis['year']

            llm_authors = (analysis.get('authors') or '').strip()
            if _is_valid_author_string(llm_authors):
                authors = llm_authors

            llm_doi = (analysis.get('doi') or '').strip()
            if llm_doi and not doi:
                doi = llm_doi

        if not analysis:
            analysis = {"category": "未分类", "methods": "", "innovations": "", "keywords_enhanced": ""}

        def _count_authors(s):
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

        if authors:

            authors_stripped = authors.rstrip('.;, ').strip()
            if authors_stripped.isupper() and ' ' not in authors_stripped and ',' not in authors_stripped:
                authors = ''

            elif authors_stripped.upper() in COUNTRY_NAMES:
                authors = ''

        all_keywords = keywords
        if analysis.get('keywords_enhanced'):
            all_keywords = f"{keywords}; {analysis['keywords_enhanced']}" if keywords else analysis['keywords_enhanced']

        page_count = 0
        try:
            with fitz.open(dest_path) as doc_pc:
                page_count = len(doc_pc)
        except Exception:
            pass

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

class AskLibraryDialog(tk.Toplevel):

    _SAMPLE_QUESTIONS = [
        "有哪些常用的蛋白质-配体对接方法？",
        "cryo-EM 与 X 射线晶体学在结构解析上各有何优劣？",
        "分子动力学模拟如何评估结合自由能？",
        "这批论文中有哪些涉及 ADMET 预测与优化的研究？",
    ]

    def __init__(self, parent):
        super().__init__(parent)
        self.title("问文献 · RAG 语义问答")
        self.geometry("960x700")
        self.resizable(True, True)
        self._history: list = []
        self._last_question = ""
        self._build_ui()

    def _build_ui(self):

        ttk.Label(self, text="问文献  ·  本地语义问答（RAG）",
                  font=("Microsoft YaHei UI", 13, "bold")).pack(anchor="w", padx=12, pady=(10, 2))

        idx_row = ttk.Frame(self)
        idx_row.pack(fill=tk.X, padx=12, pady=2)
        self.idx_lbl = ttk.Label(idx_row, text="", foreground="gray")
        self.idx_lbl.pack(side=tk.LEFT)
        ttk.Button(idx_row, text="⟳ 建立/更新索引",
                   command=self._rebuild_index).pack(side=tk.LEFT, padx=8)
        self._refresh_index_status()

        mode_row = ttk.Frame(self)
        mode_row.pack(fill=tk.X, padx=12, pady=2)
        ttk.Label(mode_row, text="模式：").pack(side=tk.LEFT)
        self._deep_mode = tk.BooleanVar(value=False)
        ttk.Radiobutton(mode_row, text="快速问答",
                        variable=self._deep_mode, value=False).pack(side=tk.LEFT, padx=4)
        ttk.Radiobutton(mode_row, text="深度溯源（多跳检索·精确引用）",
                        variable=self._deep_mode, value=True).pack(side=tk.LEFT, padx=4)
        ttk.Label(mode_row, text="· 深度模式约 60-120s",
                  foreground="gray").pack(side=tk.LEFT)

        sample_row = ttk.Frame(self)
        sample_row.pack(fill=tk.X, padx=12, pady=2)
        ttk.Label(sample_row, text="示例：", foreground="gray").pack(side=tk.LEFT)
        for q in self._SAMPLE_QUESTIONS:
            short = q[:20] + "…" if len(q) > 20 else q
            ttk.Button(sample_row, text=short,
                       command=lambda _q=q: self._fill_sample(_q)).pack(side=tk.LEFT, padx=2)

        content = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        content.pack(fill=tk.BOTH, expand=True, padx=12, pady=(4, 0))

        left = ttk.Frame(content)
        content.add(left, weight=2)

        ttk.Label(left, text="历史问题",
                  foreground="gray").pack(anchor="w", padx=4, pady=(4, 0))
        self.history_lb = tk.Listbox(left, font=("Microsoft YaHei UI", 8), height=4)
        self.history_lb.pack(fill=tk.X, padx=4, pady=(2, 4))
        self.history_lb.bind("<<ListboxSelect>>", self._on_history_click)

        ttk.Separator(left).pack(fill=tk.X, padx=4)
        ttk.Label(left, text="检索到的相关论文",
                  font=("Microsoft YaHei UI", 10, "bold")).pack(anchor="w", padx=4, pady=(4, 2))
        plist_frame = ttk.Frame(left)
        plist_frame.pack(fill=tk.BOTH, expand=True)
        self.paper_listbox = tk.Listbox(plist_frame, font=("Microsoft YaHei UI", 9))
        sb_lv = ttk.Scrollbar(plist_frame, orient="vertical", command=self.paper_listbox.yview)
        sb_lh = ttk.Scrollbar(plist_frame, orient="horizontal", command=self.paper_listbox.xview)
        self.paper_listbox.configure(yscrollcommand=sb_lv.set, xscrollcommand=sb_lh.set)
        sb_lv.pack(side=tk.RIGHT, fill=tk.Y)
        sb_lh.pack(side=tk.BOTTOM, fill=tk.X)
        self.paper_listbox.pack(fill=tk.BOTH, expand=True, padx=(4, 0))

        right = ttk.Frame(content)
        content.add(right, weight=3)

        right_hdr = ttk.Frame(right)
        right_hdr.pack(fill=tk.X)
        ttk.Label(right_hdr, text="AI 回答",
                  font=("Microsoft YaHei UI", 10, "bold")).pack(side=tk.LEFT, padx=4, pady=(4, 2))
        self.conf_lbl = ttk.Label(right_hdr, text="", foreground="gray")
        self.conf_lbl.pack(side=tk.LEFT, padx=4)
        ttk.Button(right_hdr, text="复制",
                   command=self._copy_answer).pack(side=tk.RIGHT, padx=2, pady=2)
        ttk.Button(right_hdr, text="清除",
                   command=self._clear_all).pack(side=tk.RIGHT, padx=2, pady=2)

        txt_frame = ttk.Frame(right)
        txt_frame.pack(fill=tk.BOTH, expand=True)
        self.answer_text = tk.Text(txt_frame, font=("Microsoft YaHei UI", 10),
                                   wrap=tk.WORD, state=tk.DISABLED)
        sb_r = ttk.Scrollbar(txt_frame, orient="vertical", command=self.answer_text.yview)
        self.answer_text.configure(yscrollcommand=sb_r.set)
        self.answer_text.tag_configure("cite", foreground="#1565c0",
                                       font=("Microsoft YaHei UI", 10, "bold"))
        sb_r.pack(side=tk.RIGHT, fill=tk.Y)
        self.answer_text.pack(fill=tk.BOTH, expand=True, padx=(4, 0), pady=(0, 4))

        q_row = ttk.Frame(self)
        q_row.pack(fill=tk.X, padx=12, pady=(4, 8))
        self.q_entry = ttk.Entry(q_row, font=("Microsoft YaHei UI", 12))
        self.q_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.q_entry.bind("<Return>", lambda _: self._ask())
        self.ask_btn = ttk.Button(q_row, text="提问", command=self._ask)
        self.ask_btn.pack(side=tk.LEFT, padx=(8, 0))

    def _refresh_index_status(self):
        try:
            import rag_engine
            t = rag_engine.index_mtime()
            if t == 0.0:
                self.idx_lbl.configure(
                    text="索引：未建立  ← 请点击「建立/更新索引」（首次约下载 570 MB 模型）",
                    foreground="orange")
            else:
                from datetime import datetime as _dt
                dt = _dt.fromtimestamp(t).strftime("%Y-%m-%d %H:%M")
                self.idx_lbl.configure(text=f"索引时间：{dt}  模型：bge-m3",
                                       foreground="gray")
        except ImportError:
            self.idx_lbl.configure(text="rag_engine 未找到", foreground="red")

    def _rebuild_index(self):
        self.ask_btn.configure(state=tk.DISABLED)
        self.idx_lbl.configure(
            text="正在初始化 bge-m3 模型（首次使用需下载约 570 MB，请耐心等待）…",
            foreground="orange")

        def task():
            try:
                import rag_engine
            except ImportError as _ie:
                self.after(0, lambda: self.idx_lbl.configure(
                    text=f"rag_engine 未安装，无法建立索引：{_ie}", foreground="red"))
                self.after(0, lambda: self.ask_btn.configure(state=tk.NORMAL))
                return
            n, err = rag_engine.build_index(DB_PATH)
            if err:
                self.after(0, lambda: self.idx_lbl.configure(
                    text=f"失败：{err}", foreground="red"))
            else:
                self.after(0, lambda: self.idx_lbl.configure(
                    text=f"索引完成，共 {n} 篇", foreground="green"))
            self.after(0, lambda: self.ask_btn.configure(state=tk.NORMAL))
            self.after(0, self._refresh_index_status)

        threading.Thread(target=task, daemon=True).start()

    def _fill_sample(self, q: str):
        self.q_entry.delete(0, tk.END)
        self.q_entry.insert(0, q)

    def _ask(self):
        q = self.q_entry.get().strip()
        if not q:
            return
        self._last_question = q
        deep = self._deep_mode.get()
        self.ask_btn.configure(state=tk.DISABLED, text="思考中…")
        self.conf_lbl.configure(text="")
        self.paper_listbox.delete(0, tk.END)
        hint = ("深度溯源：多跳检索 → 精确引用，约 60-120s…"
                if deep else "正在检索文献并生成回答，请稍候…")
        self._set_answer(hint)

        def task():
            try:
                import rag_engine
            except ImportError as _ie:
                self.after(0, lambda: self._set_answer(
                    f"rag_engine 模块未安装，无法使用 RAG 问答功能。\n错误：{_ie}"))
                self.after(0, lambda: self.ask_btn.configure(state=tk.NORMAL, text="提问"))
                return
            try:
                if deep:
                    answer, papers, confidence, err = rag_engine.deep_ask(q, call_llm_long)
                else:
                    answer, papers, err = rag_engine.ask(q, call_llm_long)
                    confidence = rag_engine._compute_confidence(papers) if papers else 0.0
            except Exception as _ex:
                self.after(0, lambda: self._set_answer(f"检索出错：{_ex}"))
                self.after(0, lambda: self.ask_btn.configure(state=tk.NORMAL, text="提问"))
                return
            if err:
                self.after(0, lambda: self._set_answer(f"错误：{err}"))
                self.after(0, lambda: self.conf_lbl.configure(text=""))
            else:
                ans_snap = answer
                papers_snap = list(papers)
                conf_snap = confidence
                self.after(0, lambda: self._show_results(ans_snap, papers_snap, conf_snap))
                self.after(0, lambda: self._add_history(q, ans_snap, papers_snap, conf_snap))
            self.after(0, lambda: self.ask_btn.configure(state=tk.NORMAL, text="提问"))

        threading.Thread(target=task, daemon=True).start()

    def _set_answer(self, text: str):
        self.answer_text.configure(state=tk.NORMAL)
        self.answer_text.delete("1.0", tk.END)
        self.answer_text.insert("1.0", text)
        self.answer_text.configure(state=tk.DISABLED)
        self.answer_text.see("1.0")

    def _show_results(self, answer: str, papers: list, confidence: float):

        if confidence > 0:
            pct = int(confidence * 100)
            self.conf_lbl.configure(text=f"相关度 {pct}%")

        self.paper_listbox.delete(0, tk.END)
        for i, p in enumerate(papers, 1):
            title = p.get("title", "")[:60]
            score = p.get("rerank_score") or p.get("score", 0.0)
            self.paper_listbox.insert(tk.END, f"[{i}] {title}  ({score:.2f})")

        self.answer_text.configure(state=tk.NORMAL)
        self.answer_text.delete("1.0", tk.END)

        import re as _re
        parts = _re.split(r'(\[\d+\])', answer or "")
        for part in parts:
            if _re.match(r'^\[\d+\]$', part):
                self.answer_text.insert(tk.END, part, "cite")
            else:
                self.answer_text.insert(tk.END, part)
        self.answer_text.configure(state=tk.DISABLED)
        self.answer_text.see("1.0")

    def _add_history(self, q, answer, papers, confidence):
        self._history.append((q, answer, papers, confidence))
        short = q[:30] + ("…" if len(q) > 30 else "")
        self.history_lb.insert(0, short)

    def _on_history_click(self, event=None):
        sel = self.history_lb.curselection()
        if not sel:
            return
        idx = sel[0]
        if idx >= len(self._history):
            return
        q, answer, papers, confidence = self._history[-(idx + 1)]
        self.q_entry.delete(0, tk.END)
        self.q_entry.insert(0, q)
        self._show_results(answer, papers, confidence)

    def _copy_answer(self):
        self.answer_text.configure(state=tk.NORMAL)
        text = self.answer_text.get("1.0", tk.END).strip()
        self.answer_text.configure(state=tk.DISABLED)
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            messagebox.showinfo("已复制", "回答已复制到剪贴板。", parent=self)

    def _clear_all(self):
        self.q_entry.delete(0, tk.END)
        self._set_answer("")
        self.paper_listbox.delete(0, tk.END)
        self.conf_lbl.configure(text="")

class PaperCritiqueDialog(tk.Toplevel):

    def __init__(self, parent, paper_id: int):
        super().__init__(parent)
        self.paper_id = paper_id
        self._paper_info = {}

        conn = get_db_conn()
        c = conn.cursor()
        c.execute(
            "SELECT title, authors, abstract, methods, innovations, year, category "
            "FROM papers WHERE id=?", (paper_id,)
        )
        row = c.fetchone()
        conn.close()

        if not row:
            messagebox.showerror("错误", "找不到该论文", parent=parent)
            self.destroy()
            return

        title, authors, abstract, methods, innovations, year, category = row
        self._paper_info = {
            "title": title or "无标题",
            "authors": authors or "",
            "abstract": abstract or "",
            "methods": methods or "",
            "innovations": innovations or "",
            "year": year or "",
            "category": category or "",
        }

        self.title(f"深度点评 — {(title or '')[:50]}")
        self.geometry("840x660")
        self.resizable(True, True)
        self._build_ui()

    def _build_ui(self):
        p = self._paper_info

        ttk.Label(self, text="深度点评  ·  AI 论文评审",
                  font=("Microsoft YaHei UI", 13, "bold")).pack(anchor="w", padx=12, pady=(10, 2))

        info_frame = ttk.LabelFrame(self, text="论文信息", padding=6)
        info_frame.pack(fill=tk.X, padx=12, pady=(4, 0))
        ttk.Label(info_frame, text=p["title"],
                  font=("Microsoft YaHei UI", 11, "bold"),
                  wraplength=780, justify="left").pack(anchor="w")
        ttk.Label(
            info_frame,
            text=f"{p['authors'][:80]}  {p['year']}  [{p['category']}]",
            foreground="gray"
        ).pack(anchor="w", pady=(2, 0))

        btn_row = ttk.Frame(self)
        btn_row.pack(fill=tk.X, padx=12, pady=6)
        self.critique_btn = ttk.Button(
            btn_row, text="▶ 开始深度点评", command=self._run_critique)
        self.critique_btn.pack(side=tk.LEFT)
        self.status_lbl = ttk.Label(btn_row, text="", foreground="gray")
        self.status_lbl.pack(side=tk.LEFT, padx=12)
        ttk.Button(btn_row, text="复制", command=self._copy_result).pack(side=tk.RIGHT)

        result_frame = ttk.Frame(self)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))
        self.result_text = tk.Text(
            result_frame, font=("Microsoft YaHei UI", 10),
            wrap=tk.WORD, state=tk.DISABLED, padx=8, pady=6)
        sb = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.pack(fill=tk.BOTH, expand=True)

    def _build_critique_prompt(self) -> str:
        p = self._paper_info
        return (
            f"请对以下结构生物学/CADD/细胞生物学领域论文进行结构化深度点评，用简体中文输出。\n\n"
            f"【论文信息】\n"
            f"标题：{p['title']}\n"
            f"作者：{p['authors']}\n"
            f"年份：{p['year']}  分类：{p['category']}\n"
            f"摘要：{p['abstract'][:800]}\n"
            f"核心方法：{p['methods'][:600]}\n"
            f"创新点：{p['innovations'][:400]}\n\n"
            f"---\n\n"
            f"请按以下五个维度逐一评审，每项给出详细分析（不少于3句话）：\n\n"
            f"## 一、总体评价\n"
            f"（本文的整体贡献、在结构生物学/CADD/细胞生物学领域的定位、适合发表的层次）\n\n"
            f"## 二、主要优点\n"
            f"（方法新颖性、实验设计合理性、数据可信度、结构/计算结果的可重复性）\n\n"
            f"## 三、主要不足\n"
            f"（方法局限性、实验缺陷、未解决的核心结构/计算/生物学问题）\n\n"
            f"## 四、严谨性评估\n"
            f"- 结构/计算数据质量：分辨率/精度是否达到领域标准？\n"
            f"- 生物活性佐证：计算预测是否有实验数据（IC50/Kd/活细胞实验）验证？\n"
            f"- 可证伪性：方法是否可独立验证或推翻？\n"
            f"- 对照充分性：是否与足够多的已知结构/对照化合物/SOTA方法进行了比较？\n"
            f"- 统计报告：是否提供了置信区间/p值/误差线/独立重复实验？\n\n"
            f"## 五、综合评分与建议\n"
            f"评分：[1–10，10分最高] / 建议：[接受 / 小修 / 大修 / 拒稿]\n"
            f"主要修改建议（3条以内）："
        )

    def _run_critique(self):
        self.critique_btn.configure(state=tk.DISABLED, text="分析中…")
        self.status_lbl.configure(text="正在调用 AI 进行深度点评…")
        self._set_result("")
        prompt = self._build_critique_prompt()

        def task():
            answer, err = call_llm_long(
                "你是一位严谨的结构生物学/CADD/细胞生物学领域资深论文评审专家，"
                "擅长方法学分析与实验设计评估。",
                prompt,
                max_tokens=3500,
                temperature=0.3,
                timeout=150,
            )
            if err:
                self.after(0, lambda: self._set_result(f"调用失败：{err}"))
                self.after(0, lambda: self.status_lbl.configure(text="失败"))
            else:
                self.after(0, lambda: self._set_result(answer or "（无回复）"))
                self.after(0, lambda: self.status_lbl.configure(text="点评完成"))
            self.after(0, lambda: self.critique_btn.configure(
                state=tk.NORMAL, text="▶ 开始深度点评"))

        threading.Thread(target=task, daemon=True).start()

    def _set_result(self, text: str):
        self.result_text.configure(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", text)
        self.result_text.configure(state=tk.DISABLED)

    def _copy_result(self):
        self.result_text.configure(state=tk.NORMAL)
        text = self.result_text.get("1.0", tk.END).strip()
        self.result_text.configure(state=tk.DISABLED)
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            messagebox.showinfo("已复制", "点评内容已复制到剪贴板。", parent=self)

class SynthesisDialog(tk.Toplevel):

    def __init__(self, parent, paper_ids: list):
        super().__init__(parent)
        self.paper_ids = paper_ids
        self._papers_data: list = []
        self.title(f"综述草稿生成 — 基于 {len(paper_ids)} 篇论文")
        self.geometry("920x700")
        self.resizable(True, True)
        self._build_ui()
        self._load_papers()

    def _load_papers(self):
        conn = get_db_conn()
        c = conn.cursor()
        for pid in self.paper_ids:
            c.execute(
                "SELECT title, authors, abstract, methods, innovations, year, category "
                "FROM papers WHERE id=?", (pid,)
            )
            row = c.fetchone()
            if not row:
                continue
            title, authors, abstract, methods, innovations, year, category = row
            self._papers_data.append({
                "id": pid,
                "title": title or "无标题",
                "authors": authors or "",
                "abstract": (abstract or "")[:500],
                "methods": (methods or "")[:300],
                "innovations": (innovations or "")[:200],
                "year": year or "",
                "category": category or "",
            })
        conn.close()
        for p in self._papers_data:
            self.paper_listbox.insert(tk.END, f"• {p['title']}")

    def _build_ui(self):
        ttk.Label(self, text="综述草稿生成  ·  多文献综合分析",
                  font=("Microsoft YaHei UI", 13, "bold")).pack(anchor="w", padx=12, pady=(10, 2))

        top = ttk.Frame(self)
        top.pack(fill=tk.X, padx=12, pady=8)
        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=2)
        top.rowconfigure(0, weight=1)

        list_frame = ttk.LabelFrame(top, text=f"选中论文（{len(self.paper_ids)} 篇）")
        list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self.paper_listbox = tk.Listbox(list_frame, font=("Microsoft YaHei UI", 9), height=6)
        sb_v = ttk.Scrollbar(list_frame, orient="vertical", command=self.paper_listbox.yview)
        sb_h = ttk.Scrollbar(list_frame, orient="horizontal", command=self.paper_listbox.xview)
        self.paper_listbox.configure(yscrollcommand=sb_v.set, xscrollcommand=sb_h.set)
        sb_v.pack(side=tk.RIGHT, fill=tk.Y)
        sb_h.pack(side=tk.BOTTOM, fill=tk.X)
        self.paper_listbox.pack(fill=tk.BOTH, expand=True, padx=2)

        right = ttk.Frame(top)
        right.grid(row=0, column=1, sticky="nsew")
        ttk.Label(right, text="综述聚焦方向（可选）：").pack(anchor="w")
        self.focus_entry = tk.Text(right, height=4, font=("Microsoft YaHei UI", 10))
        self.focus_entry.pack(fill=tk.BOTH, expand=True, pady=(4, 6))

        btn_row = ttk.Frame(right)
        btn_row.pack(fill=tk.X)
        self.run_btn = ttk.Button(btn_row, text="▶ 快速综述", command=self._run_synthesis)
        self.run_btn.pack(side=tk.LEFT)
        self.storm_btn = ttk.Button(btn_row, text="✦ STORM 精品综述", command=self._run_storm)
        self.storm_btn.pack(side=tk.LEFT, padx=(8, 0))
        self.status_lbl = ttk.Label(btn_row, text="", foreground="gray")
        self.status_lbl.pack(side=tk.LEFT, padx=8)

        result_frame = ttk.Frame(self)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 4))
        self.result_text = tk.Text(
            result_frame, font=("Microsoft YaHei UI", 10),
            wrap=tk.WORD, state=tk.DISABLED, padx=8, pady=6)
        sb2 = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=sb2.set)
        sb2.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.pack(fill=tk.BOTH, expand=True)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=12, pady=4)
        ttk.Button(btn_frame, text="复制全文", command=self._copy_result).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="导出 Markdown", command=self._export_md).pack(side=tk.LEFT, padx=8)
        ttk.Button(btn_frame, text="关闭", command=self.destroy).pack(side=tk.RIGHT)

    def _build_synthesis_prompt(self, focus: str) -> str:
        n = len(self._papers_data)
        focus_line = f"\n综述聚焦方向：{focus}" if focus.strip() else ""
        summaries = []
        for i, p in enumerate(self._papers_data, 1):
            summaries.append(
                f"[{i}] 《{p['title']}》（{p['year']}）\n"
                f"    作者：{p['authors'][:60]}\n"
                f"    分类：{p['category']}\n"
                f"    摘要：{p['abstract'][:400]}\n"
                f"    核心方法：{p['methods'][:200]}\n"
                f"    创新点：{p['innovations'][:150]}"
            )
        papers_block = "\n\n".join(summaries)
        return (
            f"请基于以下 {n} 篇结构生物学/CADD/细胞生物学文献，"
            f"生成一份结构化综述草稿，用简体中文输出。{focus_line}\n\n"
            f"【文献列表】\n{papers_block}\n\n---\n\n"
            f"请按以下结构输出综述草稿：\n\n"
            f"## 1. 研究背景与问题定义\n"
            f"（综合 {n} 篇文献所针对的核心科学问题，指出现有方法/结构/通路认知的主要局限）\n\n"
            f"## 2. 方法学分类与比较\n"
            f"（按方法范式分类：结构解析方法/计算模拟方法/实验验证方法等，引用[编号]）\n\n"
            f"## 3. 关键技术与发现\n"
            f"（列举 3–5 个最重要的技术突破点或关键发现，指出来源论文及核心贡献）\n\n"
            f"## 4. 数据集、模型系统与评估指标\n"
            f"（总结各文献使用的蛋白质体系/化合物库/细胞系/评估标准，指出不统一问题）\n\n"
            f"## 5. 研究空白与未来方向\n"
            f"（指出尚未解决的关键问题和有潜力的方向，至少 3 条）\n\n"
            f"## 参考文献\n（按 [编号] 格式列出所有引用文献的标题）"
        )

    def _run_synthesis(self):
        if not self._papers_data:
            messagebox.showwarning("提示", "论文数据尚未加载", parent=self)
            return
        focus = self.focus_entry.get("1.0", tk.END).strip()
        self.run_btn.configure(state=tk.DISABLED)
        self.storm_btn.configure(state=tk.DISABLED)
        self.status_lbl.configure(text="正在生成综述草稿…")
        self._set_result("")
        prompt = self._build_synthesis_prompt(focus)

        def task():
            answer, err = call_llm_long(
                "你是一位结构生物学/CADD/细胞生物学领域的资深综述撰写专家。",
                prompt, max_tokens=5000, temperature=0.4, timeout=180)
            if err:
                self.after(0, lambda: self._set_result(f"调用失败：{err}"))
                self.after(0, lambda: self.status_lbl.configure(text="失败"))
            else:
                self.after(0, lambda: self._set_result(answer or "（无回复）"))
                self.after(0, lambda: self.status_lbl.configure(text="综述生成完成"))
            self.after(0, lambda: self.run_btn.configure(state=tk.NORMAL))
            self.after(0, lambda: self.storm_btn.configure(state=tk.NORMAL))

        threading.Thread(target=task, daemon=True).start()

    def _run_storm(self):
        if not self._papers_data:
            messagebox.showwarning("提示", "论文数据尚未加载", parent=self)
            return
        focus = self.focus_entry.get("1.0", tk.END).strip()
        self.run_btn.configure(state=tk.DISABLED)
        self.storm_btn.configure(state=tk.DISABLED, text="生成中…")
        self.status_lbl.configure(text="STORM 第1步：生成大纲…")
        self._set_result("")

        papers_summary = "\n".join(
            f"[{i}] {p['title']} ({p['year']}) — {p['category']}"
            for i, p in enumerate(self._papers_data, 1)
        )
        topic = focus or "结构生物学/CADD/细胞生物学综合综述"

        def task():

            outline_prompt = (
                f"请为一篇关于「{topic}」的综述生成详细大纲（6-8节），"
                f"每节下列出2-3个需要重点回答的子问题。\n\n"
                f"涵盖的论文：\n{papers_summary}"
            )
            outline, err1 = call_llm(
                "你是结构生物学/CADD/细胞生物学综述专家。",
                outline_prompt, max_tokens=1200, temperature=0.4, timeout=60)
            if err1:
                self.after(0, lambda: self._set_result(f"大纲生成失败：{err1}"))
                self.after(0, lambda: self.status_lbl.configure(text="失败"))
                self.after(0, lambda: self.run_btn.configure(state=tk.NORMAL))
                self.after(0, lambda: self.storm_btn.configure(state=tk.NORMAL,
                                                                text="✦ STORM 精品综述"))
                return

            self.after(0, lambda: self.status_lbl.configure(text="STORM 第2步：展开正文…"))

            expand_prompt = self._build_synthesis_prompt(focus) + (
                f"\n\n参考以下大纲结构进行展开：\n{outline}")
            answer, err2 = call_llm_long(
                "你是结构生物学/CADD/细胞生物学领域资深综述撰写专家。",
                expand_prompt, max_tokens=6000, temperature=0.35, timeout=240)
            if err2:
                result = f"【大纲】\n{outline}\n\n【展开失败】\n{err2}"
            else:
                result = f"【大纲】\n{outline}\n\n{'='*60}\n\n【综述全文】\n\n{answer}"
            self.after(0, lambda: self._set_result(result))
            self.after(0, lambda: self.status_lbl.configure(text="STORM 综述完成"))
            self.after(0, lambda: self.run_btn.configure(state=tk.NORMAL))
            self.after(0, lambda: self.storm_btn.configure(state=tk.NORMAL,
                                                            text="✦ STORM 精品综述"))

        threading.Thread(target=task, daemon=True).start()

    def _set_result(self, text: str):
        self.result_text.configure(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", text)
        self.result_text.configure(state=tk.DISABLED)

    def _copy_result(self):
        self.result_text.configure(state=tk.NORMAL)
        text = self.result_text.get("1.0", tk.END).strip()
        self.result_text.configure(state=tk.DISABLED)
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            messagebox.showinfo("已复制", "综述内容已复制到剪贴板。", parent=self)

    def _export_md(self):
        text = ""
        self.result_text.configure(state=tk.NORMAL)
        text = self.result_text.get("1.0", tk.END).strip()
        self.result_text.configure(state=tk.DISABLED)
        if not text:
            messagebox.showwarning("提示", "尚无内容可导出。", parent=self)
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown 文件", "*.md"), ("文本文件", "*.txt")],
            title="导出综述草稿"
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            messagebox.showinfo("完成", f"已导出：\n{path}", parent=self)

class StructBioSkillsDialog(tk.Toplevel):

    _TAB_SKILLS = [
        ("🔬 结构解析",  "structure"),
        ("🎯 靶点-配体", "target_ligand"),
        ("💻 CADD计算",  "cadd"),
        ("🧬 细胞信号",  "cell_signal"),
    ]

    def __init__(self, parent, paper_ids: list):
        super().__init__(parent)
        self.paper_ids = paper_ids
        self._papers_data: list = []
        self.title(f"专项分析 — 基于 {len(paper_ids)} 篇论文")
        self.geometry("980x700")
        self.resizable(True, True)
        self._load_papers()
        self._build_ui()

    def _load_papers(self):
        conn = get_db_conn()
        c = conn.cursor()
        for pid in self.paper_ids:
            c.execute(
                "SELECT title, authors, abstract, methods, innovations, year, category "
                "FROM papers WHERE id=?", (pid,)
            )
            row = c.fetchone()
            if not row:
                continue
            title, authors, abstract, methods, innovations, year, category = row
            self._papers_data.append({
                "title":      title or "无标题",
                "authors":    authors or "",
                "abstract":   (abstract or "")[:1200],
                "methods":    (methods or "")[:600],
                "innovations":(innovations or "")[:400],
                "year":       year or "",
                "category":   category or "",
            })
        conn.close()

    def _build_papers_block(self) -> str:
        parts = []
        for i, p in enumerate(self._papers_data, 1):
            parts.append(
                f"【论文 {i}】标题：{p['title']}（{p['year']}）\n"
                f"分类：{p['category']}\n"
                f"摘要：{p['abstract'][:600]}\n"
                f"方法：{p['methods'][:300]}\n"
                f"创新点：{p['innovations'][:200]}"
            )
        return "\n\n".join(parts)

    def _build_ui(self):
        hdr = ttk.Frame(self)
        hdr.pack(fill=tk.X, padx=12, pady=(10, 4))
        ttk.Label(hdr, text="结构生物学/CADD/细胞生物学  专项技能分析",
                  font=("Microsoft YaHei UI", 13, "bold")).pack(side=tk.LEFT)
        ttk.Button(hdr, text="▶▶ 全部分析",
                   command=self._run_all).pack(side=tk.RIGHT)
        ttk.Label(hdr, text=f"共 {len(self._papers_data)} 篇论文",
                  foreground="gray").pack(side=tk.RIGHT, padx=8)

        nb = ttk.Notebook(self)
        nb.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        self._result_widgets = {}
        for tab_label, skill_key in self._TAB_SKILLS:
            frame = ttk.Frame(nb)
            nb.add(frame, text=tab_label)
            self._build_skill_tab(frame, skill_key)

    def _build_skill_tab(self, parent: ttk.Frame, skill_key: str):
        ctrl = ttk.Frame(parent)
        ctrl.pack(fill=tk.X, padx=10, pady=6)

        titles = {
            "structure":    "提取结构解析数据（方法/分辨率/PDB ID/关键发现）",
            "target_ligand":"分析靶点-配体相互作用与结合活性",
            "cadd":         "提取 CADD 计算数据（对接分数/ΔG/MD参数）",
            "cell_signal":  "提取细胞信号通路与功能实验信息",
        }
        run_btn = ttk.Button(ctrl, text=f"▶ {titles[skill_key]}",
                             command=lambda k=skill_key: self._run_skill(k))
        run_btn.pack(side=tk.LEFT)
        export_btn = ttk.Button(ctrl, text="导出 TXT",
                                command=lambda k=skill_key: self._export_skill(k))
        export_btn.pack(side=tk.RIGHT, padx=4)
        prog = ttk.Progressbar(ctrl, orient="horizontal", length=160, mode="determinate")
        prog.pack(side=tk.RIGHT, padx=8)
        status = ttk.Label(ctrl, text="", foreground="gray")
        status.pack(side=tk.LEFT, padx=10)

        txt_frame = ttk.Frame(parent)
        txt_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 8))
        txt = tk.Text(txt_frame, font=("Microsoft YaHei UI", 10),
                      wrap=tk.WORD, state=tk.DISABLED, padx=8, pady=6)
        sb = ttk.Scrollbar(txt_frame, orient="vertical", command=txt.yview)
        txt.configure(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        txt.pack(fill=tk.BOTH, expand=True)

        self._result_widgets[skill_key] = {
            "btn": run_btn, "status": status,
            "progress": prog, "export_btn": export_btn, "text": txt
        }

    def _run_skill(self, skill_key: str, _silent: bool = False):
        if not self._papers_data:
            if not _silent:
                messagebox.showwarning("提示", "无论文数据", parent=self)
            return
        w = self._result_widgets[skill_key]
        w["btn"].configure(state=tk.DISABLED, text="分析中…")
        w["progress"].configure(value=0)
        w["status"].configure(text="正在调用 AI 分析，请稍候…")

        papers_block = self._build_papers_block()

        prompts = {
            "structure": (
                "你是结构生物学专家，擅长解读X射线晶体学、cryo-EM、NMR等结构数据。",
                f"请从以下论文中提取所有结构解析信息，用简体中文输出：\n\n{papers_block}\n\n"
                "请按论文编号逐篇列出：\n"
                "1. 解析方法（X射线/cryo-EM/NMR/其他）\n"
                "2. 分辨率（Å）\n"
                "3. PDB ID（若已提交）\n"
                "4. 目标蛋白/复合物\n"
                "5. 关键结构发现与功能意义\n"
                "6. 结构质量参数（R因子/FSC等）\n"
                "未涉及结构解析的论文请注明「非结构类」。"
            ),
            "target_ligand": (
                "你是CADD和化学生物学专家，擅长分析靶点-配体相互作用数据。",
                f"请从以下论文中提取所有靶点-配体相互作用信息，用简体中文输出：\n\n{papers_block}\n\n"
                "请按论文编号逐篇列出：\n"
                "1. 靶点蛋白（全名/UniProt ID）\n"
                "2. 配体/化合物（名称/类型）\n"
                "3. 结合活性（IC50/Ki/Kd/EC50数值，含单位）\n"
                "4. 关键相互作用（氢键/疏水接触/静电作用等）\n"
                "5. 选择性数据（如有）\n"
                "6. 共晶结构信息（如有）"
            ),
            "cadd": (
                "你是计算化学和CADD专家，擅长分析分子对接、自由能计算和分子动力学数据。",
                f"请从以下论文中提取所有CADD计算数据，用简体中文输出：\n\n{papers_block}\n\n"
                "请按论文编号逐篇列出：\n"
                "1. 使用的CADD方法（对接软件/MD软件/QSAR方法等）\n"
                "2. 关键计算参数（力场/模拟时间/对接精度设置等）\n"
                "3. 结合自由能数值（ΔG/ΔΔG，含计算方法）\n"
                "4. 虚拟筛选结果（命中率/筛选库大小）\n"
                "5. 预测模型性能指标（AUC/RMSE/R²等）\n"
                "6. 实验验证情况"
            ),
            "cell_signal": (
                "你是细胞生物学专家，擅长信号通路和细胞功能实验分析。",
                f"请从以下论文中提取所有细胞生物学信息，用简体中文输出：\n\n{papers_block}\n\n"
                "请按论文编号逐篇列出：\n"
                "1. 涉及的信号通路（名称及关键节点）\n"
                "2. 细胞模型（细胞系/原代细胞/类器官等）\n"
                "3. 功能实验（增殖/凋亡/迁移/分化等，含检测方法）\n"
                "4. 关键蛋白/基因（表达变化/突变/修饰状态）\n"
                "5. 动物模型或临床数据（如有）\n"
                "6. 关键阳性/阴性对照设置"
            ),
        }
        system_p, user_p = prompts[skill_key]

        def task():
            self.after(0, lambda: w["progress"].configure(value=30))
            answer, err = call_llm_long(system_p, user_p,
                                         max_tokens=4000, temperature=0.3, timeout=180)
            self.after(0, lambda: w["progress"].configure(value=90))
            result = answer if not err else f"分析失败：{err}"
            status_msg = "分析完成" if not err else "失败"
            btn_label = {
                "structure":    "提取结构解析数据（方法/分辨率/PDB ID/关键发现）",
                "target_ligand":"分析靶点-配体相互作用与结合活性",
                "cadd":         "提取 CADD 计算数据（对接分数/ΔG/MD参数）",
                "cell_signal":  "提取细胞信号通路与功能实验信息",
            }.get(skill_key, "")
            self.after(0, lambda: self._set_text(skill_key, result))
            self.after(0, lambda: w["status"].configure(text=status_msg))
            self.after(0, lambda: w["btn"].configure(
                state=tk.NORMAL, text=f"▶ {btn_label}"))
            self.after(0, lambda: w["progress"].configure(value=100))

        threading.Thread(target=task, daemon=True).start()

    def _run_all(self):
        for _, skill_key in self._TAB_SKILLS:
            self._run_skill(skill_key, _silent=True)

    def _set_text(self, skill_key: str, text: str):
        txt = self._result_widgets[skill_key].get("text")
        if txt:
            txt.configure(state=tk.NORMAL)
            txt.delete("1.0", tk.END)
            txt.insert("1.0", text)
            txt.configure(state=tk.DISABLED)

    def _export_skill(self, skill_key: str):
        txt = self._result_widgets[skill_key].get("text")
        if not txt:
            return
        txt.configure(state=tk.NORMAL)
        text = txt.get("1.0", tk.END).strip()
        txt.configure(state=tk.DISABLED)
        if not text:
            messagebox.showwarning("提示", "尚无内容可导出。", parent=self)
            return
        names = {"structure": "结构解析", "target_ligand": "靶点配体",
                 "cadd": "CADD计算", "cell_signal": "细胞信号"}
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt")],
            initialfile=f"{names.get(skill_key, skill_key)}_分析.txt",
            title="导出分析结果"
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            messagebox.showinfo("完成", f"已导出：\n{path}", parent=self)

class ModelManagerDialog(tk.Toplevel):

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.title("解析引擎管理")
        self.geometry("540x440")
        self.resizable(True, True)
        self._build()
        self.grab_set()

    def _build(self):
        ttk.Label(self, text="解析引擎管理",
                  font=("Microsoft YaHei UI", 13, "bold")).pack(padx=12, pady=(10, 4), anchor="w")

        list_frame = ttk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=4)
        vsb = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self._canvas = tk.Canvas(list_frame, highlightthickness=0,
                                 yscrollcommand=vsb.set)
        vsb.config(command=self._canvas.yview)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._list_inner = ttk.Frame(self._canvas)
        cwin = self._canvas.create_window((0, 0), window=self._list_inner, anchor="nw")
        self._list_inner.bind("<Configure>",
                              lambda e: self._canvas.configure(
                                  scrollregion=self._canvas.bbox("all")))
        self._canvas.bind("<Configure>",
                          lambda e: self._canvas.itemconfig(cwin, width=e.width))
        self._refresh_list()

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=12, pady=(4, 10))
        ttk.Button(btn_frame, text="＋ 添加自定义模型",
                   command=self._add_model).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="关闭",
                   command=self.destroy).pack(side=tk.RIGHT)

    def _refresh_list(self):
        for w in self._list_inner.winfo_children():
            w.destroy()
        for name in list(MODEL_CONFIGS.keys()):
            is_default = name in DEFAULT_MODEL_CONFIGS
            row = ttk.Frame(self._list_inner)
            row.pack(fill=tk.X, pady=2)
            badge = ttk.Label(row,
                              text="预置" if is_default else "自定义",
                              foreground="gray" if is_default else "blue")
            badge.pack(side=tk.LEFT, padx=(6, 4))
            cfg = MODEL_CONFIGS[name]
            thinking_tag = "  🧠thinking" if cfg.get("thinking") else ""
            base = (cfg.get("base_url") or "")[:40]
            info_text = (f"{name}\n"
                         f"model={cfg.get('model', name)}{thinking_tag}  {base}")
            ttk.Label(row, text=info_text, justify="left").pack(
                side=tk.LEFT, fill=tk.BOTH, expand=True)

            btns = ttk.Frame(row)
            btns.pack(side=tk.RIGHT, padx=6)

            def make_set_key(n=name):
                def _set():
                    key = simpledialog.askstring(
                        "设置 API Key", f"输入 {n} 的 API Key：",
                        parent=self, show="*")
                    if key:

                        MODEL_CONFIGS[n]["api_key"] = key.strip()
                        if n == CURRENT_MODEL_NAME:
                            global LLM_API_KEY
                            LLM_API_KEY = key.strip()

                        save_model_configs()
                        messagebox.showinfo("已设置", f"{n} 的 API Key 已更新。", parent=self)
                return _set

            def make_use(n=name):
                def _use():
                    apply_model_config(n)
                    if hasattr(self.app, 'model_label'):
                        self.app.model_label.config(text=f"引擎: {CURRENT_MODEL_NAME}")
                    if hasattr(self.app, 'refresh_model_menu'):
                        self.app.refresh_model_menu()
                    messagebox.showinfo("已切换", f"当前模型已切换为：{n}", parent=self)
                return _use

            ttk.Button(btns, text="设置Key", command=make_set_key(name)).pack(
                side=tk.LEFT, padx=2)
            ttk.Button(btns, text="使用", command=make_use(name)).pack(
                side=tk.LEFT, padx=2)
            if not is_default:
                def make_del(n=name):
                    def _del():
                        if messagebox.askyesno("确认删除", f"删除自定义模型 {n}？",
                                               parent=self):
                            del MODEL_CONFIGS[n]
                            save_model_configs()
                            refresh_available_models()
                            self._refresh_list()
                    return _del
                ttk.Button(btns, text="删除", command=make_del(name)).pack(
                    side=tk.LEFT, padx=2)

    def _add_model(self):
        name = simpledialog.askstring("模型名称", "输入一个唯一的模型名称（如 qwen-72b）：",
                                      parent=self)
        if not name:
            return
        name = name.strip()
        if name in MODEL_CONFIGS:
            messagebox.showwarning("已存在", f"模型名称 {name} 已存在。", parent=self)
            return
        base_url = simpledialog.askstring(
            "Base URL",
            "输入 API Base URL（如 https://api.openai.com/v1）：",
            parent=self)
        if not base_url:
            return
        base_url = base_url.strip().rstrip("/")

        if not (base_url.startswith("https://") or base_url.startswith("http://")):
            messagebox.showerror(
                "URL 格式错误",
                "Base URL 必须以 https:// 或 http:// 开头。\n"
                "请确认您输入的是合法的 API 服务地址。",
                parent=self)
            return
        if not base_url.startswith("https://"):
            if not messagebox.askyesno(
                "安全警告",
                "您输入的 URL 使用了非加密的 http:// 协议。\n"
                "这可能导致 API Key 在传输中被截获，请确认：\n"
                f"{base_url}\n\n是否继续？",
                parent=self):
                return
        api_key = simpledialog.askstring("API Key", "输入 API Key（可留空后再设置）：",
                                         parent=self, show="*")
        model_id = simpledialog.askstring(
            "Model ID",
            f"输入模型 ID（留空则使用 {name}）：",
            parent=self)
        MODEL_CONFIGS[name] = {
            "model": (model_id or name).strip(),
            "base_url": base_url.strip().rstrip("/"),
            "api_key_env": "",
            "api_key": (api_key or "").strip()
        }
        save_model_configs()
        refresh_available_models()
        self._refresh_list()
        messagebox.showinfo("已添加", f"模型 {name} 已添加。", parent=self)

class LiteratureManager:
    def __init__(self, root):
        self.root = root
        self.root.title("文献管理器 - 结构生物学/CADD/细胞生物学专用版")
        self.root.geometry("1400x800")

        menubar = tk.Menu(root)
        cat_menu = tk.Menu(menubar, tearoff=0)
        cat_menu.add_command(label="管理分类...", command=self.manage_categories)
        menubar.add_cascade(label="分类", menu=cat_menu)

        scan_menu = tk.Menu(menubar, tearoff=0)
        scan_menu.add_command(label="导入扫描报告...", command=self.open_scan_browser)
        menubar.add_cascade(label="扫描报告", menu=scan_menu)

        self.model_menu = tk.Menu(menubar, tearoff=0)
        self.model_var = tk.StringVar(value=CURRENT_MODEL_NAME)
        self.refresh_model_menu()
        menubar.add_cascade(label="解析引擎", menu=self.model_menu)

        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="修复文件路径 + 补全 DOI/年份...", command=self.repair_and_fill_metadata)
        tools_menu.add_separator()
        tools_menu.add_command(label="管理解析引擎...",
                               command=lambda: ModelManagerDialog(self.root, self))
        menubar.add_cascade(label="工具", menu=tools_menu)

        root.config(menu=menubar)

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

        self.model_label = ttk.Label(search_frame, text=f"引擎: {CURRENT_MODEL_NAME}", foreground="gray")
        self.model_label.pack(side=tk.LEFT, padx=(20,0))

        ttk.Button(search_frame, text="导入PDF", command=self.import_pdf).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="打开PDF", command=self.open_pdf).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="删除", command=self.delete_paper).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="批量删除", command=self.delete_selected_papers).pack(side=tk.LEFT, padx=5)
        self.suggest_btn = ttk.Button(
            search_frame, text="课题建议",
            command=self.on_suggest_topics, state=tk.DISABLED
        )
        self.suggest_btn.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="问文献",
                   command=self.open_ask_library).pack(side=tk.LEFT, padx=5)

        filter_frame = ttk.Frame(root)
        filter_frame.pack(fill=tk.X, padx=5, pady=(0, 4))

        ttk.Label(filter_frame, text="标签:").pack(side=tk.LEFT)
        self.tag_filter = ttk.Combobox(filter_frame, width=16)
        self.tag_filter.set("全部")
        self.tag_filter.bind('<<ComboboxSelected>>', lambda e: self.refresh_list())
        self.tag_filter.bind('<Return>', lambda e: self.refresh_list())
        self.tag_filter.pack(side=tk.LEFT, padx=4)

        ttk.Label(filter_frame, text="年份:").pack(side=tk.LEFT, padx=(12, 0))
        self.year_from_var = tk.StringVar()
        self.year_to_var = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.year_from_var, width=6).pack(side=tk.LEFT, padx=2)
        ttk.Label(filter_frame, text="–").pack(side=tk.LEFT)
        ttk.Entry(filter_frame, textvariable=self.year_to_var, width=6).pack(side=tk.LEFT, padx=2)
        self.year_from_var.trace('w', lambda *_: self.refresh_list())
        self.year_to_var.trace('w', lambda *_: self.refresh_list())

        ttk.Button(filter_frame, text="批量重新分析", command=self.batch_reanalyze_papers).pack(side=tk.LEFT, padx=(16, 2))
        self.synthesis_btn = ttk.Button(filter_frame, text="生成综述",
                                        command=self.open_synthesis, state=tk.DISABLED)
        self.synthesis_btn.pack(side=tk.LEFT, padx=2)
        self.skills_btn = ttk.Button(filter_frame, text="🔬 AI分析",
                                     command=self.open_skills_dialog, state=tk.DISABLED)
        self.skills_btn.pack(side=tk.LEFT, padx=2)
        ttk.Button(filter_frame, text="统计", command=self.show_statistics).pack(side=tk.LEFT, padx=2)
        ttk.Button(filter_frame, text="导出 CSV", command=self.export_csv).pack(side=tk.LEFT, padx=2)
        ttk.Button(filter_frame, text="导出 BibTeX", command=self.export_bibtex).pack(side=tk.LEFT, padx=2)

        paned = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)

        columns = ('title', 'category', 'year', 'authors', 'pages')
        self.tree = ttk.Treeview(left_frame, columns=columns, show='headings')
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
        self.tree.column('title', width=260)
        self.tree.column('category', width=100)
        self.tree.column('year', width=55, anchor=tk.CENTER)
        self.tree.column('authors', width=120)
        self.tree.column('pages', width=50)

        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        self.tree.bind('<Double-1>', lambda e: self.open_pdf())

        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=2)

        info_frame = ttk.LabelFrame(right_frame, text="文献信息", padding=5)
        info_frame.pack(fill=tk.X, pady=5)

        self.info_title = ttk.Label(info_frame, text="标题: ", wraplength=600, justify=tk.LEFT)
        self.info_title.pack(anchor=tk.W)
        self.info_author = ttk.Label(info_frame, text="作者: ")
        self.info_author.pack(anchor=tk.W)
        self.info_year = ttk.Label(info_frame, text="年份: ")
        self.info_year.pack(anchor=tk.W)
        self.info_doi = ttk.Label(info_frame, text="DOI: ", foreground="#1565c0", cursor="hand2")
        self.info_doi.pack(anchor=tk.W)
        self.info_doi.bind('<Button-1>', self._copy_doi)
        self.info_category = ttk.Label(info_frame, text="分类: ")
        self.info_category.pack(anchor=tk.W)
        self.info_keywords = ttk.Label(info_frame, text="关键词: ", wraplength=600, justify=tk.LEFT)
        self.info_keywords.pack(anchor=tk.W)

        edit_frame = ttk.Frame(right_frame)
        edit_frame.pack(fill=tk.X, pady=5)

        ttk.Label(edit_frame, text="标签:").pack(side=tk.LEFT)
        self.tag_var = tk.StringVar()
        ttk.Entry(edit_frame, textvariable=self.tag_var, width=25).pack(side=tk.LEFT, padx=5)

        ttk.Label(edit_frame, text="分类:").pack(side=tk.LEFT, padx=(15,0))
        self.cat_var = ttk.Combobox(edit_frame, values=get_categories(), width=20, state="readonly")
        self.cat_var.pack(side=tk.LEFT, padx=5)
        ttk.Button(edit_frame, text="保存", command=self.save_metadata).pack(side=tk.LEFT)

        status_row = ttk.Frame(right_frame)
        status_row.pack(fill=tk.X, pady=(2, 2))
        ttk.Label(status_row, text="阅读状态:").pack(side=tk.LEFT)
        self.read_status_var = tk.StringVar(value="unread")
        self.read_status_cb = ttk.Combobox(
            status_row, textvariable=self.read_status_var,
            values=["unread", "reading", "read"], width=10, state="readonly")
        self.read_status_cb.pack(side=tk.LEFT, padx=5)
        self.read_status_cb.bind('<<ComboboxSelected>>', self._save_read_status)
        self.critique_btn_tb = ttk.Button(
            status_row, text="深度点评", command=self.open_critique, state=tk.DISABLED)
        self.critique_btn_tb.pack(side=tk.LEFT, padx=(12, 0))

        notes_frame = ttk.LabelFrame(right_frame, text="个人笔记", padding=4)
        notes_frame.pack(fill=tk.X, pady=(2, 4))
        self.notes_text = tk.Text(notes_frame, height=3, wrap=tk.WORD)
        self.notes_text.pack(fill=tk.X)
        ttk.Button(notes_frame, text="保存笔记",
                   command=self._save_personal_notes).pack(anchor=tk.W, pady=(2, 0))

        analysis_frame = ttk.LabelFrame(right_frame, text="AI分析", padding=5)
        analysis_frame.pack(fill=tk.X, pady=5)

        ttk.Label(analysis_frame, text="主要方法:").pack(anchor=tk.W)
        self.methods_text = tk.Text(analysis_frame, height=3, wrap=tk.WORD)
        self.methods_text.pack(fill=tk.X)

        ttk.Label(analysis_frame, text="创新点:").pack(anchor=tk.W)
        self.innovations_text = tk.Text(analysis_frame, height=3, wrap=tk.WORD)
        self.innovations_text.pack(fill=tk.X)
        ttk.Button(analysis_frame, text="重新分析（LLM）", command=self.reanalyze_paper).pack(anchor=tk.W, pady=(4, 0))

        abs_frame = ttk.LabelFrame(right_frame, text="摘要", padding=5)
        abs_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.abstract_text = scrolledtext.ScrolledText(abs_frame, wrap=tk.WORD)
        self.abstract_text.pack(fill=tk.BOTH, expand=True)

        self.current_paper_id = None
        self.refresh_filter_options()
        self.refresh_list()

    def refresh_filter_options(self):
        categories = get_categories()
        tags = get_all_tags()

        cur_cat_filter = self.cat_filter.get() if hasattr(self, 'cat_filter') else "全部"
        cur_cat = self.cat_var.get() if hasattr(self, 'cat_var') else ""
        cur_tag = self.tag_filter.get() if hasattr(self, 'tag_filter') else "全部"

        self.cat_filter['values'] = ["全部"] + categories
        self.cat_var['values'] = categories
        self.tag_filter['values'] = ["全部"] + tags

        self.cat_filter.set(cur_cat_filter if cur_cat_filter in self.cat_filter['values'] else "全部")
        if cur_cat in categories:
            self.cat_var.set(cur_cat)
        self.tag_filter.set(cur_tag if cur_tag in self.tag_filter['values'] else "全部")

    def refresh_category_options(self):
        self.refresh_filter_options()

    def refresh_after_data_change(self):
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

    def on_select(self, event):
        selection = self.tree.selection()
        n_sel = len(selection)

        self.suggest_btn.config(state=tk.NORMAL if n_sel >= 2 else tk.DISABLED)
        self.synthesis_btn.config(state=tk.NORMAL if n_sel >= 2 else tk.DISABLED)
        self.skills_btn.config(state=tk.NORMAL if n_sel >= 1 else tk.DISABLED)
        if not selection:
            return

        paper_id = selection[0]
        self.current_paper_id = paper_id

        self.critique_btn_tb.config(state=tk.NORMAL if n_sel >= 1 else tk.DISABLED)

        conn = get_db_conn()
        c = conn.cursor()
        c.execute(
            '''SELECT title, authors, category, keywords, abstract, tags,
                      methods, innovations, file_path, year, doi,
                      read_status, personal_notes
               FROM papers WHERE id=?''',
            (paper_id,))
        row = c.fetchone()
        conn.close()

        if row:
            self.info_title.config(text=f"标题: {row[0]}")
            self.info_author.config(text=f"作者: {row[1] or '未知'}")
            self.info_year.config(text=f"年份: {row[9] or '未知'}")
            doi_val = row[10] or ''
            self.info_doi.config(text=f"DOI: {doi_val or 'N/A'}")
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

            _rs = row[11] or "unread"
            self.read_status_var.set(_rs)

            self.notes_text.delete(1.0, tk.END)
            self.notes_text.insert(1.0, row[12] or '')

    def open_ask_library(self):
        AskLibraryDialog(self.root)

    def open_skills_dialog(self):
        paper_ids = list(self.tree.selection())
        if not paper_ids:
            messagebox.showwarning("提示", "请先选择至少1篇论文。", parent=self.root)
            return
        StructBioSkillsDialog(self.root, paper_ids)

    def open_synthesis(self):
        paper_ids = list(self.tree.selection())
        if len(paper_ids) < 2:
            messagebox.showwarning("提示", "请至少选择2篇论文（Ctrl+点击多选）。", parent=self.root)
            return
        SynthesisDialog(self.root, paper_ids)

    def open_critique(self):
        if not self.current_paper_id:
            messagebox.showwarning("提示", "请先选择一篇论文。", parent=self.root)
            return
        PaperCritiqueDialog(self.root, self.current_paper_id)

    def _save_read_status(self, event=None):
        if not self.current_paper_id:
            return
        val = self.read_status_var.get()
        try:
            conn = get_db_conn()
            conn.execute("UPDATE papers SET read_status=? WHERE id=?",
                         (val, self.current_paper_id))
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror("错误", f"保存阅读状态失败：{e}", parent=self.root)

    def _save_personal_notes(self):
        if not self.current_paper_id:
            messagebox.showwarning("提示", "请先选择一篇论文。", parent=self.root)
            return
        notes = self.notes_text.get(1.0, tk.END).strip()
        try:
            conn = get_db_conn()
            conn.execute("UPDATE papers SET personal_notes=? WHERE id=?",
                         (notes, self.current_paper_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("已保存", "个人笔记已保存。", parent=self.root)
        except Exception as e:
            messagebox.showerror("错误", f"保存笔记失败：{e}", parent=self.root)

    def on_suggest_topics(self):
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

                try:
                    pending_dir = os.path.join(os.path.dirname(row[0]), '_pending_delete')
                    os.makedirs(pending_dir, exist_ok=True)
                    import time
                    new_name = f"{int(time.time())}_{os.path.basename(row[0])}"
                    os.rename(row[0], os.path.join(pending_dir, new_name))
                    pdf_deleted = True
                except Exception:
                    pass

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

        self.refresh_after_data_change()
        messagebox.showinfo("完成", "已保存")

    def refresh_model_menu(self):
        self.model_menu.delete(0, tk.END)
        for name in AVAILABLE_MODELS:
            self.model_menu.add_radiobutton(
                label=name,
                variable=self.model_var,
                value=name,
                command=self.on_model_change
            )
        self.model_menu.add_separator()
        self.model_menu.add_command(
            label="新增/修改自定义模型/API...",
            command=self.configure_custom_model
        )

    def configure_custom_model(self):
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
        self.model_label.config(text=f"引擎: {CURRENT_MODEL_NAME}")
        messagebox.showinfo(
            "引擎切换",
            f"已切换至: {CURRENT_MODEL_NAME}\n模型ID: {LLM_MODEL}\nAPI: {LLM_BASE_URL}\n下次调用AI时生效"
        )

    def delete_selected_papers(self):
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
                self.refresh_category_options()

        def delete_selected():
            sel = listbox.curselection()
            if sel:
                name = listbox.get(sel[0])
                if messagebox.askyesno("确认", f"删除分类 '{name}'？\n该分类下的文献将变为'未分类'", parent=dialog):
                    delete_category(name)
                    listbox.delete(sel[0])
                    self.refresh_category_options()

        ttk.Button(btn_frame, text="添加", command=add_new).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="删除", command=delete_selected).pack(side=tk.LEFT, padx=5)

    def clear_detail(self):
        self.info_title.config(text="标题: ")
        self.info_author.config(text="作者: ")
        self.info_year.config(text="年份: ")
        self.info_doi.config(text="DOI: ")
        self.info_category.config(text="分类: ")
        self.info_keywords.config(text="关键词: ")
        self.cat_var.set('')
        self.tag_var.set('')
        self.methods_text.delete(1.0, tk.END)
        self.innovations_text.delete(1.0, tk.END)
        self.abstract_text.delete(1.0, tk.END)
        self.read_status_var.set("unread")
        self.notes_text.delete(1.0, tk.END)

    def repair_and_fill_metadata(self):

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
            c2.execute('SELECT id, file_path, doi, year, authors FROM papers')
            all_rows = c2.fetchall()

            fixed_paths = 0
            filled_meta = 0

            for pid, fp, cur_doi, cur_year, cur_authors in all_rows:

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

                need_doi     = not (cur_doi     and cur_doi.strip())
                need_year    = not (cur_year    and cur_year.strip())
                need_authors = not (cur_authors and cur_authors.strip())
                if not need_doi and not need_year and not need_authors:
                    continue

                try:
                    with fitz.open(actual_fp) as doc:
                        meta = doc.metadata
                        text = ''.join(
                            doc.load_page(i).get_text()
                            for i in range(min(5, len(doc)))
                        )
                except Exception:
                    continue

                fields, vals = [], []
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

                    authors = (meta.get('author') or '').strip()
                    if not authors:
                        authors = extract_authors_from_text(text)
                    if authors:
                        fields.append('authors=?'); vals.append(authors)

                if fields:
                    vals.append(pid)
                    c2.execute(f"UPDATE papers SET {', '.join(fields)} WHERE id=?", vals)
                    filled_meta += 1

            conn2.commit()

            self.root.after(0, lambda: slabel.config(text="CrossRef 在线查询中…"))
            import time as _time
            filled_crossref = 0

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

                _time.sleep(0.2)

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

    def _copy_doi(self, event=None):
        doi = self.info_doi.cget('text').replace('DOI: ', '').strip()
        if doi and doi != 'N/A':
            self.root.clipboard_clear()
            self.root.clipboard_append(doi)
            messagebox.showinfo("已复制", f"DOI 已复制：\n{doi}", parent=self.root)

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
        vals   = [analysis.get('category', '未分类'), analysis.get('methods', ''),
                  analysis.get('innovations', ''), year]
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
        if doi:        parts.append('DOI')
        if new_authors: parts.append('作者')
        messagebox.showinfo("完成", f"重新分析完成，已更新：{'/ '.join(parts)}。", parent=self.root)

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

                fields = ['category=?', 'methods=?', 'innovations=?', 'year=?']
                vals   = [analysis.get('category', '未分类'), analysis.get('methods', ''),
                          analysis.get('innovations', ''), year]
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

        lines = ["文献库统计", "=" * 38,
                 f"总计：{total} 篇", "",
                 f"按分类（共 {len(by_cat)} 类）："]
        for cat, cnt in by_cat:
            bar = '█' * cnt if cnt <= 30 else '█' * 30 + f"…+{cnt-30}"
            lines.append(f"  {(cat or '未分类'):<16} {cnt:>4} 篇  {bar}")
        lines += ["", "按年份："]
        for yr, cnt in by_year:
            lines.append(f"  {yr}  {cnt} 篇")

        dlg = tk.Toplevel(self.root)
        dlg.title("文献库统计")
        dlg.geometry("440x520")
        t = scrolledtext.ScrolledText(dlg, wrap=tk.WORD, font=("Courier New", 10))
        t.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        t.insert(tk.END, "\n".join(lines))
        t.config(state=tk.DISABLED)
        ttk.Button(dlg, text="关闭", command=dlg.destroy).pack(pady=4)

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

class ScanReportBrowser(tk.Toplevel):

    CHECK_ON  = '☑'
    CHECK_OFF = '☐'

    def __init__(self, parent, on_import_done=None):
        super().__init__(parent)
        self.title("扫描报告浏览器")
        self.geometry("1100x680")
        self.resizable(True, True)
        self.on_import_done = on_import_done

        self._papers = []
        self._item_checks = {}

        self._build_ui()
        self._load_default_report()

    def _build_ui(self):

        top = ttk.Frame(self)
        top.pack(fill=tk.X, padx=8, pady=6)

        ttk.Label(top, text="报告文件:").pack(side=tk.LEFT)
        self._file_var = tk.StringVar()
        ttk.Entry(top, textvariable=self._file_var, width=55).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="浏览...", command=self._browse_file).pack(side=tk.LEFT)
        ttk.Button(top, text="加载", command=self._load_report).pack(side=tk.LEFT, padx=4)

        bar = ttk.Frame(self)
        bar.pack(fill=tk.X, padx=8, pady=2)
        ttk.Button(bar, text="全选", command=self._select_all).pack(side=tk.LEFT)
        ttk.Button(bar, text="取消全选", command=self._deselect_all).pack(side=tk.LEFT, padx=4)
        self._count_label = ttk.Label(bar, text="")
        self._count_label.pack(side=tk.LEFT, padx=12)

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

        detail = ttk.LabelFrame(self, text="核心方法 / 详情", padding=6)
        detail.pack(fill=tk.X, padx=8, pady=4)
        self._detail_text = tk.Text(detail, height=4, wrap=tk.WORD, state=tk.DISABLED,
                                    background='#f5f5f5')
        self._detail_text.pack(fill=tk.X)

        btn_row = ttk.Frame(self)
        btn_row.pack(fill=tk.X, padx=8, pady=4)
        ttk.Button(btn_row, text="下载并导入选中",
                   command=self._download_and_import).pack(side=tk.LEFT)
        ttk.Button(btn_row, text="仅导入元数据（不下载PDF）",
                   command=self._import_metadata_only).pack(side=tk.LEFT, padx=6)
        ttk.Button(btn_row, text="复制选中链接",
                   command=self._copy_links).pack(side=tk.LEFT)

        prog_frame = ttk.Frame(self)
        prog_frame.pack(fill=tk.X, padx=8, pady=(0, 6))
        self._progress = ttk.Progressbar(prog_frame, mode='determinate', length=400)
        self._progress.pack(side=tk.LEFT)
        self._status_label = ttk.Label(prog_frame, text="")
        self._status_label.pack(side=tk.LEFT, padx=8)

    def _load_default_report(self):
        lit_dir = os.path.dirname(os.path.abspath(__file__))
        today = datetime.now().strftime('%Y-%m-%d')
        default = os.path.join(lit_dir, f'StructBioCADD_CellBio_scan_{today}.md')
        if not os.path.isfile(default):

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

    def _insert_paper_to_db(self, p, file_path: str) -> bool:
        conn = get_db_conn()
        c = conn.cursor()
        try:
            if p.doi:
                c.execute('SELECT id FROM papers WHERE doi=?', (p.doi,))
                if c.fetchone():
                    return False
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
    root = tk.Tk()
    set_app_icon(root)
    ask_api_key(root)
    app = LiteratureManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()