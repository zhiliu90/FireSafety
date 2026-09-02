# Fire Safety Paper Monitor

## English (Normative)

A weekly literature-monitoring skill for fire safety, structural engineering, and high-temperature materials research.

All filenames use English. Each user-facing document presents the complete English version first; a Chinese translation appears later in the same file only to help Chinese-speaking readers. The English section is authoritative.

It reads a customizable journal workbook, collects RSS and publisher updates, uses Crossref fallbacks, filters new titles, retrieves lawful full text or abstracts, writes Chinese digests, and archives verified PDFs in Zotero.

## Features

- Mixed journal RSS/Atom monitoring;
- Publisher-page and Crossref fallback for journals without RSS;
- DOI, URL, and title deduplication;
- Idempotent `first_seen` / `first_reported` snapshots;
- Direct institutional-access and PDF validation;
- Publisher, Crossref, and OpenAlex abstract fallback;
- Isolated-browser auditing;
- Full-text or abstract-based Chinese summaries;
- Telegram delivery;
- PDF-backed dated Zotero collections.

## Requirements

- Python 3.9+;
- Zotero 10+ for the bundled automated Local API archiving workflow;
- Earlier Zotero versions are untested and may not support the same authorization, collection, or attachment behavior;
- The monitoring and digest stages can run without Zotero;
- An agent that supports SKILL.md, files, terminal commands, scheduling, and optionally an isolated browser;
- PyMuPDF is recommended for PDF extraction.

### Validated full environment

- macOS 26.5.2, build 25F84, Apple Silicon;
- Hermes Agent 0.20.4 with Python 3.11.15;
- system Python 3.9.6;
- Zotero 10.0;
- Google Chrome 152.0.7977.65;
- cua-driver 0.20.0.

The core collector is designed for macOS, Windows 10/11, and Linux with Python 3.9+. Full browser, proxy, and Zotero attachment automation has only been validated end to end on the documented macOS stack. Windows and Linux require target-machine verification.

See `references/system-requirements.md`.

## Quick start

1. Install this directory as an agent skill.
2. Read `SKILL.md`.
3. Copy `templates/journal-rss-table.xlsx` to the monitor directory as `journal_rss_table.xlsx`.
4. Set `FIRE_SAFETY_MONITOR_DIR`.
5. Run a dry test:

```bash
python scripts/weekly-scan.py --no-update --debug
```

6. After verification, schedule the collector for Monday 13:00 and the summary stage for Monday 14:00 in `Asia/Shanghai`.

See the English sections of `references/installation.md` and `references/setup-guide.md`; the Chinese sections are in the same files.

## Zotero

Automated archiving requires Zotero 10+ with local application communication enabled and an approved write grant. A completed archive item must have a real PDF child attachment that opens from Zotero. A URL-only metadata item is not a completed PDF archive.

See `references/zotero-workflow.md`.

## CAPTCHA and bot challenges

This skill cannot and will not bypass publisher bot challenges, including Cloudflare Challenge/Turnstile, reCAPTCHA, hCaptcha, or publisher-specific verification pages from ScienceDirect, ASCE, Wiley, and other sites.

When a challenge appears, the workflow records a blocked status. It does not automate CAPTCHA solving, spoof verification cookies, use CAPTCHA-solving services, or evade access controls. A user may complete a challenge in a lawful browser session and rerun the task.

See `references/browser-retrieval.md`.

## Telegram format

```text
**[1] Journal name**
Paper title [链接](real URL)
Authors
Summary when available
```

Do not prepend summary counts or scheduler metadata. The title is plain text, and its link remains on the same line. An unavailable paper has no placeholder summary.

Example: `assets/telegram-example.png`.

## Journal customization

`templates/journal-rss-table.xlsx` is a starter template, not a fixed catalog. Add or remove journals as needed. Use official RSS URLs; leave the RSS cell blank when no reliable feed exists.

## Security

Do not store API keys, passwords, Zotero grants, cookies, or institutional credentials in prompts, scripts, commits, or issues. Do not modify Zotero SQLite directly. Do not bypass paywalls or bot challenges.

See `SECURITY.md`.

## Publishing

Use GitHub as the source of truth, ClawHub for discovery, and an optional Gitee mirror for readers in China.

```bash
hermes skills publish <skill-directory> --to github --repo owner/repository
hermes skills publish <skill-directory> --to clawhub
```

---

## Chinese Translation (Reference Only)

The following Chinese text is provided only as a translation to help Chinese-speaking readers. The English section above is the normative version.

一个面向火灾安全、结构工程和高温材料研究的每周论文监测 Skill。

包内所有文件名均使用英文。每份面向用户的文档先提供完整英文主版本，再在同一文件后部提供中文翻译，帮助中文用户理解；英文部分是规范性版本。

它可以读取自定义期刊 Excel 清单，抓取 RSS、出版社最新论文页面和 Crossref，按题名筛选新增论文，尝试从合法来源取得全文或摘要，生成中文周报，并把已验证 PDF 归档到 Zotero。

## 主要功能

- 混合期刊 RSS 监测；
- 无 RSS 期刊的出版社页面和 Crossref 后备；
- DOI、链接和题名去重；
- `first_seen` / `first_reported` 快照，保证重复运行稳定；
- 校园网直连及 PDF 真实性验证；
- 出版社、Crossref、OpenAlex 摘要后备；
- 隔离浏览器逐篇核验；
- 中文全文/摘要总结；
- Telegram 周报；
- PDF 支持的 Zotero 日期分类。

## 版本要求

- Python 3.9 或更新版本；
- Zotero 10 或更新版本，适用于本 Skill 的自动 Local API 归档流程；
- 更早的 Zotero 版本未经过验证，不保证分类、授权和附件写入兼容；
- 不使用 Zotero 时，论文检索和周报功能仍可独立运行；
- 需要一个支持 SKILL.md、文件、终端、定时任务和可选隔离浏览器的 Agent；
- 全文解析推荐安装 PyMuPDF。

### 已验证的完整环境

- macOS 26.5.2（Build 25F84，Apple Silicon）；
- Hermes Agent 0.20.4（运行时 Python 3.11.15）；
- 系统 Python 3.9.6；
- Zotero 10.0；
- Google Chrome 152.0.7977.65；
- cua-driver 0.20.0。

核心检索脚本按设计支持 macOS、Windows 10/11 和安装 Python 3.9+ 的 Linux。完整的浏览器控制、系统代理检查和 Zotero 附件流程目前只在上述 macOS 环境完成端到端验证；Windows 和 Linux 需要在目标机器重新测试。

完整矩阵见 `references/system-requirements.md`。

## 快速开始

1. 把本目录安装到 Agent 的 Skill 目录；
2. 读取 `SKILL.md`；
3. 把 `templates/journal-rss-table.xlsx` 复制到工作目录并改名为 `journal_rss_table.xlsx`；
4. 设置 `FIRE_SAFETY_MONITOR_DIR`；
5. 先运行：

```bash
python scripts/weekly-scan.py --no-update --debug
```

6. 测试通过后，创建每周一 13:00 检索和 14:00 总结任务。

完整步骤见 `references/installation.md` 和 `references/setup-guide.md` 的中文部分；英文部分也在同一文件中。

## Zotero要求

自动归档需要：

- Zotero 10+ 正在运行；
- 开启本机应用通信/Local API；
- 用户完成写入授权；
- Bot 在一个批次内复用授权；
- PDF 必须成为母文献下的真实子附件；
- 双击应打开 PDF，而不是出版社网页。

只有网页 URL、没有 PDF 的元数据条目不算归档完成。详情见 `references/zotero-workflow.md`。

## 人机验证限制

本 Skill **不能也不会跳过出版社的人机验证**，包括但不限于：

- Cloudflare Challenge / Turnstile；
- reCAPTCHA；
- hCaptcha；
- ScienceDirect、ASCE、Wiley 或其他出版社的机器人验证页面。

遇到验证时，任务会标记为“CAPTCHA/验证阻塞”，不会自动点击、伪造 Cookie、调用验证码代解服务或规避访问控制。用户可以在合法浏览器会话中自行完成验证，再重新运行。详情见 `references/browser-retrieval.md`。

## Telegram输出

```text
**[1] Journal name**
Paper title [链接](real URL)
Authors
Summary when available
```

不显示统计段落和Cron任务元信息。编号与期刊名称同一行并加粗；题名不加粗，链接紧随题名且不换行；没有全文或摘要时完全省略总结。

示例图：`assets/telegram-example.png`。

## 自定义期刊

`templates/journal-rss-table.xlsx` 只是模板。用户可以增加、删除或替换期刊：

- 有官方 RSS 时填写 RSS；
- 没有 RSS 时留空，并在脚本或配置中增加出版社/Crossref后备；
- 不要把普通 HTML 主页写进 RSS 列。

## 安全

- 不要在提示词、脚本、Git提交或Issue中保存 API Key、密码、Zotero密钥、Cookie和机构账号；
- 不直接修改 Zotero SQLite；
- 不绕过付费墙和人机验证；
- 发布前运行密钥扫描和文件完整性检查。

详见 `SECURITY.md`。

## 发布

可通过 GitHub 维护源码和 Release，通过 ClawHub发布技能目录，并为国内用户提供Gitee镜像。

```bash
hermes skills publish <skill目录> --to github --repo 用户名/仓库名
hermes skills publish <skill目录> --to clawhub
```
