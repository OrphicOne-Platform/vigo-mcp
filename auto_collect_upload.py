#!/usr/bin/env python3
"""
============================================================
  VIGO SFC 雙語監管信息自動收集 & 上傳 v3.0
  PDF 智能提取 + 中英雙語 + 官方鏈接
  OpenAI 直連 + DeepSeek 直連（匹配 v3.3）
============================================================

核心能力：
  - PDF 文件：自動下載 → pdfplumber 提取文字 → 按章節拆分
  - HTML 文件：自動清理 HTML 標籤 → 提取正文
  - 每條信息 → 英文原文 chunk + 中文翻譯 chunk
  - 所有 chunk 底部附 SFC 官方原文鏈接

數據源：
  1. SFC 通函 (Circulars)         — PDF 或 HTML
  2. SFC 執法新聞 (Enforcement)   — HTML
  3. SFC 諮詢文件 (Consultations) — PDF 或 HTML
  4. SFC VATP/虛擬資產動態         — HTML
  5. SFC 新聞稿 (Press Releases)  — HTML
  + Charltons Law 執法摘要（補充源）

安裝依賴：
  pip install requests beautifulsoup4 pdfplumber

使用方法：
  雙擊 auto_collect_upload.py
"""

import requests
import json
import time
import re
import sys
import os
import io
from datetime import datetime

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ============================================================
# 配置
# ============================================================
SUPABASE_URL = "https://lsoatzzwpltpydwyfqqv.supabase.co"
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "your-supabase-service-key-here")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your-openai-api-key-here")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "your-deepseek-api-key-here")

KNOWLEDGE_TABLE = "vigo_knowledge"
QUESTIONS_TABLE = "vigo_quick_questions"
SFC_API_BASE = "https://apps.sfc.hk/edistributionWeb/api"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': '*/*'
}

# VIGO chunk 最佳長度：400-1200 字符（太短缺上下文，太長降低匹配精度）
CHUNK_MIN = 300
CHUNK_MAX = 1500
CHUNK_IDEAL = 800


# ============================================================
# PDF 文字提取
# ============================================================
def extract_text_from_pdf(pdf_bytes):
    """用 pdfplumber 從 PDF 二進制中提取文字"""
    try:
        import pdfplumber
    except ImportError:
        print("      ERROR: pip install pdfplumber")
        return None

    try:
        pdf = pdfplumber.open(io.BytesIO(pdf_bytes))
        pages_text = []
        for page in pdf.pages:
            text = page.extract_text() or ""
            if text.strip():
                pages_text.append(text)
        pdf.close()

        if not pages_text:
            return None

        full_text = "\n\n".join(pages_text)

        # 清理 PDF 提取的常見問題
        full_text = re.sub(r'(\d+)\s*\n\s*\n', r'\1\n', full_text)  # 頁碼後多餘空行
        full_text = re.sub(r'\n{3,}', '\n\n', full_text)  # 過多空行
        # 移除頁眉頁腳（SFC 通函常見格式）
        full_text = re.sub(
            r'54/F,\s*One Island East.*?www\.sfc\.hk\s*(?:Page \d+ of \d+)?',
            '', full_text, flags=re.DOTALL
        )
        full_text = re.sub(
            r'香港鰂魚涌華蘭路.*?港島東中心.*?樓',
            '', full_text
        )

        return full_text.strip()
    except Exception as e:
        print(f"      PDF extract error: {e}")
        return None


# ============================================================
# 智能拆分：按章節 / 段落拆分長文
# ============================================================
def smart_chunk_text(full_text, doc_title, max_size=CHUNK_MAX):
    """
    將長文智能拆分為多個 chunks。
    優先按章節標題拆分，其次按編號段落，最後按段落。
    每個 chunk 都帶文檔標題上下文。
    """
    if len(full_text) <= max_size:
        return [full_text]

    chunks = []

    # 策略 1：按 SFC 通函的編號段落拆分（1. 2. 3. 或 (a) (b) (c)）
    # SFC 通函典型結構：數字標題段落
    sections = re.split(r'\n(?=\d{1,2}\.\s+[A-Z])', full_text)

    if len(sections) >= 3:
        # 按編號段落拆分成功
        current_chunk = ""
        for section in sections:
            section = section.strip()
            if not section:
                continue

            if len(current_chunk) + len(section) <= max_size:
                current_chunk += ("\n\n" if current_chunk else "") + section
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                # 如果單個 section 超長，再按段落拆
                if len(section) > max_size:
                    sub_paragraphs = section.split('\n\n')
                    sub_chunk = ""
                    for para in sub_paragraphs:
                        if len(sub_chunk) + len(para) <= max_size:
                            sub_chunk += ("\n\n" if sub_chunk else "") + para
                        else:
                            if sub_chunk:
                                chunks.append(sub_chunk)
                            sub_chunk = para
                    if sub_chunk:
                        current_chunk = sub_chunk
                    else:
                        current_chunk = ""
                else:
                    current_chunk = section

        if current_chunk:
            chunks.append(current_chunk)
    else:
        # 策略 2：按段落拆分
        paragraphs = full_text.split('\n\n')
        current_chunk = ""
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            if len(current_chunk) + len(para) <= max_size:
                current_chunk += ("\n\n" if current_chunk else "") + para
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = para
        if current_chunk:
            chunks.append(current_chunk)

    # 過濾太短的 chunks（合併到前一個）
    final_chunks = []
    for chunk in chunks:
        if len(chunk) < CHUNK_MIN and final_chunks:
            final_chunks[-1] += "\n\n" + chunk
        else:
            final_chunks.append(chunk)

    # 每個 chunk 加上文檔標題上下文（幫助 VIGO 理解來源）
    contextualized = []
    for i, chunk in enumerate(final_chunks):
        if len(final_chunks) > 1:
            header = f"[{doc_title} — Part {i+1}/{len(final_chunks)}]"
        else:
            header = f"[{doc_title}]"
        contextualized.append(f"{header}\n\n{chunk}")

    return contextualized


# ============================================================
# SFC 數據抓取（自動處理 PDF 和 HTML）
# ============================================================
def fetch_sfc_content(ref, api_path):
    """
    抓取一條 SFC 內容。自動判斷 PDF 或 HTML：
    - PDF → pdfplumber 提取文字
    - HTML → 清理標籤提取正文
    返回：(text, content_type) 或 (None, None)
    """
    url = f"{SFC_API_BASE}/{api_path}?refNo={ref}&lang=EN"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code != 200:
            return None, None

        # 判斷返回類型
        content_type = resp.headers.get('content-type', '').lower()
        raw_start = resp.content[:10]

        if raw_start.startswith(b'%PDF') or 'application/pdf' in content_type:
            # ===== PDF 處理 =====
            text = extract_text_from_pdf(resp.content)
            if text and len(text) > 200:
                return text, "pdf"
            return None, None

        else:
            # ===== HTML/Text 處理 =====
            text = resp.text
            if 'You need to enable JavaScript' in text:
                return None, None

            # 清理 HTML
            text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
            text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'&[a-zA-Z]+;', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()

            if len(text) > 200:
                return text, "html"
            return None, None

    except Exception as e:
        print(f"      Fetch error: {e}")
        return None, None


# ============================================================
# 核心 API 函數
# ============================================================
def generate_embedding(text):
    text = text[:8000]
    for attempt in range(3):
        try:
            resp = requests.post("https://api.openai.com/v1/embeddings",
                headers={"Authorization": f"Bearer {OPENAI_API_KEY}",
                         "Content-Type": "application/json"},
                json={"model": "text-embedding-3-small", "input": text}, timeout=30)
            if resp.status_code == 200:
                return resp.json()["data"][0]["embedding"]
            elif resp.status_code in [429, 500, 502, 503]:
                time.sleep(min(2 ** attempt, 8))
                continue
            else:
                print(f"      Embedding {resp.status_code}")
                return None
        except Exception as e:
            print(f"      Embedding err: {e}")
            if attempt < 2: time.sleep(2)
    return None


def deepseek_chat(prompt, max_tokens=800, temperature=0.3):
    try:
        resp = requests.post("https://api.deepseek.com/chat/completions",
            headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                     "Content-Type": "application/json"},
            json={"model": "deepseek-chat",
                  "messages": [{"role": "user", "content": prompt}],
                  "max_tokens": max_tokens, "temperature": temperature},
            timeout=60)
        if resp.status_code == 200:
            return resp.json()['choices'][0]['message']['content'].strip()
        else:
            print(f"      DeepSeek {resp.status_code}")
    except Exception as e:
        print(f"      DeepSeek err: {e}")
    return None


def generate_questions(content, lang="zh"):
    if lang == "zh":
        prompt = f"你是香港金融合規專家。生成 2 個用戶可能問的繁體中文問題。\n內容：{content[:500]}\n只返回 JSON：[\"問題1？\", \"問題2？\"]"
    else:
        prompt = f"You are an HK compliance expert. Generate 2 likely user questions.\nContent: {content[:500]}\nReturn ONLY JSON: [\"Q1?\", \"Q2?\"]"
    answer = deepseek_chat(prompt, max_tokens=150, temperature=0.7)
    if not answer: return None
    try:
        answer = re.sub(r'^```json\s*', '', answer)
        answer = re.sub(r'\s*```$', '', answer)
        q = json.loads(answer.strip())
        return [x for x in q if x and len(x) >= 5][:2] if isinstance(q, list) else None
    except: return None


def upload_chunk(content, metadata):
    embedding = generate_embedding(content)
    if not embedding: return None
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    try:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/{KNOWLEDGE_TABLE}",
            headers=headers,
            json={"content": content, "metadata": metadata, "embedding": embedding},
            timeout=30)
        if resp.status_code in [200, 201]:
            result = resp.json()
            if isinstance(result, list) and len(result) > 0:
                kid = result[0].get('id')
                # Quick questions
                lang = metadata.get("language", "zh")
                questions = generate_questions(content, lang)
                if questions:
                    qh = {**headers, "Prefer": "return=minimal"}
                    for q in questions:
                        requests.post(f"{SUPABASE_URL}/rest/v1/{QUESTIONS_TABLE}",
                            headers=qh,
                            json={"question_text": q,
                                  "category": metadata.get("category", "SFC"),
                                  "keywords": metadata.get("keywords", ["SFC"]),
                                  "source_knowledge_id": kid,
                                  "source_table": "vigo_knowledge",
                                  "generation_method": "auto",
                                  "is_active": True},
                            timeout=30)
                        time.sleep(0.2)
                return kid
    except Exception as e:
        print(f"      Upload err: {e}")
    return None


# ============================================================
# 翻譯
# ============================================================
def translate_to_chinese(text):
    prompt = f"""你是 SFC 監管情報翻譯師。翻譯為繁體中文摘要。
要求：保留專業術語英文+括號，如：持牌法團 (Licensed Corporation)。保留日期、金額、編號。
原文：{text[:3500]}
只返回翻譯。"""
    return deepseek_chat(prompt, max_tokens=800, temperature=0.2)


# ============================================================
# 生成雙語 chunks
# ============================================================
def build_official_url(ref, doc_type):
    """生成 SFC 官方人類可讀鏈接"""
    if doc_type in ("circular",):
        return f"https://apps.sfc.hk/edistributionWeb/gateway/EN/circular/doc?refNo={ref}"
    elif doc_type in ("enforcement", "vatp", "press_release"):
        return f"https://apps.sfc.hk/edistributionWeb/gateway/EN/news-and-announcements/news/doc?refNo={ref}"
    elif doc_type in ("consultation", "consultation_conclusion"):
        return f"https://apps.sfc.hk/edistributionWeb/gateway/EN/consultation/doc?refNo={ref}"
    return f"https://www.sfc.hk/en/"


def create_bilingual_chunks(ref, text_chunks, doc_type, source_url):
    """
    每個 text chunk → EN 版本 + ZH 版本
    """
    all_vigo_chunks = []
    official_url = build_official_url(ref, doc_type)

    type_labels = {
        "circular": ("Circular", "通函"),
        "enforcement": ("Enforcement", "執法行動"),
        "consultation": ("Consultation", "諮詢文件"),
        "vatp": ("Virtual Asset", "虛擬資產"),
        "press_release": ("Press Release", "新聞稿"),
        "enforcement_summary": ("Enforcement Summary", "執法摘要")
    }
    en_label, zh_label = type_labels.get(doc_type, ("Update", "動態"))

    # Detect keywords from all chunks combined
    combined = " ".join(text_chunks).lower()
    keywords = ["SFC"]
    kw_map = {"virtual asset": "VATP", "vatp": "VATP", "aml": "AML",
              "aspire": "ASPIRe", "sponsor": "Sponsor", "ipo": "IPO",
              "type 1": "Type1", "type 9": "Type9", "stablecoin": "Stablecoin",
              "staking": "Staking", "enforcement": "Enforcement",
              "consultation": "Consultation", "circular": "Circular"}
    for kw, tag in kw_map.items():
        if kw in combined and tag not in keywords:
            keywords.append(tag)
    keywords = keywords[:6]

    for i, chunk_text in enumerate(text_chunks):
        part_label = f" (Part {i+1}/{len(text_chunks)})" if len(text_chunks) > 1 else ""
        base_meta = {
            "source": f"SFC_Official_{ref}",
            "source_url": official_url,
            "doc_type": doc_type,
            "category": "SFC",
            "ref_no": ref,
            "source_table": "vigo_financial",
            "keywords": keywords,
            "collected_date": datetime.now().strftime("%Y-%m-%d"),
            "content_type": "pdf_extract" if len(text_chunks) > 1 else "html"
        }

        # ── EN chunk ──
        en_content = f"【SFC {en_label}{part_label} — {ref}】\n\n"
        en_content += chunk_text
        en_content += f"\n\n---\nSource: SFC Official ({ref})\nFull document: {official_url}"

        all_vigo_chunks.append({
            "content": en_content,
            "metadata": {**base_meta, "language": "en"},
            "lang": "EN"
        })

        # ── ZH chunk ──
        zh_translation = translate_to_chinese(chunk_text)
        if zh_translation and len(zh_translation) > 80:
            zh_content = f"【SFC {zh_label}{part_label} — {ref}】\n\n"
            zh_content += zh_translation
            zh_content += f"\n\n---\n資料來源：證監會官方 ({ref})\n原文鏈接：{official_url}"

            all_vigo_chunks.append({
                "content": zh_content,
                "metadata": {**base_meta, "language": "zh"},
                "lang": "ZH"
            })

        time.sleep(1)  # Rate limit

    return all_vigo_chunks


# ============================================================
# 掃描 5 個數據源
# ============================================================
def scan_source(name, ref_prefix_list, api_path, filter_fn=None, max_items=10):
    """掃描一個 SFC 數據源"""
    print(f"\n{'=' * 50}")
    print(f"  {name}")
    print(f"{'=' * 50}")

    results = []
    found = 0

    for prefix in ref_prefix_list:
        for ref_id in prefix["range"]:
            if found >= max_items:
                break
            ref = f"{prefix['year']}{prefix['code']}{ref_id}"

            text, ctype = fetch_sfc_content(ref, api_path)
            if not text:
                continue

            # Apply filter
            if filter_fn and not filter_fn(text):
                continue

            # Smart chunk
            chunks = smart_chunk_text(text, f"SFC {ref}")
            results.append({
                "ref": ref,
                "chunks": chunks,
                "content_type": ctype,
                "doc_type": prefix.get("doc_type", "unknown"),
                "source_url": f"{SFC_API_BASE}/{api_path}?refNo={ref}&lang=EN"
            })
            found += 1
            print(f"   OK: {ref} ({ctype}, {len(chunks)} chunk{'s' if len(chunks)>1 else ''}, {len(text)} chars)")
            time.sleep(0.3)

    print(f"   Total: {found} items")
    return results


def fetch_all_sources(year, depth="quick"):
    max_ec = 8 if depth == "quick" else 20
    max_pr = 10 if depth == "quick" else 30
    max_cp = 6 if depth == "quick" else 12

    all_results = []

    # 1. Circulars (usually PDF)
    all_results += scan_source(
        "[1/5] SFC Circulars (通函)",
        [{"year": year, "code": "EC", "range": range(max_ec, 0, -1), "doc_type": "circular"},
         {"year": year-1, "code": "EC", "range": range(50, 35, -1), "doc_type": "circular"}],
        "circular/openFile", max_items=10
    )

    # 2. Enforcement News (HTML)
    enforce_kw = ['reprimand', 'fine', 'suspend', 'ban', 'prosecut',
                  'convict', 'disciplin', 'enforcement', 'sanction', 'misconduct']
    all_results += scan_source(
        "[2/5] SFC Enforcement (執法新聞)",
        [{"year": year, "code": "PR", "range": range(max_pr, 0, -1), "doc_type": "enforcement"},
         {"year": year-1, "code": "PR", "range": range(220, 220-max_pr, -1), "doc_type": "enforcement"}],
        "news/list-content",
        filter_fn=lambda t: any(k in t.lower() for k in enforce_kw),
        max_items=10
    )

    # 3. Consultations (usually PDF)
    all_results += scan_source(
        "[3/5] SFC Consultations (諮詢文件)",
        [{"year": year, "code": "CP", "range": range(max_cp, 0, -1), "doc_type": "consultation"},
         {"year": year-1, "code": "CP", "range": range(15, 0, -1), "doc_type": "consultation"}],
        "consultation/openFile", max_items=8
    )

    # 4. VATP / Virtual Asset (HTML)
    va_kw = ['virtual asset', 'vatp', 'vasp', 'crypto', 'stablecoin',
             'digital asset', 'web3', 'staking', 'aspire']
    all_results += scan_source(
        "[4/5] SFC VATP (虛擬資產)",
        [{"year": year, "code": "PR", "range": range(max_pr, 0, -1), "doc_type": "vatp"},
         {"year": year-1, "code": "PR", "range": range(220, 220-max_pr, -1), "doc_type": "vatp"}],
        "news/list-content",
        filter_fn=lambda t: any(k in t.lower() for k in va_kw),
        max_items=8
    )

    # 5. General Press Releases (HTML)
    skip_kw = enforce_kw + va_kw
    all_results += scan_source(
        "[5/5] SFC Press Releases (新聞稿)",
        [{"year": year, "code": "PR", "range": range(max_pr, 0, -1), "doc_type": "press_release"}],
        "news/list-content",
        filter_fn=lambda t: not any(k in t.lower() for k in skip_kw) and len(t) > 300,
        max_items=8
    )

    # Bonus: Charltons Law
    print(f"\n{'=' * 50}")
    print(f"  [Bonus] Charltons Law")
    print(f"{'=' * 50}")
    try:
        from bs4 import BeautifulSoup
        url = "https://www.charltonslaw.com/sfc-enforcement-actions-in-january-2026-and-december-2025/"
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            article = soup.find('div', class_='entry-content') or soup.find('article')
            if article:
                text = '\n\n'.join([e.get_text(strip=True) for e in article.find_all(['p', 'h2', 'h3', 'li'])
                                    if len(e.get_text(strip=True)) > 10])
                if len(text) > 500:
                    chunks = smart_chunk_text(text, "Charltons SFC Enforcement")
                    all_results.append({
                        "ref": "charltons_latest",
                        "chunks": chunks,
                        "content_type": "html",
                        "doc_type": "enforcement_summary",
                        "source_url": url
                    })
                    print(f"   OK: {len(chunks)} chunks, {len(text)} chars")
    except Exception as e:
        print(f"   Skip: {e}")

    return all_results


# ============================================================
# 備份
# ============================================================
def save_backup(vigo_chunks, filename):
    sections = []
    for c in vigo_chunks:
        m = c["metadata"]
        meta = '\n'.join(f"{k}: {v}" for k, v in m.items() if not isinstance(v, list))
        kw = m.get("keywords", [])
        if kw: meta += f"\nkeywords: {', '.join(kw)}"
        title = c['content'].split('\n')[0].replace('【', '').replace('】', '')
        body = '\n'.join(c['content'].split('\n')[2:])
        sections.append(f"===SECTION===\n【標題】{title}\n【內容】\n{body}\n【元數據】\n{meta}\n===END===")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(sections))
    print(f"   Backup: {filename}")


# ============================================================
# 主程序
# ============================================================
def main():
    now = datetime.now()
    year = now.year % 100

    print("=" * 60)
    print("  VIGO SFC Bilingual Collector v3.0")
    print("  PDF Extract + EN/ZH Bilingual + Official Links")
    print("  OpenAI + DeepSeek direct (v3.3)")
    print("=" * 60)
    print(f"\n  Date: {now.strftime('%Y-%m-%d %H:%M')}")
    print(f"  PDF handling: pdfplumber extract -> smart chunk")
    print(f"  Each item -> EN chunk + ZH chunk + SFC link")

    # Check dependencies
    missing = []
    try: import pdfplumber
    except: missing.append("pdfplumber")
    try: from bs4 import BeautifulSoup
    except: missing.append("beautifulsoup4")
    if missing:
        print(f"\n  Missing: {', '.join(missing)}")
        print(f"  Run: pip install {' '.join(missing)}")
        return

    print("\n  Mode:")
    print("  1. Quick update (~15 min)")
    print("  2. Full scan (~40 min)")
    print("  3. Test single source")

    mode = input("\n  (1/2/3): ").strip()

    if mode == "3":
        print("\n  a. Circulars (PDF)")
        print("  b. Enforcement (HTML)")
        print("  c. Consultations (PDF)")
        print("  d. VATP (HTML)")
        print("  e. Press Releases (HTML)")
        src = input("  (a/b/c/d/e): ").strip().lower()

        enforce_kw = ['reprimand', 'fine', 'suspend', 'ban', 'prosecut', 'convict']
        va_kw = ['virtual asset', 'vatp', 'vasp', 'crypto', 'stablecoin', 'staking', 'aspire']

        if src == "a":
            results = scan_source("Test: Circulars",
                [{"year": year, "code": "EC", "range": range(8, 0, -1), "doc_type": "circular"}],
                "circular/openFile", max_items=5)
        elif src == "b":
            results = scan_source("Test: Enforcement",
                [{"year": year, "code": "PR", "range": range(15, 0, -1), "doc_type": "enforcement"}],
                "news/list-content",
                filter_fn=lambda t: any(k in t.lower() for k in enforce_kw), max_items=5)
        elif src == "c":
            results = scan_source("Test: Consultations",
                [{"year": year, "code": "CP", "range": range(8, 0, -1), "doc_type": "consultation"}],
                "consultation/openFile", max_items=5)
        elif src == "d":
            results = scan_source("Test: VATP",
                [{"year": year, "code": "PR", "range": range(15, 0, -1), "doc_type": "vatp"}],
                "news/list-content",
                filter_fn=lambda t: any(k in t.lower() for k in va_kw), max_items=5)
        elif src == "e":
            skip = enforce_kw + va_kw
            results = scan_source("Test: Press",
                [{"year": year, "code": "PR", "range": range(15, 0, -1), "doc_type": "press_release"}],
                "news/list-content",
                filter_fn=lambda t: not any(k in t.lower() for k in skip), max_items=5)
        else:
            print("Invalid"); return
    elif mode in ("1", "2"):
        depth = "quick" if mode == "1" else "full"
        results = fetch_all_sources(year, depth)
    else:
        print("Invalid"); return

    # Deduplicate
    seen = set()
    unique = []
    for r in results:
        if r["ref"] not in seen:
            seen.add(r["ref"])
            unique.append(r)
    results = unique

    if not results:
        print("\n  No items found."); return

    # Summary
    total_chunks = sum(len(r["chunks"]) for r in results)
    pdf_count = sum(1 for r in results if r["content_type"] == "pdf")
    html_count = sum(1 for r in results if r["content_type"] == "html")

    print(f"\n{'=' * 50}")
    print(f"  Collected: {len(results)} SFC items")
    print(f"    PDF documents: {pdf_count}")
    print(f"    HTML pages: {html_count}")
    print(f"    Text chunks: {total_chunks}")
    print(f"    VIGO chunks: ~{total_chunks * 2} (EN + ZH)")

    # Generate bilingual VIGO chunks
    print(f"\n{'=' * 50}")
    print(f"  Generating bilingual chunks...")
    print(f"{'=' * 50}")

    all_vigo_chunks = []
    for i, r in enumerate(results, 1):
        print(f"\n  [{i}/{len(results)}] {r['ref']} ({r['content_type']}, "
              f"{len(r['chunks'])} text chunks)")

        vigo_chunks = create_bilingual_chunks(
            r["ref"], r["chunks"], r["doc_type"], r["source_url"])

        en_count = sum(1 for c in vigo_chunks if c["lang"] == "EN")
        zh_count = sum(1 for c in vigo_chunks if c["lang"] == "ZH")
        print(f"      -> {en_count} EN + {zh_count} ZH chunks")

        all_vigo_chunks.extend(vigo_chunks)

    if not all_vigo_chunks:
        print("\n  No chunks generated."); return

    en_total = sum(1 for c in all_vigo_chunks if c["lang"] == "EN")
    zh_total = sum(1 for c in all_vigo_chunks if c["lang"] == "ZH")
    print(f"\n{'=' * 50}")
    print(f"  Generated: {len(all_vigo_chunks)} VIGO chunks")
    print(f"    English: {en_total}")
    print(f"    Chinese: {zh_total}")

    # Backup
    backup = f"VIGO_SFC_bilingual_{now.strftime('%Y%m%d')}.md"
    save_backup(all_vigo_chunks, backup)

    # Upload
    answer = input(f"\n  Upload {len(all_vigo_chunks)} chunks? (y/n): ").strip().lower()
    if answer != 'y':
        print(f"\n  Data saved to: {backup}"); return

    print(f"\n{'=' * 50}")
    print(f"  Uploading...")
    print(f"{'=' * 50}")

    stats = {"ok": 0, "fail": 0, "en": 0, "zh": 0}
    t0 = time.time()

    for i, c in enumerate(all_vigo_chunks, 1):
        lang = c["lang"]
        first = c["content"].split('\n')[0][:45]
        print(f"  [{i:02d}/{len(all_vigo_chunks)}] [{lang}] {first}")

        kid = upload_chunk(c["content"], c["metadata"])
        if kid:
            stats["ok"] += 1
            stats[lang.lower()] = stats.get(lang.lower(), 0) + 1
            print(f"      OK (ID: {kid})")
        else:
            stats["fail"] += 1
            print(f"      FAILED")
        time.sleep(0.5)

    elapsed = time.time() - t0
    print(f"\n{'=' * 60}")
    print(f"  DONE! {elapsed/60:.1f} min")
    print(f"  Success: {stats['ok']}/{len(all_vigo_chunks)}")
    print(f"    EN: {stats.get('en', 0)}")
    print(f"    ZH: {stats.get('zh', 0)}")
    print(f"  Failed: {stats['fail']}")
    print(f"  Backup: {backup}")
    print(f"{'=' * 60}")
    print(f"\n  Test in VIGO:")
    print(f'    "SFC最新通函內容是什麼？"')
    print(f'    "What did the latest SFC circular say about sponsors?"')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Cancelled")
    except Exception as e:
        print(f"\n  ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

    print("\n")
    input("Press Enter to close...")
