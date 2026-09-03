# Changelog

## English (Normative)

All notable changes to this skill are documented here.

## [0.1.2] - 2026-09-02

### Added

- `Nature`, `Science`, `Nature Communications`, `Proceedings of the National Academy of Sciences` (PNAS), and `Communications Engineering`;
- verified official RSS feeds for all five journals;
- online ISSN profiles for precise Crossref fallback when a feed fails.

### Changed

- expanded the starter workbook from 74 to 79 journals;
- extended regression coverage to all newly tracked comprehensive journals.

## [0.1.1] - 2026-09-02

### Added

- `Fire and Materials` with its verified Wiley RSS feed and ISSN-scoped fallback;
- `Journal of Structural Fire Engineering` with online ISSN `2040-2325`;
- `International Journal of Wildland Fire` with online ISSN `1448-5516`.

### Changed

- expanded the starter workbook from 71 to 74 journals;
- profile-only ISSN fallbacks now skip the first-party listing parser unless a `listing_url` is configured;
- added regression coverage for the three journals, workbook rows, and listing-profile behavior.

## [0.1.0] - 2026-09-01

### Added

- Weekly two-stage collector and summary workflow;
- Starter workbook with 71 civil, structural, and fire-safety journals;
- RSS, Springer listing, and Crossref collection script;
- Idempotent `first_seen` / `first_reported` snapshot behavior;
- Direct institutional-access and verified-PDF rules;
- Isolated-browser audit and CAPTCHA boundary;
- Evidence-bounded Chinese summaries;
- Telegram digest format with hidden URLs;
- PDF-backed dated Zotero archive semantics;
- bilingual single-file sections for the README, Skill guide, prompt, setup, installation, system, Zotero, browser, script, security, and changelog documents;
- English machine-readable Excel column headers, explained in the Chinese translation;
- exact system/software requirements with a validated macOS stack and Windows/Linux support levels;
- installation, setup, Zotero, browser, and security documentation;
- Telegram example image;
- shareable release ZIP workflow.

### Known limitations

- Zotero Local API write authorization may require user interaction and can time out;
- Local API file upload behavior varies by Zotero build;
- ScienceDirect, ASCE, Wiley, and other publishers may block automation with CAPTCHA;
- the collector includes a dedicated publisher profile only for `Fire Technology`; other no-RSS journals rely primarily on Crossref unless extended;
- publisher RSS author fields may contain affiliations or ORCID text and require conservative handling.

---

## Chinese Translation (Reference Only)

The following Chinese text is provided only as a translation to help Chinese-speaking readers. The English section above is the normative version.

## [0.1.2] - 2026-09-02

### 新增

- `Nature`、`Science`、`Nature Communications`、`Proceedings of the National Academy of Sciences`（PNAS）和`Communications Engineering`；
- 为5种期刊配置并验证官方RSS；
- 为RSS失败情况配置在线ISSN限定的Crossref后备。

### 变更

- Excel模板从74种期刊扩展到79种；
- 回归测试扩展到全部新增综合性期刊。

## [0.1.1] - 2026-09-02

### 新增

- `Fire and Materials`，使用已验证的Wiley RSS和ISSN限定后备；
- `Journal of Structural Fire Engineering`，在线ISSN为 `2040-2325`；
- `International Journal of Wildland Fire`，在线ISSN为 `1448-5516`。

### 变更

- Excel模板从71种期刊扩展到74种；
- 只有配置 `listing_url` 的期刊才调用出版社列表解析器，只有ISSN的后备配置不再产生虚假的列表错误；
- 增加三种期刊、Excel条目及列表配置行为的回归测试。

## [0.1.0] - 2026-09-01

### 新增

- 每周两阶段论文采集和总结流程；
- 包含71种土木、结构和火灾安全期刊的Excel模板；
- RSS、Springer列表和Crossref采集脚本；
- `first_seen` / `first_reported` 稳定快照；
- 校园网直连和真实PDF验证规则；
- 隔离浏览器审计及人机验证边界；
- 有证据来源的中文总结；
- 隐藏完整URL的Telegram格式；
- 仅以PDF子附件为完成标准的Zotero日期归档；
- README、Skill说明、提示词、部署、安装、系统、Zotero、浏览器、脚本、安全和更新记录均在同一文件内分英文和中文章节；
- Excel使用英文机器可读表头，中文解释放在同一文档的翻译部分；
- 已验证macOS环境及Windows/Linux支持层级；
- Telegram示例图片；
- 可分享的Release ZIP流程。

### 已知限制

- Zotero Local API授权可能需要用户操作并可能超时；
- Zotero不同版本的附件上传行为可能不同；
- ScienceDirect、ASCE、Wiley等可能使用人机验证阻塞自动访问；
- 采集器只为 `Fire Technology` 内置专用出版社列表配置；其他无RSS期刊主要依赖Crossref，除非继续扩展；
- RSS作者字段可能混入单位、ORCID或邮箱，必须保守处理。
