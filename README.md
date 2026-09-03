# FireSafety Skills

## English (Normative)

This repository publishes reusable academic research skills for fire-safety literature monitoring and related workflows.

## fire-safety-paper-monitor

`fire-safety-paper-monitor` is a weekly literature-monitoring skill for fire safety, structural fire engineering, and high-temperature materials research. It currently tracks 79 civil-engineering, fire-safety, and multidisciplinary journals, including *Nature*, *Science*, *Nature Communications*, PNAS, and *Communications Engineering*.

The workflow:

- collects new records from official RSS/Atom feeds, publisher pages, and ISSN-scoped Crossref fallbacks;
- filters paper titles for `fire`, `high temperature`, `high-temperature`, `elevated temperature`, or `elevated-temperature`;
- deduplicates records by DOI, canonical URL, and normalized title;
- writes evidence-bounded Chinese summaries when verified full text or a reliable abstract is available;
- delivers a clean weekly digest through Telegram;
- organizes verified papers under dated Zotero collections in `Hermes Weekly: Fire`;
- never bypasses paywalls, logins, CAPTCHA, or other access controls.

- [View the skill](skills/fire-safety-paper-monitor/)
- [Read the full documentation](skills/fire-safety-paper-monitor/README.md)
- [Download the latest release](https://github.com/zhiliu90/FireSafety/releases/latest)

The repository is publicly viewable and downloadable. No license is granted unless a license file or explicit permission states otherwise.

---

## Chinese Translation (Reference Only)

> 以下中文内容仅用于帮助中文用户理解。英文部分是规范性主版本；如有差异，以英文部分为准。

本仓库用于发布火灾安全论文监测及相关学术研究流程的可复用Skills。

### fire-safety-paper-monitor

`fire-safety-paper-monitor` 是一个面向火灾安全、结构抗火和材料高温性能研究的每周论文监测Skill。目前跟踪79种土木工程、火灾安全和综合性期刊，包括 *Nature*、*Science*、*Nature Communications*、PNAS和*Communications Engineering*。

它可以：

- 通过官方RSS/Atom、出版社页面和ISSN限定Crossref检索新增论文；
- 按题名关键词筛选并通过DOI、规范化链接和题名去重；
- 在取得已验证全文或可靠摘要时生成中文总结；
- 通过Telegram发送简洁周报；
- 在Zotero的`Hermes Weekly: Fire`分类下按日期整理已验证论文；
- 遇到付费墙、登录或验证码时停止，不绕过访问控制。

- [查看Skill](skills/fire-safety-paper-monitor/)
- [阅读完整说明](skills/fire-safety-paper-monitor/README.md)
- [下载最新版本](https://github.com/zhiliu90/FireSafety/releases/latest)

本仓库允许公开查看和下载。除非许可证文件或明确授权另有说明，否则不授予进一步使用许可。
