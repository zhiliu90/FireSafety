---
name: fire-safety-paper-monitor
description: Build and run weekly fire-safety paper monitoring.
version: 0.1.1
author: Zhi Liu, Hermes Agent
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Research, RSS, Fire-Safety, Zotero, Monitoring]
    related_skills: []
---

# English (Normative)

# Fire-Safety Paper Monitor

Build and operate a two-stage weekly monitor for fire-safety and high-temperature papers. The skill covers mixed journal RSS, publisher fallbacks, idempotent snapshots, lawful full-text retrieval, Chinese summaries, Telegram delivery, and PDF-backed Zotero archiving.

Use English filenames throughout the package. In every user-facing document, place the complete English normative content first and a Chinese reference translation later in that same file. Do not create parallel English and Chinese documents.

## When to Use

Use this skill when the user asks to:

- monitor named civil, structural, or fire-safety journals on a schedule;
- filter new papers by title keywords;
- create a weekly Chinese digest with summaries only when evidence exists;
- download papers through the user's legitimate institutional access;
- archive verified PDFs in dated Zotero collections;
- reproduce or share this workflow with another agent.

Do not use it for a one-off review of a known paper, broad web news monitoring, or any workflow that requires bypassing paywalls, CAPTCHA, or institutional access controls.

## Prerequisites

- Python 3.9+; the collector uses only the standard library and has been validated with Python 3.9.6 and 3.11.15.
- A writable monitor directory and the supplied `journal-rss-table.xlsx` template.
- Network access to RSS, publisher pages, Crossref, and optional OpenAlex.
- An LLM-capable second-stage agent for summaries.
- Zotero is optional for monitoring, but the bundled automated Local API archive workflow requires Zotero 10 or newer. Earlier versions are untested and unsupported by this skill.
- Optional: an isolated browser tool for publisher-page fallback.
- Optional: PyMuPDF or a platform PDF text extractor for full-text reading.

Never place API keys, Zotero write keys, passwords, cookies, or institutional credentials in prompts, scripts, reports, or the shared skill package. Use the host's secret store or OS keychain.

Read `references/system-requirements.md` before deployment. Full end-to-end automation is validated on the documented macOS stack; Windows and Linux support is limited to the levels stated there.

## Bundled Files

- `templates/journal-rss-table.xlsx` — starter list of 74 journals with English machine-readable headers and known RSS URLs.
- `templates/bot-prompt.md` — one file with English and Chinese task-prompt sections.
- `scripts/weekly-scan.py` — deterministic RSS/publisher/Crossref collector.
- `scripts/weekly-send.py` — freshness gate for the summary stage.
- `scripts/README.md` — bilingual script instructions.
- `references/system-requirements.md` — bilingual OS/software matrix.
- `references/installation.md` — bilingual install/release guide.
- `references/setup-guide.md` — bilingual deployment guide.
- `references/zotero-workflow.md` — bilingual Zotero rules.
- `references/browser-retrieval.md` — bilingual browser/CAPTCHA rules.
- `assets/telegram-example.png` — privacy-safe Telegram digest illustration.
- `README.md` — bilingual public overview.
- `SKILL.md` — English loader section and Chinese operator section in one file.
- `CHANGELOG.md` and `SECURITY.md` — bilingual release and security guidance.

Load a linked file with `skill_view(name='fire-safety-paper-monitor', file_path='...')` before changing its procedure.

## Canonical Schedule

Use timezone `Asia/Shanghai`.

- Collector: Monday 13:00, cron `0 13 * * 1`.
- Summary delivery: Monday 14:00, cron `0 14 * * 1`.

The 14:00 stage must reject a missing or older-than-eight-hours collector report. A failed Zotero sync must make the 13:00 stage fail instead of silently reporting success.

## Quick Reference

- Dry run: `weekly-scan.py --no-update --debug`.
- Updating run: `weekly-scan.py`.
- Summary input check: `weekly-send.py`.
- Main report: `latest_report.md`.
- Enriched report: `latest_report_with_summaries.md`.
- State: `state.json`.
- Snapshots: `snapshots/` and `snapshot_latest.xlsx`.
- PDF fallback: `pdfs/YYYY-MM-DD/`.
- Browser audit: `browser_retrieval_YYYY-MM-DD.md`.
- Zotero parent: `Hermes Weekly: Fire`.
- Zotero child: execution date `YYYY-MM-DD`.

## Procedure

### 1. Prepare the working directory

Copy `templates/journal-rss-table.xlsx` into the monitor directory as `journal_rss_table.xlsx`. Copy the two bundled scripts into an executable scripts directory, or run them from the skill directory. Set `FIRE_SAFETY_MONITOR_DIR` to the chosen monitor directory.

Completion criterion: the collector reports the workbook path and the expected journal count without a missing-file error.

### 2. Validate the journal sources

Read the workbook before running. Preserve journal names exactly. Keep the RSS cell blank when no reliable RSS exists; do not put an HTML journal page in the RSS column.

Source priority:

1. official RSS/Atom;
2. publisher latest-articles page;
3. ISSN-scoped Crossref fallback;
4. OpenAlex only for metadata or abstract enrichment.

`Fire Technology` uses the Springer articles page plus online ISSN `1572-8099`. `Fire and Materials` uses its official Wiley RSS and online ISSN `1099-1018`. `Journal of Structural Fire Engineering` and `International Journal of Wildland Fire` use ISSN-scoped Crossref fallbacks (`2040-2325` and `1448-5516`) because no reliable publisher RSS was verified.

Completion criterion: every configured source is classified as RSS, publisher fallback, or metadata fallback; none is silently dropped.

### 3. Apply the exact title filter

The default case-insensitive title rule is:

- `fire`;
- `high temperature` or `high-temperature`;
- `elevated temperature` or `elevated-temperature`.

Do not broaden filtering to abstracts or journal scope unless the user changes the rule.

Completion criterion: each reported title matches the configured title expression.

### 4. Make reruns idempotent

Use a reliable item-level date when present. For undated sources, compare canonical DOI, URL, or title keys with the persisted snapshot. The first run creates a baseline instead of reporting all history.

Persist `first_seen` separately from `first_reported`. An undated item that entered a weekly report remains visible on deterministic reruns during the same seven-day window. Never infer reportability from recent `first_seen` alone.

Completion criterion: two consecutive reruns produce the same report, with no duplicate titles or lost snapshot-diff items.

### 5. Retrieve lawful full text

Use direct institutional access only when the user requests it. Inspect both process proxy variables and OS proxy settings. Do not modify global proxy settings without explicit permission.

A PDF is accepted only when:

- the final HTTP status succeeds;
- MIME is `application/pdf`;
- the file begins with `%PDF`;
- the response is not a login, payment, or CAPTCHA page.

Try official publisher HTML/XML, open-access locations, and validated PDF fallbacks. Record abstract-only and metadata-only outcomes explicitly in internal state.

Completion criterion: every claimed full-text item has a verified PDF or complete publisher text; all failures carry a reason.

### 6. Use browser fallback

When API and direct requests do not provide full text or an abstract, use an isolated browser and open each publisher page. Do not attach to the user's personal browser unless the user explicitly authorizes that risk.

If a page presents login, payment, CAPTCHA, or account permission, stop. Never solve or bypass the challenge. Record final URL and one outcome: abstract visible, PDF available, no abstract, login/CAPTCHA blocked, or access failed.

Completion criterion: if unresolved items remain, the browser audit contains one row per unresolved item; if browser tooling was unavailable, the job reports that as failure rather than claiming a complete search.

### 7. Generate evidence-bounded summaries

Use sources in this order:

1. verified PDF full text;
2. publisher full text;
3. publisher abstract;
4. Crossref abstract;
5. OpenAlex abstract.

Summaries must not exceed 500 Chinese characters and should cover purpose, methods, key results, conclusion, and explicit limitations when the source supports them. If only an abstract is available, label the actual source. If neither abstract nor full text is available, omit the summary line entirely.

Completion criterion: every summary maps to a recorded source; unavailable items contain no inferred or placeholder summary.

### 8. Archive in Zotero

Follow `references/zotero-workflow.md`. Do not modify Zotero SQLite directly. Request authorization once per continuous batch and reuse it.

The user's preferred completion semantics are strict:

- a Zotero item counts as archived only when it has a real PDF child attachment;
- double-clicking should open the PDF, not a publisher webpage;
- metadata-only URL items remain in the Telegram report but do not count as completed PDF archive entries;
- file names use `Journal - Article title - Corresponding author.pdf` without a date;
- identify the corresponding author from an envelope/correspondence marker or email, never author order.

Completion criterion: the dated collection contains only items with verified PDF children, duplicate titles are zero, and a sampled attachment opens.

### 9. Format the Telegram digest

Do not prepend a statistics paragraph. The scheduler delivery must also be unwrapped: no `Cronjob Response`, job ID, separator, or task-management footer.

For each paper:

```text
**[1] Journal name**
Paper title [链接](real URL)
Authors
Summary text only when available
```

The sequence number and journal share one bold line. The paper title is plain text. Its Markdown link follows the title on the same line. Authors are plain text on the next line; an evidence-backed summary follows when available. Do not show field labels, item dates, naked URLs, left indentation, JSON, API payloads, temporary paths, or unavailable-summary placeholders.

Completion criterion: scheduler-wrapper count, statistics-paragraph count, naked URL count, item-date label count, indentation count, bold-title count, and unavailable placeholder-summary count are all zero; every item has one bold number-plus-journal line and one title-plus-link line.

### 10. Schedule and test

Run a dry collector first. Inspect source counts, candidate titles, duplicates, and failure states. Run one updating collector and then the summary stage. Only after both pass should `cronjob` create the recurring 13:00 and 14:00 jobs.

Make each cron prompt self-contained because scheduled runs have no current-chat context. Attach `scholarly-literature-monitoring` and document/PDF extraction skills when available. Give the summary stage network, file, terminal, and isolated-browser tools.

Completion criterion: both jobs are enabled, recurring forever, use `Asia/Shanghai`, and a manual run produces the expected local artifacts and Telegram format.

## Pitfalls

- A blank web-search backend can produce a plausible "no results" message without any retrieval. Require deterministic collection or a hard failure.
- ScienceDirect, ASCE, Wiley, and other publishers may block isolated browsers with Cloudflare Challenge, Turnstile, reCAPTCHA, hCaptcha, or publisher-specific robot checks. Institutional subscription does not remove these challenges. The skill cannot solve, skip, or bypass them; record a blocked status and require lawful human verification when appropriate.
- Crossref `created` is not a publication date.
- HTML 200 is not proof of PDF access.
- Repeated Local API authorization usually means the client did not reuse its grant; do not hide this as a successful run.
- A standalone local PDF is not a Zotero imported attachment.
- Metadata-only Zotero items may open webpages on double-click; they do not satisfy this user's archive rule.
- Publisher author strings may include affiliations or ORCID text. Never guess corrected authors or corresponding authors.

## Verification

Before reporting success, verify:

- workbook and source counts;
- report window and rerun stability;
- zero duplicate DOI/title keys;
- PDF signatures and parsed page coverage;
- browser audit row count;
- Zotero collection, child attachment, and open behavior;
- enriched report item count;
- Telegram formatting invariants;
- no secrets or personal browser data in shared artifacts.

A failure in retrieval, Zotero write, browser fallback, or report freshness must remain a failure. Never substitute a plausible-looking report for an unexecuted step.

---

# Chinese Translation (Reference Only)

> 以下中文内容仅用于帮助中文用户理解。英文部分是规范性主版本；如果翻译与英文存在差异，以英文部分为准。

包内文件名统一使用英文。每份面向用户的文档在同一文件中先写完整英文主版本，再附中文参考翻译；不得拆分为英文文件和中文文件。

## 适用场景

用于：

- 定期监测土木、结构、高温和火灾安全期刊；
- 按题名关键词筛选新增论文；
- 只有在全文或摘要可核验时生成中文总结；
- 使用用户合法的机构权限下载PDF；
- 把已验证PDF归档到Zotero日期分类；
- 创建可复用、可分享的论文周报定时任务。

不用于已知单篇论文的一次性精读、网络事故新闻监测，也不用于绕过付费墙、验证码或机构权限。

## 前置要求

- Python 3.9+；核心采集脚本只使用标准库；
- 可写且持久的监测目录；
- `journal-rss-table.xlsx`；
- RSS、出版社、Crossref及可选OpenAlex网络访问；
- 能执行总结的大模型Agent；
- Zotero归档可选，但自动Local API流程要求Zotero 10或更新版本；
- 出版社页面后备需要隔离浏览器；
- 全文总结推荐PyMuPDF或其他PDF提取器。

不要把API Key、Zotero写入密钥、密码、Cookie和机构账号写入提示词、脚本、报告或公开压缩包。完整版本矩阵见 `references/system-requirements.md` 的中文部分。

## 包含文件

- `templates/journal-rss-table.xlsx`：74种期刊模板；为保证机器兼容，表头使用英文，中文解释见本翻译部分；
- `templates/bot-prompt.md`：同一文件包含英文和中文提示词；
- `scripts/weekly-scan.py`：确定性采集器；
- `scripts/weekly-send.py`：总结阶段新鲜度检查；
- `scripts/README.md`：同一文件包含英文和中文脚本说明；
- `references/system-requirements.md`：中英双语系统和软件要求；
- `references/installation.md`：中英双语安装和发布；
- `references/setup-guide.md`：中英双语部署指南；
- `references/zotero-workflow.md`：中英双语Zotero规则；
- `references/browser-retrieval.md`：中英双语浏览器和验证码边界；
- `assets/telegram-example.png`：无私人信息的Telegram示例图。

## 标准时间

时区：`Asia/Shanghai`。

- 周一13:00采集：`0 13 * * 1`；
- 周一14:00总结：`0 14 * * 1`。

14点阶段必须拒绝缺失或超过8小时的采集报告。Zotero同步失败必须让13点任务失败。

## 操作流程

### 1. 准备工作目录

把Excel模板复制到监测目录并改名为 `journal_rss_table.xlsx`，设置 `FIRE_SAFETY_MONITOR_DIR`。先执行干运行。

完成标准：脚本报告正确工作簿和期刊数，没有缺失文件错误。

### 2. 检查来源

优先级：

1. 官方RSS/Atom；
2. 出版社最新论文页面；
3. ISSN限定Crossref；
4. OpenAlex仅补充元数据或摘要。

没有可靠RSS时保持Excel单元格为空，不能把HTML主页填入RSS列。`Fire Technology` 使用Springer论文列表和在线ISSN `1572-8099`；`Fire and Materials` 使用Wiley官方RSS及在线ISSN `1099-1018`；`Journal of Structural Fire Engineering` 和 `International Journal of Wildland Fire` 分别使用ISSN `2040-2325`、`1448-5516`进行Crossref后备检索。

完成标准：每个期刊都有RSS、出版社后备或元数据后备分类。

### 3. 题名筛选

默认不区分大小写匹配：

- `fire`；
- `high temperature` / `high-temperature`；
- `elevated temperature` / `elevated-temperature`。

除非用户修改规则，不扩展到摘要和期刊范围。

### 4. 稳定重跑

有可靠文章时间时按时间窗口判断；无时间时使用DOI、URL和题名快照。第一次运行只建立基线。

分别保存 `first_seen` 和 `first_reported`。同一周内重复运行时，已经报告的无日期论文继续保留；不能因为 `first_seen` 较新就把全部基线论文报告出来。

完成标准：连续两次运行报告一致，没有重复题名或丢失条目。

### 5. 合法全文获取

使用用户明确允许的机构访问。分别检查进程代理变量和系统代理；未经允许不修改全局代理。

PDF必须满足：

- 最终HTTP成功；
- MIME为 `application/pdf`；
- 文件头为 `%PDF`；
- 不是登录、付费或验证码HTML。

所有失败必须保留原因。

### 6. 浏览器后备

API和直接访问都无法得到全文或摘要时，使用隔离浏览器逐篇打开。遇到登录、付费、Cloudflare、Turnstile、reCAPTCHA、hCaptcha或其他机器人验证时停止。

Skill不能破解、跳过、代答验证码，不能伪造Cookie或浏览器指纹。记录最终URL和结果。

完成标准：未解决论文数量与浏览器审计行数一致；没有执行浏览器时必须报告失败。

### 7. 总结

来源优先级：

1. 已验证PDF全文；
2. 出版社HTML全文；
3. 出版社摘要；
4. Crossref摘要；
5. OpenAlex摘要。

每篇总结不超过500个中文字，写目的、方法、关键结果、结论和明确局限。只有摘要时标明来源。无全文和摘要时完全省略总结。

### 8. Zotero归档

不直接修改SQLite。一个批次只请求一次授权并复用。

完成含义：

- 文献有真实PDF子附件；
- 双击打开PDF而不是网页；
- 只有URL的元数据不算完成；
- 无PDF论文留在Telegram周报，不作为已归档PDF；
- 文件名为“期刊 - 论文标题 - 通讯作者.pdf”；
- 通讯作者只能根据首页信封、Correspondence或邮箱确认。

完成标准：日期分类只含有验证PDF的论文，重复题名为0，抽样附件可打开。

### 9. Telegram格式

```text
**[1] 期刊名称**
论文题名 [链接](真实URL)
作者
有来源时的总结正文
```

不显示统计段落，也不显示 `Cronjob Response`、job_id、分隔线或任务管理提示。编号与期刊名称放在同一行并整行加粗；论文题名使用普通文本，链接紧随题名并位于同一行。作者单独占下一行，有可靠来源时再写总结。不显示字段标题、条目日期、裸URL、缩进、JSON、临时路径和无内容占位总结。

### 10. 建立定时任务

先执行干采集，检查来源、题名、重复和错误。再正式采集一次并运行总结。两阶段都通过后才建立长期Cron。

定时任务提示词必须自包含。总结阶段需要网络、文件、终端和隔离浏览器工具。

## 常见问题

- Web后端为空时，模型可能在没有检索的情况下声称“无结果”；必须用确定性采集或硬失败。
- ScienceDirect、ASCE、Wiley等可能返回人机验证；机构订阅不能关闭机器人检查。
- Crossref `created` 不是出版日期。
- HTTP 200不代表取得PDF。
- 重复授权通常说明客户端没有复用Zotero授权。
- Hermes目录中的独立PDF不是Zotero附件。
- 只有URL的Zotero条目可能双击打开网页，不满足归档要求。

## 验证

成功前检查：

- 工作簿、期刊和来源数量；
- 日期窗口和重复运行稳定性；
- DOI/题名重复数为0；
- PDF签名和页面覆盖；
- 浏览器审计数量；
- Zotero分类、PDF子附件和打开行为；
- 总结报告条目数；
- Telegram格式；
- 分享包无密钥、个人路径和私人浏览器数据。

检索、Zotero、浏览器或报告新鲜度失败时必须保留失败状态，不能用看似合理的内容代替真实执行。
