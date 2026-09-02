# Deployment Guide

## English (Normative)

This guide helps another agent reproduce the weekly workflow. The package contains no API keys, passwords, cookies, Zotero grants, or personal account data.

## Files

- `templates/journal-rss-table.xlsx`: 74 starter journals and known RSS URLs;
- `templates/bot-prompt.md`: English and Chinese prompts in one file;
- `scripts/weekly-scan.py`: RSS/publisher/Crossref collection and snapshots;
- `scripts/weekly-send.py`: freshness gate for the summary stage;
- reference documents for system, Zotero, browser, and installation requirements.

## Environment

- Python 3.9+;
- network access to RSS, Springer, Crossref, OpenAlex, and DOI resolvers;
- optional PyMuPDF for PDF extraction;
- optional isolated-browser support;
- Zotero 10+ for automated archiving.

See `system-requirements.md` for validated versions and platform support levels.

## Working directory

```text
<WORKDIR>/fire_safety_paper_monitor/
├── journal_rss_table.xlsx
├── state.json
├── latest_report.md
├── latest_report_with_summaries.md
├── reports/
├── snapshots/
├── pdfs/YYYY-MM-DD/
└── browser_retrieval_YYYY-MM-DD.md
```

Set `FIRE_SAFETY_MONITOR_DIR` to this directory. Never copy another user's absolute path.

## Schedule

Use `Asia/Shanghai`:

```text
collector: 0 13 * * 1
summary:   0 14 * * 1
```

The summary stage rejects missing or older-than-eight-hours collector results.

## Journal workbook

The first row is:

```text
Journal name | RSS
```

Use official RSS URLs. Leave the RSS cell blank when no reliable feed exists. Do not put HTML journal pages in the RSS column.

`Fire Technology` uses the Springer articles page and Crossref online ISSN `1572-8099`. `Fire and Materials` uses the Wiley RSS feed and ISSN `1099-1018`. `Journal of Structural Fire Engineering` and `International Journal of Wildland Fire` use ISSN-scoped Crossref fallbacks (`2040-2325` and `1448-5516`).

## Direct institutional access

On macOS, inspect both OS and process proxy settings:

```bash
scutil --proxy
networksetup -getwebproxy "Wi-Fi"
networksetup -getsecurewebproxy "Wi-Fi"
networksetup -getsocksfirewallproxy "Wi-Fi"
```

Other platforms require equivalent checks. Never change global proxy settings without explicit permission.

A PDF must have a successful final response, `application/pdf` MIME, and `%PDF` signature. Do not save login, CAPTCHA, or payment HTML as PDF.

## Browser fallback

Use an isolated browser only after API and direct routes fail. Stop at Cloudflare, Turnstile, reCAPTCHA, hCaptcha, login, payment, or account permissions. Do not bypass them. Save one audit result per unresolved paper.

## Zotero

Enable local application communication in Zotero 10+. Verify `http://127.0.0.1:23119/api/` is reachable. Read `Zotero-Server-ID`, request one write grant per batch, and reuse it. Store persistent credentials only in a keychain or secret manager.

Use the parent collection `Hermes Weekly: Fire` and a `YYYY-MM-DD` child. Under this user's strict semantics, only items with verified PDF child attachments enter the dated child. A metadata-only URL item is not complete.

## Telegram format

```text
**[1] Journal name**
Paper title [链接](real URL)
Authors
Summary only when available
```

Do not show scheduler metadata, a statistics paragraph, field labels, item dates, indentation, naked URLs, or unavailable-summary placeholders. Keep the title plain and its link on the same line.

## Verification

Before scheduling:

- dry-run the collector;
- inspect source counts and sample titles;
- run one updating collector;
- run the summary stage within eight hours;
- verify duplicate count;
- verify PDF signatures and page extraction;
- verify browser audit count;
- verify Zotero PDF children and sampled open behavior;
- verify Telegram formatting;
- scan the package for secrets and personal paths.

## Known limits

- Publisher RSS can omit reliable dates;
- Crossref created dates are metadata events;
- ScienceDirect/ASCE/Wiley may block automated browsers;
- Zotero write authorization can time out;
- PDF upload behavior can vary by Zotero build;
- only `Fire Technology` has a dedicated publisher-listing parser; profile-only journals skip that parser and use ISSN-scoped Crossref without generating a false listing error.

---

## Chinese Translation (Reference Only)

The following Chinese text is provided only as a translation to help Chinese-speaking readers. The English section above is the normative version.

本包用于让另一台机器或另一个具备工具调用能力的 Bot 复现当前的每周论文检索流程。包内不包含任何 API Key、密码、Cookie、Zotero 写入密钥或个人账号信息。

## 1. 包内文件

- `journal_rss_table.xlsx`：期刊名称与官方 RSS 地址。当前包含74种期刊，其中部分期刊没有RSS，需要出版社页面或Crossref后备。
- `templates/bot-prompt.md`：同一文件先提供英文主版本，再提供中文翻译。
- `scripts/weekly-scan.py`：RSS、Springer页面、Crossref、快照差异、标题筛选及报告生成脚本。
- `scripts/weekly-send.py`：检查13点结果是否存在且未过期，并把原始报告交给后续总结阶段。

## 2. 环境要求

- Python 3.9 或更新版本；核心检索脚本仅使用标准库。
- 可访问 RSS、Springer、Crossref 和 OpenAlex 的网络环境。
- 如果需要 PDF 全文解析，建议安装 PyMuPDF；macOS 也可使用 PDFKit。
- 如果需要浏览器后备，Bot 必须具备隔离浏览器或桌面浏览器控制能力。
- 如果需要 Zotero 归档，安装并运行 Zotero 10 或更新版本。

## 3. 工作目录

在目标机器创建独立目录，例如：

```text
<WORKDIR>/fire_safety_paper_monitor/
├── journal_rss_table.xlsx
├── state.json
├── latest_report.md
├── latest_report_with_summaries.md
├── reports/
├── snapshots/
├── pdfs/
│   └── YYYY-MM-DD/
└── browser_retrieval_YYYY-MM-DD.md
```

把脚本中的 `HERMES_HOME` 或工作目录变量设置为目标机器自己的路径，不要照搬其他用户的绝对路径。

## 4. 定时调度

时区统一设为 `Asia/Shanghai`。

- 每周一 13:00：运行检索脚本。
- 每周一 14:00：读取 13 点报告，获取全文/摘要并生成最终周报。

Cron 表达式：

```text
0 13 * * 1
0 14 * * 1
```

14 点任务必须检查 13 点结果时间，结果缺失或超过 8 小时则报告失败，不得使用旧报告。

## 5. Excel 清单维护

工作表第一行为表头：

```text
Journal name | RSS
```

- 有官方 RSS：填入 RSS 地址。
- 没有可靠 RSS：RSS 单元格留空。
- 不要把普通 HTML 期刊主页填入 RSS 列。
- 新增期刊后先单独测试 RSS 是否能解析出真实条目。

`Fire Technology` 的RSS留空，主来源为Springer官方文章列表：

```text
https://link.springer.com/journal/10694/articles
```

其Crossref后备使用在线ISSN `1572-8099`。

`Fire and Materials` 使用Wiley官方RSS：

```text
https://onlinelibrary.wiley.com/feed/10991018/most-recent
```

`Journal of Structural Fire Engineering` 和 `International Journal of Wildland Fire` 的RSS留空，分别使用在线ISSN `2040-2325`、`1448-5516`进行Crossref后备检索。

## 6. 校园网与代理

用户要求出版社访问使用校园网直连，不通过 VPN 或代理。

macOS 检查命令：

```bash
scutil --proxy
networksetup -getwebproxy "Wi-Fi"
networksetup -getsecurewebproxy "Wi-Fi"
networksetup -getsocksfirewallproxy "Wi-Fi"
```

Bot 发起下载时还应清除当前进程中的代理变量，并显式绕过代理。不要仅凭环境变量为空就假定系统代理已关闭；也不要未经用户同意修改全局网络设置。

PDF 获取必须同时满足：

- 最终 HTTP 请求成功；
- MIME 类型为 `application/pdf`；
- 文件头为 `%PDF`；
- 不是登录页、验证码页或付费页。

## 7. 浏览器后备

API、RSS、Crossref、OpenAlex 和直接 PDF 均失败后，使用隔离浏览器打开出版社页面。

- 不接管用户的个人浏览器配置。
- 可以利用校园 IP 机构权限。
- 遇到 CAPTCHA、登录、支付或账户权限时停止。
- 不自动完成或绕过人机验证。
- 每篇记录最终 URL 和结果：可见摘要、可用 PDF、无摘要、验证码阻塞、登录阻塞或访问失败。

## 8. Zotero 设置

在 Zotero 中启用本机应用通信/Local API。不同版本的设置文字可能略有差异，通常位于：

```text
Zotero → 设置 → 高级 → 允许本机其他应用与 Zotero 通信
```

验证地址：

```text
http://127.0.0.1:23119/api/
```

能够返回 HTTP 200 只说明 Local API 已启用；写入还需要 Zotero 授权。

### 授权流程

1. 读取 Local API 根响应中的 `Zotero-Server-ID`。
2. 使用固定的应用名称请求 `/local/authorize`。
3. 用户在 Zotero 中确认授权。
4. 一个连续批次内复用同一授权，不要逐条重新申请。
5. 若需要无人值守运行，只能把写入密钥存入操作系统钥匙串或安全的 Secret Manager；不要写入提示词、聊天记录、脚本源码或公开配置。
6. 如果 Bot 不持久保存授权，新进程或新日期批次可能再次请求授权。

不要直接修改 Zotero SQLite 数据库。

## 9. Zotero 分类与 PDF 附件

顶层分类固定为：

```text
Hermes Weekly: Fire
```

每次任务创建：

```text
YYYY-MM-DD
```

当前用户要求：

- Zotero 日期分类中的论文应有真实 PDF 子附件；
- 双击应打开 PDF，不应打开出版社网页；
- 只有 URL、没有 PDF 的元数据条目不算完成；
- 无 PDF 的论文仍保留在 Telegram 周报，但不应作为“已成功下载的 Zotero 论文”处理；
- 优先使用 Zotero Connector、Zotero 的“查找可用 PDF”或官方附件接口；
- PDF 必须显示为对应文献条目的子附件，并实际打开验证；
- 不能把 Hermes 目录中的独立 PDF 冒充 Zotero 附件。

PDF 文件名：

```text
期刊 - 论文标题 - 通讯作者.pdf
```

通讯作者依据首页信封符号、Correspondence 标记或对应邮箱确认；不可按作者顺序猜测。上级文件夹已有日期，文件名不重复日期。

## 10. Telegram 输出

每篇论文使用：

```text
**[1] 期刊名称**
论文题名 [链接](真实URL)
作者
有全文或摘要时直接写总结正文
```

- 不显示Cron任务元信息或统计段落。
- 编号与期刊名称放在同一行，整行加粗。
- 论文题名使用普通文本；链接紧随题名且不换行。
- 不显示“期刊、题名、作者、链接、总结、条目日期”等字段标题。
- 没有全文和摘要时，作者行即为该项目最后一行。
- Telegram 只显示“链接”两个字，不裸露 URL。
- 项目内部不缩进，每项之间空一行。

## 11. 验证清单

每次运行结束前检查：

- RSS/出版社/Crossref 各来源是否真实返回记录；
- DOI和题名重复数是否为零；
- 日期窗口和快照差异条目是否正确；
- PDF 数量、PDF 文件头和全文解析覆盖；
- Zotero 日期分类及 PDF 子附件数量；
- Zotero 中随机双击一篇是否打开 PDF；
- Telegram 裸露 URL 数量是否为零；
- “条目日期”字段数量是否为零；
- 无摘要论文是否没有占位总结；
- 链接是否均位于每项最后一行。

## 12. 已知限制

- ScienceDirect/ASCE 可能出现 Cloudflare 或 CAPTCHA；Bot 不得绕过。
- 校园网订阅不代表所有期刊都能下载。
- Crossref 的 created 日期不是正式出版日期。
- Local API 授权超时会导致 Zotero 分类缺失；必须将其作为任务失败，而非静默成功。
- Zotero 的 Local API 附件上传在部分版本中可能失败；需要改用 Connector、“查找可用 PDF”或经验证的官方附件流程。
