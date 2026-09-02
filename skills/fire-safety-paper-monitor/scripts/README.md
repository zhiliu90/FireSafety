# Scripts

## English (Normative)

## weekly-scan.py

Deterministic collector for the weekly monitor. It reads `journal_rss_table.xlsx`, retrieves RSS/Atom feeds, uses publisher and Crossref fallbacks, applies the title filter, persists snapshots, and writes Markdown/XLSX reports.

```bash
python weekly-scan.py --no-update --debug
python weekly-scan.py
```

Set `FIRE_SAFETY_MONITOR_DIR` to the monitor data directory.

## weekly-send.py

Freshness gate for the summary stage. It prints `latest_report.md` only when the collector state exists and is no older than eight hours.

```bash
python weekly-send.py
```

The host agent consumes its output and performs full-text/abstract retrieval, summaries, browser fallback, and delivery.

---

## Chinese Translation (Reference Only)

The following Chinese text is provided only as a translation to help Chinese-speaking readers. The English section above is the normative version.

## weekly-scan.py

每周监测的确定性采集脚本。它读取 `journal_rss_table.xlsx`，抓取RSS/Atom，使用出版社和Crossref后备，执行题名筛选，保存快照，并生成Markdown/XLSX报告。

```bash
python weekly-scan.py --no-update --debug
python weekly-scan.py
```

通过 `FIRE_SAFETY_MONITOR_DIR` 设置监测数据目录。

## weekly-send.py

总结阶段的新鲜度检查脚本。只有采集状态存在且不超过8小时时，才输出 `latest_report.md`。

```bash
python weekly-send.py
```

宿主Agent读取其输出，再执行全文/摘要获取、总结、浏览器后备和消息投递。
