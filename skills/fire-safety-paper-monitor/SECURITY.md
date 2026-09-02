# Security Policy

## English (Normative)

## Supported version

The current supported release line is `0.1.x`. Security fixes are applied to the latest release only.

## Do not publish secrets

Never place these values in the repository, a prompt, a report, a screenshot, a GitHub Issue, or a shared ZIP:

- LLM API keys;
- Zotero Web API or Local API write keys;
- passwords;
- browser cookies or profiles;
- institutional login details;
- proxy credentials;
- Telegram bot tokens or chat identifiers.

Use an OS keychain, GitHub Actions Secrets, or another approved secret manager.

## Zotero safety

- Use official Zotero APIs, Connector, or Find Available PDF.
- Never edit `zotero.sqlite` directly.
- Request one authorization per continuous batch and reuse it.
- Treat authorization timeout and attachment failure as task failures.
- Verify that a PDF child attachment exists and opens.

## Publisher access

This project does not bypass paywalls, CAPTCHA, Cloudflare challenges, reCAPTCHA, hCaptcha, or institutional authorization.

Do not add:

- CAPTCHA-solving services;
- stealth/fingerprint spoofing intended to evade bot controls;
- forged cookies or access tokens;
- Sci-Hub or other unauthorized full-text routes;
- credential sharing.

Publisher access must use open-access sources, official APIs, the user's lawful institutional access, or manual resolver links.

## Reporting a vulnerability

Do not open a public Issue containing a credential or private document. Contact the maintainer privately and include:

- affected version;
- reproduction steps with secrets removed;
- expected and actual behavior;
- impact;
- suggested fix, if known.

Rotate any exposed credential before reporting it.

## Pre-release checks

Before publishing a release:

1. scan for absolute user paths and credentials;
2. compile the Python scripts;
3. run the collector in an isolated temporary directory;
4. verify the Excel template contains no personal data;
5. inspect screenshots for private library or chat content;
6. test the release ZIP;
7. verify the CAPTCHA and paywall boundary remains documented.

---

## Chinese Translation (Reference Only)

The following Chinese text is provided only as a translation to help Chinese-speaking readers. The English section above is the normative version.

## 支持版本

当前支持 `0.1.x`，安全修复仅应用到最新版本。

## 不得公开密钥

以下信息不得写入仓库、提示词、报告、截图、GitHub Issue或分享ZIP：

- 大模型API Key；
- Zotero Web API或Local API写入密钥；
- 密码；
- 浏览器Cookie或个人配置；
- 机构登录信息；
- 代理凭据；
- Telegram Bot Token或聊天标识。

使用系统钥匙串、GitHub Actions Secrets或其他Secret Manager。

## Zotero安全

- 使用官方API、Connector或“查找可用PDF”；
- 不直接修改 `zotero.sqlite`；
- 一个连续批次只请求一次授权并复用；
- 授权超时和附件失败必须使任务失败；
- 验证PDF子附件真实存在并可以打开。

## 出版社访问

项目不绕过付费墙、CAPTCHA、Cloudflare、Turnstile、reCAPTCHA、hCaptcha或机构授权。

禁止增加：

- 验证码代解服务；
- 用于规避机器人检查的指纹伪造；
- 伪造Cookie或令牌；
- Sci-Hub等未经授权的全文来源；
- 凭据共享。

出版社访问只能使用开放来源、官方API、用户自己的合法机构权限或人工resolver链接。

## 报告安全问题

不要在公开Issue中提交密钥或私人文档。通过私密方式联系维护者，并提供：

- 受影响版本；
- 已清除密钥的复现步骤；
- 预期与实际行为；
- 影响；
- 可能的修复建议。

暴露的凭据应先轮换再报告。

## 发布前检查

1. 扫描个人绝对路径和密钥；
2. 编译Python脚本；
3. 在临时目录干运行；
4. 检查Excel模板不含个人数据；
5. 检查截图不含私人聊天或文库；
6. 测试Release ZIP；
7. 确认验证码和付费墙边界仍写入文档。
