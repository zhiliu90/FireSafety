# Browser Retrieval

## English (Normative)

## Trigger

Use browser fallback only after RSS metadata, publisher/API access, open scholarly indexes, and direct PDF routes fail to provide full text or an abstract.

## Browser profile

Use a driver-owned isolated browser. Do not attach to the user's personal profile unless the user explicitly approves exposure of its tabs, cookies, and storage.

## Procedure

1. Create or bind an isolated browser with exact mutation permission.
2. Open the publisher URL or DOI resolver.
3. Record final URL and page title.
4. Check for institution access text, abstract, full HTML, or a PDF control.
5. If a PDF is offered, download through the browser or a verified direct request.
6. Confirm MIME, `%PDF`, and page content before treating it as full text.
7. Save one audit row per item.

Allowed audit outcomes:

- publisher abstract visible;
- publisher full text visible;
- verified PDF downloaded;
- page has no abstract;
- login required;
- CAPTCHA or bot challenge blocked;
- payment or subscription blocked;
- navigation or extraction failed.

## Safety boundary

Never:

- solve or bypass CAPTCHA;
- use a CAPTCHA-solving service;
- fake browser fingerprints or verification cookies;
- enter passwords, payment details, or API keys;
- click login, consent, or account prompts without explicit user instruction;
- treat an institution-access banner as proof the PDF downloaded.

A campus IP grants subscription entitlement only when the publisher recognizes it. It does not disable bot protection.

## ScienceDirect and ASCE

These sites may return usable RSS metadata while isolated browsers receive Cloudflare or CAPTCHA pages. Record that distinction. RSS availability is evidence for title/author/link only, not abstract or full-text availability.

## Springer

Springer journal listing and predictable PDF routes may work without a browser. Prefer direct validated access before browser fallback. A cookie notice is not a CAPTCHA; reject optional cookies in an isolated profile if needed, then continue.

## Completion gate

If unresolved papers exist and browser tooling is required, the browser audit row count must equal the unresolved item count. If no browser action occurred, report `浏览器后备未执行` and do not overwrite a previously valid enriched report.

---

## Chinese Translation (Reference Only)

The following Chinese text is provided only as a translation to help Chinese-speaking readers. The English section above is the normative version.

## 触发条件

仅在RSS元数据、出版社/API、开放学术索引和直接PDF均无法提供全文或摘要后使用浏览器。

## 浏览器配置

使用驱动管理的隔离浏览器。除非用户明确接受暴露标签页、Cookie和存储的风险，否则不接管个人浏览器。

## 流程

1. 创建或精确绑定隔离浏览器；
2. 打开出版社URL或DOI解析页；
3. 记录最终URL和页面标题；
4. 检查机构权限提示、摘要、HTML全文或PDF按钮；
5. 有PDF时通过浏览器或验证后的直接请求下载；
6. 验证MIME、`%PDF`和页面内容；
7. 每篇写入一条审计记录。

允许的结果：

- 出版社摘要可见；
- 出版社全文可见；
- 已下载并验证PDF；
- 页面没有摘要；
- 需要登录；
- CAPTCHA或机器人验证阻塞；
- 付费或订阅阻塞；
- 导航或提取失败。

## 安全边界

禁止：

- 破解、代答或跳过CAPTCHA；
- 使用验证码代解服务；
- 为规避机器人检查伪造浏览器指纹；
- 伪造Cookie或验证令牌；
- 输入密码、付款信息和API Key；
- 未经明确授权点击登录、同意或账户提示；
- 把机构权限横幅当作PDF下载证据。

校园IP只提供出版社认可时的订阅权限，不能关闭机器人验证。

## ScienceDirect和ASCE

这些网站可能允许RSS元数据访问，却在隔离浏览器中返回Cloudflare或CAPTCHA。必须区分：RSS只能证明题名、作者和链接存在，不能证明摘要或全文可得。

## Springer

Springer期刊列表和可预测PDF路径有时无需浏览器即可访问，应先使用直接验证。Cookie提示不是CAPTCHA；可以在隔离配置中拒绝可选Cookie后继续。

## 完成条件

如果仍有未解决论文，浏览器审计行数必须等于未解决数量。若没有执行浏览器操作，任务应报告“浏览器后备未执行”，不得覆盖已有的有效总结报告。
