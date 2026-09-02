#!/usr/bin/env python3
"""Weekly fire-safety paper monitor for the user's journal RSS workbook.

Stdlib-only on purpose: cron jobs run in the Hermes environment where pip/openpyxl
may not be available. The script reads a simple two-column .xlsx, fetches RSS/Atom
feeds, uses snapshot diff for feeds without item-level timestamps, falls back to
Crossref for journals without RSS, and writes both Markdown and XLSX artifacts.
"""
from __future__ import annotations

import argparse
import concurrent.futures as futures
import datetime as dt
from email.utils import parsedate_to_datetime
import html
import json
import os
from pathlib import Path
import re
import shutil
import sys
import time
from typing import Dict, Iterable, List, Optional, Tuple
import urllib.parse
import urllib.request
from xml.etree import ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED

TZ = dt.timezone(dt.timedelta(hours=8), name="Asia/Shanghai")
HERMES_HOME = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes")).expanduser()
BASE_DIR = Path(
    os.environ.get(
        "FIRE_SAFETY_MONITOR_DIR",
        HERMES_HOME / "data" / "fire_safety_paper_monitor",
    )
).expanduser()
INPUT_XLSX = BASE_DIR / "journal_rss_table.xlsx"
FALLBACK_INPUT_XLSX = INPUT_XLSX
STATE_JSON = BASE_DIR / "state.json"
LATEST_REPORT = BASE_DIR / "latest_report.md"
LATEST_SNAPSHOT_XLSX = BASE_DIR / "snapshot_latest.xlsx"
REPORT_DIR = BASE_DIR / "reports"
SNAPSHOT_DIR = BASE_DIR / "snapshots"
DISCOVERED_FEEDS_JSON = BASE_DIR / "discovered_feeds.json"

KEYWORD_RE = re.compile(r"fire|high[ -]temperature|elevated[ -]temperature", re.I)
# First-party latest-article sources for journals without a publisher RSS URL.
JOURNAL_PROFILES = {
    "Fire Technology": {
        "listing_url": "https://link.springer.com/journal/10694/articles",
        "issn": "1572-8099",
    },
}
XML_NS_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
SPREADSHEET_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"

USER_AGENT = "HermesAcademicRSS/1.0 (weekly fire safety paper monitor; https://hermes-agent.nousresearch.com)"
HTTP_TIMEOUT = 25
MAX_WORKERS = 8


def now_bj() -> dt.datetime:
    return dt.datetime.now(TZ)


def log(msg: str) -> None:
    print(msg, flush=True)


def norm_space(s: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(str(s or ""))).strip()


def strip_tags(s: str) -> str:
    s = re.sub(r"(?is)<(script|style).*?</\1>", " ", s or "")
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    return norm_space(s)


def local_name(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[1]
    return tag


def child_text(el: ET.Element, names: Iterable[str]) -> str:
    wanted = set(names)
    for ch in list(el):
        if local_name(ch.tag) in wanted:
            txt = "".join(ch.itertext())
            if txt and txt.strip():
                return norm_space(txt)
    return ""


def all_child_texts(el: ET.Element, names: Iterable[str]) -> List[str]:
    wanted = set(names)
    out = []
    for ch in list(el):
        if local_name(ch.tag) in wanted:
            txt = norm_space("".join(ch.itertext()))
            if txt:
                out.append(txt)
    return out


def col_index(cell_ref: str) -> int:
    m = re.match(r"([A-Z]+)", cell_ref or "")
    letters = m.group(1) if m else "A"
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def read_xlsx_journals(path: Path) -> List[Dict[str, str]]:
    """Read first worksheet from the user's two-column workbook."""
    with ZipFile(path) as z:
        shared: List[str] = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall(f".//{{{SPREADSHEET_NS}}}si"):
                shared.append("".join(t.text or "" for t in si.findall(f".//{{{SPREADSHEET_NS}}}t")))

        wb_root = ET.fromstring(z.read("xl/workbook.xml"))
        rel_root = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        relmap = {r.attrib["Id"]: r.attrib["Target"] for r in rel_root}
        first_sheet = wb_root.find(f".//{{{SPREADSHEET_NS}}}sheet")
        if first_sheet is None:
            return []
        rid = first_sheet.attrib.get(f"{{{XML_NS_REL}}}id")
        target = relmap.get(rid or "", "worksheets/sheet1.xml")
        sheet_path = "xl/" + target.lstrip("/") if not target.startswith("xl/") else target
        root = ET.fromstring(z.read(sheet_path))

        grid: Dict[Tuple[int, int], str] = {}
        max_row = 0
        for row in root.findall(f".//{{{SPREADSHEET_NS}}}sheetData/{{{SPREADSHEET_NS}}}row"):
            r_idx = int(row.attrib.get("r", "0")) - 1
            max_row = max(max_row, r_idx + 1)
            for c in row.findall(f"{{{SPREADSHEET_NS}}}c"):
                ci = col_index(c.attrib.get("r", "A"))
                ctype = c.attrib.get("t")
                value = ""
                if ctype == "s":
                    v = c.find(f"{{{SPREADSHEET_NS}}}v")
                    if v is not None and v.text is not None:
                        idx = int(v.text)
                        value = shared[idx] if 0 <= idx < len(shared) else ""
                elif ctype == "inlineStr":
                    is_el = c.find(f"{{{SPREADSHEET_NS}}}is")
                    value = "".join(is_el.itertext()) if is_el is not None else ""
                else:
                    v = c.find(f"{{{SPREADSHEET_NS}}}v")
                    value = v.text if v is not None and v.text is not None else ""
                grid[(r_idx, ci)] = norm_space(value)

    journals = []
    for r in range(1, max_row):
        name = grid.get((r, 0), "")
        rss = grid.get((r, 1), "")
        if name:
            journals.append({"journal": name, "rss": rss})
    return journals


def fetch_url(url: str, accept: str = "application/rss+xml, application/atom+xml, application/xml, text/xml, */*", timeout: int = HTTP_TIMEOUT) -> Tuple[Optional[bytes], Optional[str], Optional[str]]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": accept,
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            final_url = getattr(r, "url", url)
            # Some publisher feeds (notably World Scientific etoc feeds) exceed
            # 2.5 MB. Keep a finite cap so a bad endpoint cannot exhaust memory,
            # but allow normal journal feeds through intact.
            return r.read(12_000_000), final_url, None
    except Exception as e:
        return None, None, f"{type(e).__name__}: {e}"


def parse_dt(s: str) -> Optional[dt.datetime]:
    s = norm_space(s)
    if not s:
        return None
    # Remove bracketed timezone labels that parsedate sometimes dislikes.
    s2 = re.sub(r"\s*\([^)]*\)\s*$", "", s)
    try:
        d = parsedate_to_datetime(s2)
        if d.tzinfo is None:
            d = d.replace(tzinfo=dt.timezone.utc)
        return d.astimezone(TZ)
    except Exception:
        pass
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ", "%d %B %Y", "%d %b %Y", "%Y-%m-%d", "%Y/%m/%d"):
        try:
            if fmt.endswith("Z"):
                d = dt.datetime.strptime(s2, fmt).replace(tzinfo=dt.timezone.utc)
            elif "%z" in fmt:
                d = dt.datetime.strptime(s2, fmt)
            else:
                d = dt.datetime.strptime(s2[:10], fmt).replace(tzinfo=TZ)
            return d.astimezone(TZ)
        except Exception:
            continue
    try:
        d = dt.datetime.fromisoformat(s2.replace("Z", "+00:00"))
        if d.tzinfo is None:
            d = d.replace(tzinfo=TZ)
        return d.astimezone(TZ)
    except Exception:
        return None


def undated_detection_reason(
    *,
    first_run: bool,
    feed_seen_before: bool,
    item_seen_before: bool,
    first_reported: str,
    since: dt.datetime,
    now: dt.datetime,
) -> str:
    """Return why an undated RSS item belongs in the current weekly report.

    A snapshot diff must remain visible on deterministic reruns throughout the
    same seven-day reporting window. Otherwise, the first run reports it once
    and the immediately repeated run silently drops it.
    """
    if not first_run and feed_seen_before and not item_seen_before:
        return "snapshot_diff"
    if item_seen_before and first_reported:
        first_reported_dt = parse_dt(first_reported)
        if first_reported_dt and since <= first_reported_dt <= now + dt.timedelta(hours=1):
            return "snapshot_first_reported_within_7d"
    return ""


def iso_date_from_parts(parts: dict) -> str:
    # Crossref date-parts: [[YYYY, MM, DD]]
    try:
        arr = parts.get("date-parts", [[]])[0]
        if len(arr) >= 3:
            return f"{int(arr[0]):04d}-{int(arr[1]):02d}-{int(arr[2]):02d}"
        if len(arr) == 2:
            return f"{int(arr[0]):04d}-{int(arr[1]):02d}"
        if len(arr) == 1:
            return f"{int(arr[0]):04d}"
    except Exception:
        pass
    return ""


def canonical_key(title: str, link: str, guid: str = "") -> str:
    # Normalize DOI-shaped URLs from publisher pages and doi.org to the same key.
    # This lets the first-party listing win over a Crossref copy of the same work.
    doi_match = re.search(r"10\.\d{4,9}/[-._;()/:a-z0-9]+", " ".join([guid or "", link or ""]), re.I)
    if doi_match:
        return "doi:" + doi_match.group(0).lower().rstrip(".,;)")
    base = guid or link or title
    base = base.strip()
    base = re.sub(r"[?#].*$", "", base)
    base = base.lower().strip()
    if not base:
        base = re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()
    return base[:500]


def extract_authors_from_description(desc: str) -> str:
    if not desc:
        return ""
    text = html.unescape(desc)
    patterns = [
        r"Author\(s\)\s*:\s*(.*?)(?:</p>|<br\s*/?>|$)",
        r"Authors?\s*:\s*(.*?)(?:</p>|<br\s*/?>|$)",
        r"By\s+(.+?)(?:</p>|<br\s*/?>|$)",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.I | re.S)
        if m:
            return strip_tags(m.group(1))
    return ""


def extract_pubdate_from_description(desc: str) -> str:
    if not desc:
        return ""
    text = html.unescape(desc)
    m = re.search(r"Publication date\s*:\s*(.*?)(?:</p>|<br\s*/?>|$)", text, re.I | re.S)
    if m:
        return strip_tags(m.group(1))
    return ""


def parse_feed(xml_bytes: bytes, journal: str, feed_url: str) -> List[Dict[str, str]]:
    text = xml_bytes.decode("utf-8", "replace").lstrip("\ufeff")
    root = ET.fromstring(text)
    root_local = local_name(root.tag).lower()
    items: List[ET.Element] = []
    if root_local == "rss":
        channel = None
        for ch in list(root):
            if local_name(ch.tag).lower() == "channel":
                channel = ch
                break
        if channel is not None:
            items = [ch for ch in list(channel) if local_name(ch.tag).lower() == "item"]
    elif root_local == "feed":
        items = [ch for ch in list(root) if local_name(ch.tag).lower() == "entry"]
    else:
        items = [ch for ch in list(root) if local_name(ch.tag).lower() in {"item", "entry"}]

    entries = []
    for item in items:
        title = child_text(item, ["title"])
        desc = child_text(item, ["description", "summary", "content", "encoded"])

        link = ""
        for ch in list(item):
            if local_name(ch.tag).lower() == "link":
                href = ch.attrib.get("href", "")
                rel = ch.attrib.get("rel", "alternate")
                if href and rel in {"alternate", "", None}:
                    link = href
                    break
                txt = norm_space("".join(ch.itertext()))
                if txt and not link:
                    link = txt
        guid = child_text(item, ["guid", "id"])
        if not link and guid.startswith("http"):
            link = guid

        # Item-level timestamp only. Do not treat ScienceDirect description
        # "Publication date" as a feed timestamp for the past-week test.
        date_text = child_text(item, ["pubDate", "published", "updated", "date", "issued", "modified"])
        date_dt = parse_dt(date_text) if date_text else None
        display_date = date_text or extract_pubdate_from_description(desc)

        authors = []
        authors.extend(all_child_texts(item, ["creator", "author", "authors"]))
        # Atom authors are often <author><name>...</name></author>
        for ch in list(item):
            if local_name(ch.tag).lower() == "author":
                nm = child_text(ch, ["name"])
                if nm:
                    authors.append(nm)
        if not authors:
            a = extract_authors_from_description(desc)
            if a:
                authors.append(a)
        # De-duplicate while preserving order.
        seen_a = set()
        authors_clean = []
        for a in authors:
            aa = norm_space(a)
            if aa and aa.lower() not in seen_a:
                seen_a.add(aa.lower())
                authors_clean.append(aa)

        if title:
            entries.append({
                "journal": journal,
                "title": title,
                "authors": "; ".join(authors_clean),
                "link": link,
                "guid": guid,
                "item_date": display_date,
                "item_datetime": date_dt.isoformat() if date_dt else "",
                "has_time_marker": "yes" if date_dt else "no",
                "feed_url": feed_url,
                "source": "rss",
                "key": canonical_key(title, link, guid),
            })
    return entries


def title_matches(title: str) -> bool:
    return bool(KEYWORD_RE.search(title or ""))


def title_similarity(a: str, b: str) -> float:
    # Simple token Jaccard for validating Crossref title/container matches.
    toks_a = set(re.findall(r"[a-z0-9]+", (a or "").lower()))
    toks_b = set(re.findall(r"[a-z0-9]+", (b or "").lower()))
    if not toks_a or not toks_b:
        return 0.0
    return len(toks_a & toks_b) / len(toks_a | toks_b)


def crossref_authors(work: dict) -> str:
    people = []
    for a in work.get("author") or []:
        name = norm_space(" ".join(x for x in [a.get("given", ""), a.get("family", "")] if x))
        if name:
            people.append(name)
    return "; ".join(people)


def crossref_lookup_by_title(title: str, journal: str = "") -> Tuple[str, str, str]:
    # returns (authors, date, link) when a high-similarity Crossref hit exists.
    params = {"query.title": title, "rows": "1", "select": "title,author,URL,DOI,published-print,published-online,created,issued,container-title"}
    if journal:
        params["query.container-title"] = journal
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(params)
    data, _, err = fetch_url(url, accept="application/json", timeout=20)
    if err or not data:
        return "", "", ""
    try:
        msg = json.loads(data.decode("utf-8", "replace")).get("message", {})
        items = msg.get("items") or []
        if not items:
            return "", "", ""
        w = items[0]
        hit_title = (w.get("title") or [""])[0]
        if title_similarity(title, hit_title) < 0.78:
            return "", "", ""
        authors = crossref_authors(w)
        date = ""
        for fld in ("published-online", "published-print", "issued", "created"):
            if isinstance(w.get(fld), dict):
                date = iso_date_from_parts(w[fld])
                if date:
                    break
        link = w.get("URL") or ("https://doi.org/" + w.get("DOI") if w.get("DOI") else "")
        return authors, date, link
    except Exception:
        return "", "", ""


def crossref_recent_for_journal(journal: str, since_date: dt.date, until_date: dt.date) -> List[Dict[str, str]]:
    # Crossref created/indexed date is not identical to issue publication date;
    # it is used only as a fallback for journals with no RSS in the workbook.
    profile = JOURNAL_PROFILES.get(journal, {})
    issn = profile.get("issn", "")
    params = {
        "query.container-title": journal,
        "filter": f"from-created-date:{since_date.isoformat()},until-created-date:{until_date.isoformat()},type:journal-article",
        "rows": "30",
        "select": "title,author,URL,DOI,published-print,published-online,created,issued,container-title",
        "sort": "created",
        "order": "desc",
    }
    # An ISSN-scoped endpoint is more precise than a title query. Use it when
    # a journal profile provides an authoritative online ISSN.
    endpoint = f"https://api.crossref.org/journals/{issn}/works" if issn else "https://api.crossref.org/works"
    url = endpoint + "?" + urllib.parse.urlencode(params)
    data, _, err = fetch_url(url, accept="application/json", timeout=25)
    if err or not data:
        return []
    out = []
    try:
        items = json.loads(data.decode("utf-8", "replace")).get("message", {}).get("items") or []
    except Exception:
        return []
    for w in items:
        title = norm_space((w.get("title") or [""])[0])
        if not title or not title_matches(title):
            continue
        containers = [norm_space(x) for x in (w.get("container-title") or [])]
        if containers:
            best = max(title_similarity(journal, c) for c in containers)
            if best < 0.55:
                continue
        date = ""
        date_dt = None
        for fld in ("published-online", "published-print", "issued", "created"):
            if isinstance(w.get(fld), dict):
                date = iso_date_from_parts(w[fld])
                if date:
                    date_dt = parse_dt(date)
                    break
        link = w.get("URL") or ("https://doi.org/" + w.get("DOI") if w.get("DOI") else "")
        out.append({
            "journal": journal,
            "title": title,
            "authors": crossref_authors(w),
            "link": link,
            "guid": w.get("DOI", ""),
            "item_date": date,
            "item_datetime": date_dt.isoformat() if date_dt else "",
            "has_time_marker": "yes" if date_dt else "no",
            "feed_url": "",
            "source": "crossref-no-rss",
            "key": canonical_key(title, link, w.get("DOI", "")),
        })
    return out


def validate_feed_candidate(url: str, journal: str) -> bool:
    data, _, err = fetch_url(url, timeout=15)
    if err or not data:
        return False
    try:
        entries = parse_feed(data, journal, url)
    except Exception:
        return False
    if not entries:
        return False
    # Accept if feed titles contain at least one entry and the URL is a known publisher feed.
    return True


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def save_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def col_letters(n: int) -> str:
    s = ""
    n += 1
    while n:
        n, rem = divmod(n - 1, 26)
        s = chr(65 + rem) + s
    return s


def write_simple_xlsx(path: Path, sheet_name: str, headers: List[str], rows: List[List[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet_name = (sheet_name or "Sheet1")[:31]
    all_rows = [headers] + rows
    worksheet_rows = []
    for r_idx, row in enumerate(all_rows, 1):
        cells = []
        for c_idx, val in enumerate(row, 0):
            ref = f"{col_letters(c_idx)}{r_idx}"
            text = html.escape("" if val is None else str(val), quote=False)
            cells.append(f'<c r="{ref}" t="inlineStr"><is><t>{text}</t></is></c>')
        worksheet_rows.append(f'<row r="{r_idx}">' + "".join(cells) + "</row>")
    max_col = col_letters(max(0, len(headers) - 1))
    dimension = f"A1:{max_col}{len(all_rows)}"
    sheet_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="{SPREADSHEET_NS}" xmlns:r="{XML_NS_REL}">
  <dimension ref="{dimension}"/>
  <sheetData>{''.join(worksheet_rows)}</sheetData>
</worksheet>'''
    workbook_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="{SPREADSHEET_NS}" xmlns:r="{XML_NS_REL}"><sheets><sheet name="{html.escape(sheet_name)}" sheetId="1" r:id="rId1"/></sheets></workbook>'''
    rels_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="{PKG_REL_NS}"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>'''
    wb_rels_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="{PKG_REL_NS}"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/></Relationships>'''
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>'''
    with ZipFile(path, "w", ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels_xml)
        z.writestr("xl/workbook.xml", workbook_xml)
        z.writestr("xl/_rels/workbook.xml.rels", wb_rels_xml)
        z.writestr("xl/worksheets/sheet1.xml", sheet_xml)


def format_report(matches: List[Dict[str, str]], since: dt.datetime, now: dt.datetime) -> str:
    title = f"Fire-Safety Weekly Paper Report ({since.date().isoformat()} to {now.date().isoformat()})"
    if not matches:
        return title + "\n\nNo new papers matched the configured title terms during the reporting window."
    lines = [title, ""]
    for i, m in enumerate(matches, 1):
        authors = m.get("authors") or "Not provided"
        item_date = m.get("item_date") or "Not provided"
        link = m.get("link") or "Not provided"
        lines.extend([
            f"{i}. Journal: {m.get('journal','')}",
            f"   Paper title: {m.get('title','')}",
            f"   Authors: {authors}",
            f"   Link: {link}",
            f"   Item date: {item_date}",
            "",
        ])
    return "\n".join(lines).rstrip()


def process_rss_journal(j: Dict[str, str]) -> Tuple[str, List[Dict[str, str]], Optional[str]]:
    journal = j["journal"]
    rss = j.get("rss", "").strip()
    if not rss:
        return journal, [], "no_rss"
    data, final_url, err = fetch_url(rss)
    if err or not data:
        return journal, [], err or "fetch_failed"
    try:
        entries = parse_feed(data, journal, final_url or rss)
        return journal, entries, None
    except Exception as e:
        return journal, [], f"parse_error: {type(e).__name__}: {e}"


def process_first_party_listing(journal: str) -> Tuple[List[Dict[str, str]], Optional[str]]:
    """Parse a configured Springer latest-articles page into snapshot entries."""
    profile = JOURNAL_PROFILES.get(journal, {})
    listing_url = profile.get("listing_url", "")
    if not listing_url:
        return [], "no_listing_profile"
    data, final_url, err = fetch_url(listing_url, accept="text/html,application/xhtml+xml,*/*")
    if err or not data:
        return [], err or "fetch_failed"
    page = data.decode("utf-8", "replace")
    entries: List[Dict[str, str]] = []
    for block in re.findall(r"(?is)<article\b[^>]*>(.*?)</article>", page):
        title_match = re.search(r"(?is)<h2[^>]*>.*?<a\s+[^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", block)
        if not title_match:
            continue
        href, raw_title = title_match.groups()
        title = strip_tags(raw_title)
        if not title:
            continue
        link = urllib.parse.urljoin(final_url or listing_url, html.unescape(href))
        authors = [strip_tags(x) for x in re.findall(r"(?is)<li[^>]*app-author-list__item[^>]*>(.*?)</li>", block)]
        authors = [a for a in authors if a]
        meta = strip_tags(block)
        date_match = re.search(r"\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b", meta)
        item_date = date_match.group(0) if date_match else ""
        item_dt = parse_dt(item_date) if item_date else None
        entries.append({
            "journal": journal,
            "title": title,
            "authors": "; ".join(authors),
            "link": link,
            "guid": "",
            "item_date": item_date,
            "item_datetime": item_dt.isoformat() if item_dt else "",
            "has_time_marker": "yes" if item_dt else "no",
            "feed_url": final_url or listing_url,
            "source": "springer-homepage",
            "key": canonical_key(title, link),
        })
    return entries, None


def run(no_update: bool = False, debug: bool = False) -> int:
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    if not INPUT_XLSX.exists() and FALLBACK_INPUT_XLSX.exists():
        shutil.copyfile(FALLBACK_INPUT_XLSX, INPUT_XLSX)
    if not INPUT_XLSX.exists():
        raise SystemExit(f"Input workbook not found: {INPUT_XLSX}")

    now = now_bj()
    since = now - dt.timedelta(days=7)
    today = now.date()
    since_date = since.date()
    run_stamp = now.strftime("%Y%m%d_%H%M%S")

    journals = read_xlsx_journals(INPUT_XLSX)
    with_rss = [j for j in journals if j.get("rss")]
    no_rss = [j for j in journals if not j.get("rss")]
    prev_state = load_json(STATE_JSON, {})
    prev_seen = prev_state.get("seen", {}) if isinstance(prev_state, dict) else {}

    log(f"scan_start={now.isoformat()}")
    log(f"input_workbook={INPUT_XLSX}")
    log(f"journals_total={len(journals)} with_rss={len(with_rss)} no_rss={len(no_rss)}")

    all_entries: List[Dict[str, str]] = []
    feed_errors: Dict[str, str] = {}
    homepage_errors: Dict[str, str] = {}
    with futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        fut_map = {ex.submit(process_rss_journal, j): j for j in with_rss}
        for fut in futures.as_completed(fut_map):
            journal, entries, err = fut.result()
            if err:
                feed_errors[journal] = err
            all_entries.extend(entries)

    # Some journals have no stable RSS URL but expose a publisher-maintained
    # latest-articles listing. Snapshot that first-party listing as well.
    for j in no_rss:
        if j["journal"] not in JOURNAL_PROFILES:
            continue
        if debug:
            log(f"first_party_listing {j['journal']}")
        entries, err = process_first_party_listing(j["journal"])
        if err:
            homepage_errors[j["journal"]] = err
        all_entries.extend(entries)

    # Crossref fallback for no-RSS journals. It is intentionally bounded and only
    # checks recent Crossref-created journal articles, then applies the title filter.
    crossref_entries: List[Dict[str, str]] = []
    # Use Crossref not only for journals with blank RSS cells, but also as a
    # bounded fallback for RSS URLs that were blocked or unparsable this run.
    crossref_fallback_journals = list(no_rss) + [{"journal": k, "rss": ""} for k in sorted(feed_errors)]
    for idx, j in enumerate(crossref_fallback_journals, 1):
        if debug:
            log(f"crossref_fallback {idx}/{len(crossref_fallback_journals)} {j['journal']}")
        try:
            crossref_entries.extend(crossref_recent_for_journal(j["journal"], since_date, today))
        except Exception:
            pass
        time.sleep(0.05)
    all_entries.extend(crossref_entries)

    # Build new state and detect matches.
    new_seen: Dict[str, Dict[str, dict]] = {}
    matches: List[Dict[str, str]] = []
    first_run = not bool(prev_seen)
    for e in all_entries:
        feed_key = e.get("feed_url") or ("crossref:" + e.get("journal", ""))
        key = e.get("key") or canonical_key(e.get("title", ""), e.get("link", ""), e.get("guid", ""))
        previous_item = prev_seen.get(feed_key, {}).get(key, {})
        first_seen = previous_item.get("first_seen") or now.isoformat()
        state_item = {
            "journal": e.get("journal", ""),
            "title": e.get("title", ""),
            "link": e.get("link", ""),
            "authors": e.get("authors", ""),
            "item_date": e.get("item_date", ""),
            "first_seen": first_seen,
            "first_reported": previous_item.get("first_reported", ""),
            "last_seen": now.isoformat(),
        }
        new_seen.setdefault(feed_key, {})[key] = state_item
        if not title_matches(e.get("title", "")):
            continue

        include = False
        reason = ""
        if e.get("item_datetime"):
            parsed = parse_dt(e["item_datetime"])
            if parsed and since <= parsed <= now + dt.timedelta(hours=1):
                include = True
                reason = "item_date_within_7d"
        else:
            # RSS without a real item-level timestamp: report a new snapshot
            # diff and keep it visible on reruns during the same weekly window.
            reason = undated_detection_reason(
                first_run=first_run,
                feed_seen_before=feed_key in prev_seen,
                item_seen_before=bool(previous_item),
                first_reported=state_item["first_reported"],
                since=since,
                now=now,
            )
            include = bool(reason)
            # For Crossref fallback, created date is usually available; if not,
            # also use diff after baseline exists.
        if e.get("source", "").startswith("crossref") and e.get("item_datetime"):
            parsed = parse_dt(e["item_datetime"])
            if parsed and since <= parsed <= now + dt.timedelta(days=1):
                include = True
                reason = "crossref_created_within_7d"

        if include:
            if reason.startswith("snapshot") and not state_item["first_reported"]:
                state_item["first_reported"] = now.isoformat()
            e = dict(e)
            e["detection_method"] = reason
            # RSS and first-party listing records can be enriched from Crossref.
            suspicious_authors = bool(re.search(r"\b(ORCID|Dept\.|Department|Univ\.|University|Email:|Professor|Student|Fellow)\b", e.get("authors", ""), re.I)) or len(e.get("authors", "")) > 280
            use_crossref_enrichment = e.get("source") in {"rss", "springer-homepage"}
            if use_crossref_enrichment and (not e.get("authors") or not e.get("item_date") or suspicious_authors or e.get("source") == "springer-homepage"):
                ca, cd, clink = crossref_lookup_by_title(e.get("title", ""), e.get("journal", ""))
                if (not e.get("authors") or suspicious_authors or e.get("source") == "springer-homepage") and ca:
                    e["authors"] = ca
                if not e.get("item_date") and cd:
                    e["item_date"] = cd
                if not e.get("link") and clink:
                    e["link"] = clink
            matches.append(e)

    # De-duplicate matches by canonical key/title.
    deduped: List[Dict[str, str]] = []
    seen_keys = set()
    for e in sorted(matches, key=lambda x: (x.get("journal", ""), x.get("title", ""))):
        k = e.get("key") or canonical_key(e.get("title", ""), e.get("link", ""), e.get("guid", ""))
        kt = re.sub(r"[^a-z0-9]+", " ", e.get("title", "").lower()).strip()
        if k in seen_keys or kt in seen_keys:
            continue
        seen_keys.add(k); seen_keys.add(kt)
        deduped.append(e)
    matches = deduped

    report_md = format_report(matches, since, now)

    headers = ["run_at", "journal", "title", "authors", "link", "item_date", "source", "detection_method", "feed_url", "key"]
    match_rows = [[now.isoformat(), m.get("journal", ""), m.get("title", ""), m.get("authors", "") or "Not provided", m.get("link", ""), m.get("item_date", "") or "Not provided", m.get("source", ""), m.get("detection_method", ""), m.get("feed_url", ""), m.get("key", "")] for m in matches]
    snapshot_rows = [[now.isoformat(), e.get("journal", ""), e.get("title", ""), e.get("authors", ""), e.get("link", ""), e.get("item_date", ""), e.get("source", ""), e.get("has_time_marker", ""), e.get("feed_url", ""), e.get("key", "")] for e in all_entries]

    report_xlsx = REPORT_DIR / f"fire_safety_weekly_{run_stamp}.xlsx"
    report_md_path = REPORT_DIR / f"fire_safety_weekly_{run_stamp}.md"
    snapshot_xlsx = SNAPSHOT_DIR / f"snapshot_{run_stamp}.xlsx"

    if not no_update:
        write_simple_xlsx(report_xlsx, "weekly_matches", headers, match_rows)
        write_simple_xlsx(snapshot_xlsx, "snapshot", headers, snapshot_rows)
        write_simple_xlsx(LATEST_SNAPSHOT_XLSX, "snapshot", headers, snapshot_rows)
        report_md_path.write_text(report_md, encoding="utf-8")
        LATEST_REPORT.write_text(report_md, encoding="utf-8")
        state = {
            "last_run_at": now.isoformat(),
            "since": since.isoformat(),
            "input_workbook": str(INPUT_XLSX),
            "latest_report_md": str(LATEST_REPORT),
            "latest_report_xlsx": str(report_xlsx),
            "latest_snapshot_xlsx": str(LATEST_SNAPSHOT_XLSX),
            "journals_total": len(journals),
            "with_rss": len(with_rss),
            "no_rss": len(no_rss),
            "feed_errors": feed_errors,
            "homepage_errors": homepage_errors,
            "entries_total": len(all_entries),
            "matches_total": len(matches),
            "seen": new_seen,
        }
        save_json(STATE_JSON, state)
    else:
        report_xlsx = Path("DRY_RUN_NOT_WRITTEN")
        snapshot_xlsx = Path("DRY_RUN_NOT_WRITTEN")
        report_md_path = Path("DRY_RUN_NOT_WRITTEN")

    log(f"entries_total={len(all_entries)} matches_total={len(matches)} first_run={first_run}")
    log(f"rss_feed_errors={len(feed_errors)} crossref_fallback_entries={len(crossref_entries)}")
    if debug and feed_errors:
        for k, v in sorted(feed_errors.items()):
            log(f"feed_error | {k} | {v}")
    log(f"report_md={report_md_path}")
    log(f"report_xlsx={report_xlsx}")
    log(f"snapshot_xlsx={snapshot_xlsx}")
    log("BEGIN_REPORT")
    log(report_md)
    log("END_REPORT")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-update", action="store_true", help="Run without updating state or writing reports")
    ap.add_argument("--debug", action="store_true")
    args = ap.parse_args(argv)
    return run(no_update=args.no_update, debug=args.debug)


if __name__ == "__main__":
    raise SystemExit(main())
