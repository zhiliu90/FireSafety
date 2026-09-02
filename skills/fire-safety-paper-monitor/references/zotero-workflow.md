# Zotero Workflow

## English (Normative)

## Goal

A dated weekly archive is complete only when each included bibliographic item has a real PDF child attachment that opens from Zotero. A URL field or webpage attachment is not a PDF archive.

## Collection hierarchy

Use one parent collection:

```text
Hermes Weekly: Fire
```

Create one child per run:

```text
YYYY-MM-DD
```

For this user's preferred behavior, add an item to the dated child only after its PDF attachment is verified. Keep metadata-only papers in the Telegram report rather than populating the Zotero child with items that open publisher webpages.

## Safe write path

1. Use Zotero's official Local API, Web API, Connector, or Find Available PDF feature.
2. Never edit `zotero.sqlite` directly.
3. Read `Zotero-Server-ID` before local authorization.
4. Use a stable application name.
5. Request one grant per continuous batch and reuse it.
6. Keep credentials in an OS keychain or secret store, never prompts or logs.
7. Treat authorization timeout as a failed task.

## Deduplication

Match in this order:

1. normalized DOI;
2. exact normalized title;
3. canonical publisher URL.

Query by title as well as DOI because some Zotero search paths do not match DOI fields reliably. Before creating items, inspect the dated collection and the whole library. After writes, count duplicate titles and remove only newly created duplicates with version-safe API operations.

## Attachment requirements

- Imported PDF child preferred.
- A linked local file is acceptable only when the user explicitly approves external storage and understands portability limits.
- A PDF in a Hermes folder without a Zotero child attachment is not complete.
- A webpage attachment is not complete.
- Verify file existence, `%PDF` signature, nonzero pages, and Zotero open behavior.
- If multiple PDFs exist, set or verify the preferred attachment so double-click opens the intended file.

## File naming

```text
Journal - Article title - Corresponding author.pdf
```

Do not repeat the run date in the file name. Replace path-invalid characters with `-`. Identify the corresponding author from the first-page envelope symbol, a correspondence label, or matching email. Never infer from author order. Use `通讯作者未确认` when unresolved.

## Find Available PDF

For bulk retrieval inside Zotero:

1. Select the PDF-eligible items.
2. Run Find Available PDF.
3. Re-read Zotero state after completion.
4. Count parents with PDF child attachments.
5. Open a sample attachment.

Institutional access can still be blocked by CAPTCHA or publisher automation controls. Do not claim success from a landing page or resolver URL.

## Failure behavior

The collector can save its Markdown/Excel report even when Zotero fails, but the combined 13:00 task must return nonzero and alert the user. Do not allow a missing dated collection to coexist with a green scheduler status.

## Verification

Report:

- dated collection key and item count;
- parents with PDF child count;
- duplicate title count;
- missing current-report titles;
- sampled PDF open result;
- unresolved authorization or upload errors.

---

## Chinese Translation (Reference Only)

The following Chinese text is provided only as a translation to help Chinese-speaking readers. The English section above is the normative version.

## 目标

只有文献条目包含真实、可打开的PDF子附件时，才算完成日期归档。URL字段或网页附件不属于PDF归档。

## 分类层级

顶层分类：

```text
Hermes Weekly: Fire
```

每次执行创建：

```text
YYYY-MM-DD
```

按当前用户要求，只有PDF子附件已经验证的论文才进入日期分类。没有PDF的论文继续保留在Telegram周报中，不要用会打开出版社网页的元数据条目填充Zotero日期分类。

## 安全写入路径

1. 使用Zotero官方Local API、Web API、Connector或“查找可用PDF”；
2. 不直接修改 `zotero.sqlite`；
3. Local API授权前读取 `Zotero-Server-ID`；
4. 使用稳定的应用名称；
5. 一个连续批次只申请一次授权并复用；
6. 凭据只存入系统钥匙串或Secret Manager；
7. 授权超时必须使任务失败。

## 去重

匹配顺序：

1. 规范化DOI；
2. 精确规范化题名；
3. 出版社规范化URL。

同时按题名和DOI查询，因为部分Zotero检索路径无法可靠匹配DOI字段。写入后统计重复题名，只删除本次新建的重复项。

## 附件要求

- 优先导入PDF子附件；
- 仅在用户明确同意外部存储时使用链接文件，并说明不可移植性；
- Hermes目录中的独立PDF不是Zotero附件；
- 网页附件不是PDF附件；
- 验证文件存在、`%PDF`、页数和Zotero打开行为；
- 多个PDF并存时，验证默认打开的首选附件。

## 文件名

```text
期刊 - 论文标题 - 通讯作者.pdf
```

文件名不重复日期，非法路径字符替换为 `-`。通讯作者根据首页信封、Correspondence标记或邮箱确认，不按作者顺序猜测；无法确认时使用“通讯作者未确认”。

## 查找可用PDF

批量执行：

1. 选择可尝试下载的文献；
2. 运行“查找可用PDF”；
3. 完成后重新读取Zotero状态；
4. 统计拥有PDF子附件的母文献；
5. 随机打开一个附件。

机构订阅仍可能被验证码或出版社自动化限制阻塞。出版社落地页不等于PDF下载成功。

## 失败处理

采集脚本可以先保存Markdown/Excel，但组合后的13点任务在Zotero失败时必须返回非零并提醒用户。不能让缺失日期分类的任务显示绿色成功状态。

## 验证输出

报告：

- 日期分类key和条目数；
- 带PDF子附件的母文献数；
- 重复题名数；
- 当前报告中缺失的题名；
- 抽样PDF打开结果；
- 授权或附件错误。
