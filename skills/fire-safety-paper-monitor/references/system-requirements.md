# System and Software Requirements

## English (Normative)

## Support levels

### Full workflow: validated

The complete workflow—collector, summary agent, isolated browser, Telegram delivery, and Zotero Local API—has been validated on:

- OS: macOS 26.5.2, build 25F84;
- architecture: Apple Silicon;
- Hermes Agent: 0.20.4 (2026.8.18);
- Hermes Python runtime: 3.11.15;
- system Python used for bundled scripts: 3.9.6;
- Zotero: 10.0;
- Google Chrome: 152.0.7977.65;
- cua-driver: 0.20.0.

These are validated versions, not claims that every newer release is automatically compatible. Re-run the verification checklist after upgrades.

### Core collector and sender: supported by design

The bundled `weekly-scan.py` and `weekly-send.py` use Python standard-library APIs and are designed to run on:

- macOS;
- Windows 10/11;
- Linux desktop or server distributions with Python 3.9+.

The scripts have been executed with Python 3.9.6 and Hermes Python 3.11.15. Python versions below 3.9 are unsupported.

### Full browser and Zotero automation outside macOS: experimental

- Windows 10/11: collector and sender should work; full browser, proxy, Zotero authorization, and attachment behavior require testing on the target machine.
- Linux: collector and sender should work; desktop browser control depends on X11/Wayland and the installed accessibility stack. Zotero attachment behavior requires testing.
- Headless servers: collector and API-only summaries can run; native Zotero and desktop-browser control require a graphical session or a separately designed remote workflow.

Do not report Windows or Linux end-to-end support until the target environment passes the full verification run.

## Required software

### Collector only

- Python 3.9+;
- outbound HTTPS access;
- a writable monitor directory;
- the supplied `journal-rss-table.xlsx`;
- a scheduler such as Hermes Cron, cron/systemd timer, Windows Task Scheduler, or GitHub Actions.

Microsoft Excel and LibreOffice are not required. The collector reads and writes `.xlsx` files using the Python standard library.

### Summary stage

- an LLM-capable agent;
- file and network tools;
- a PDF text extractor for full-text summaries.

PyMuPDF is recommended but optional:

```bash
python -m pip install pymupdf
```

Without a PDF extractor, the workflow can still produce metadata and abstract-only digests.

### Hermes deployment

The tested setup uses Hermes Agent 0.20.4. A compatible Hermes build must expose:

- `cronjob`;
- `terminal`;
- `read_file`, `write_file`, `patch`, and `search_files`;
- network/web retrieval or terminal HTTPS access;
- `computer_use` for browser fallback;
- skill loading.

Older Hermes builds lacking one of these capabilities are unsupported for the full workflow.

### Zotero deployment

- Zotero 10.0 or newer is required for the bundled automated Local API workflow;
- Zotero must be installed, running, and signed into the intended library when cloud sync is required;
- local application communication/Local API must be enabled;
- local port `127.0.0.1:23119` must be reachable;
- the user must approve write access;
- the chosen PDF attachment route must be verified on the installed Zotero build.

Zotero versions below 10 are unsupported by this skill. Monitoring and Telegram delivery remain available without Zotero.

### Browser fallback

- Google Chrome or Chromium with a supported driver integration;
- an isolated browser profile;
- a working accessibility/automation driver.

The validated macOS setup uses Chrome 152.0.7977.65 and cua-driver 0.20.0. Other versions require a browser preflight.

On macOS, cua-driver requires:

- Accessibility permission;
- Screen Recording permission.

The skill cannot bypass Cloudflare Challenge/Turnstile, reCAPTCHA, hCaptcha, login, payment, or publisher-specific robot verification. Those pages require lawful human action or remain blocked.

## Network requirements

The machine must reach, as applicable:

- journal RSS/Atom endpoints;
- Springer journal pages;
- Crossref;
- OpenAlex;
- DOI resolvers;
- publisher PDF/HTML endpoints;
- Zotero local API;
- Telegram or the chosen delivery channel.

Institutional full-text access requires the user's lawful campus network, library proxy, VPN, or remote-access method. This user's deployment specifically uses direct campus-network access without VPN/proxy; other users must adapt the network policy to their institution.

Do not change global proxy settings without explicit permission. Check process proxy variables and OS proxy settings separately.

## Storage and hardware

- No GPU is required for the bundled collector or cloud-LLM workflow.
- A normal office computer is sufficient for RSS collection and PDF parsing.
- Local LLM use is optional and introduces model-specific RAM/VRAM requirements not covered by this skill.
- Reserve enough disk space for the growing PDF archive. The skill imposes no fixed quota.
- The monitor directory must support atomic file replacement and persistent state across runs.

## Required configuration

- `FIRE_SAFETY_MONITOR_DIR`: absolute path to the monitor data directory, or rely on the documented `$HERMES_HOME/data/fire_safety_paper_monitor` default.
- `journal_rss_table.xlsx`: copied into the monitor directory.
- LLM credentials: stored in a secret manager when summaries use a cloud model.
- Zotero credentials/grants: stored only in a secret manager or OS keychain when persistence is permitted.
- delivery target: Telegram, WeCom, email, or another channel configured by the host agent.

## Compatibility verification

After any OS, Python, Hermes, Zotero, Chrome, cua-driver, or PDF-library upgrade:

1. run Python syntax checks;
2. run the collector with `--no-update --debug` in a temporary directory;
3. verify journal and source counts;
4. run browser preflight against one non-sensitive publisher page;
5. verify Zotero Local API read and write authorization;
6. create a test collection and attach a test PDF;
7. open the PDF from Zotero;
8. remove test artifacts;
9. run the Telegram format validator;
10. enable recurring scheduling only after all required stages pass.

---

## Chinese Translation (Reference Only)

The following Chinese text is provided only as a translation to help Chinese-speaking readers. The English section above is the normative version.

## 支持层级

### 已完成完整验证的环境

采集、总结、隔离浏览器、Telegram投递和Zotero Local API完整流程已在以下环境验证：

- 操作系统：macOS 26.5.2，Build 25F84；
- 架构：Apple Silicon；
- Hermes Agent：0.20.4（2026.8.18）；
- Hermes Python运行时：3.11.15；
- 运行脚本的系统Python：3.9.6；
- Zotero：10.0；
- Google Chrome：152.0.7977.65；
- cua-driver：0.20.0。

这些是已验证版本，不代表所有更新版本一定兼容。升级后必须重新执行兼容性检查。

### 核心采集和发送脚本

`weekly-scan.py` 和 `weekly-send.py` 仅使用Python标准库，按设计可运行在：

- macOS；
- Windows 10/11；
- 安装Python 3.9或更新版本的Linux桌面或服务器。

脚本已在Python 3.9.6和Hermes Python 3.11.15中实际运行。Python 3.9以下版本不支持。

### macOS以外的完整自动化

- Windows 10/11：检索和发送脚本按设计支持；浏览器、代理检查、Zotero授权和附件必须在目标机器测试。
- Linux：检索和发送脚本按设计支持；桌面控制取决于X11/Wayland和辅助功能环境，Zotero附件必须测试。
- 无桌面服务器：可以执行采集和API摘要；原生Zotero和桌面浏览器需要图形会话或重新设计远程流程。

在目标机器完成全部测试之前，不要声称Windows或Linux端到端支持。

## 必需软件

### 仅采集

- Python 3.9+；
- 出站HTTPS访问；
- 可写且可持久保存的工作目录；
- `journal-rss-table.xlsx`；
- Hermes Cron、cron/systemd timer、Windows Task Scheduler或GitHub Actions等调度器。

不需要安装Microsoft Excel或LibreOffice，脚本使用标准库读写XLSX。

### 总结阶段

- 能调用大模型的Agent；
- 文件和网络工具；
- 需要全文总结时，安装PDF文本提取器。

推荐但非必需：

```bash
python -m pip install pymupdf
```

没有PDF提取器时，仍可生成元数据和摘要周报。

### Hermes部署

已验证Hermes Agent 0.20.4。兼容版本必须提供：

- `cronjob`；
- `terminal`；
- `read_file`、`write_file`、`patch`、`search_files`；
- 网络工具或终端HTTPS能力；
- 浏览器后备所需的 `computer_use`；
- Skill加载能力。

缺少这些工具的旧版Hermes不支持完整流程。

### Zotero部署

- 自动Local API流程要求Zotero 10.0或更新版本；
- Zotero必须安装并运行；
- 需要云同步时，应登录目标文库；
- 开启本机应用通信/Local API；
- `127.0.0.1:23119`可访问；
- 用户批准写入权限；
- 在当前Zotero版本中验证PDF附件写入方法。

Zotero 10以下版本不支持。没有Zotero时，检索和Telegram周报仍可运行。

### 浏览器后备

- Google Chrome或Chromium；
- 隔离浏览器配置；
- 可用的自动化驱动。

已验证Chrome 152.0.7977.65和cua-driver 0.20.0。其他版本应执行浏览器预检。

macOS中cua-driver需要：

- 辅助功能权限；
- 屏幕录制权限。

Skill无法跳过Cloudflare Challenge/Turnstile、reCAPTCHA、hCaptcha、登录、付费或出版社机器人验证。此类页面需要用户合法操作，否则保持阻塞状态。

## 网络要求

按任务范围，机器需要访问：

- 期刊RSS/Atom；
- Springer期刊页面；
- Crossref；
- OpenAlex；
- DOI解析器；
- 出版社PDF/HTML；
- Zotero Local API；
- Telegram或其他投递渠道。

机构全文取决于用户合法的校园网、图书馆代理、VPN或远程访问方式。本用户环境明确使用校园网直连且不使用VPN/代理；其他用户应按学校政策调整。

不得未经用户同意修改全局代理。进程代理变量和系统代理必须分别检查。

## 硬件和存储

- 云端大模型流程和核心采集不需要GPU；
- 普通办公电脑足以完成RSS采集和PDF解析；
- 本地大模型的内存/显存需求由所选模型决定，不属于本Skill固定要求；
- PDF会长期增长，应预留足够磁盘空间；
- 工作目录必须支持原子文件替换并跨任务保存状态。

## 必需配置

- `FIRE_SAFETY_MONITOR_DIR`：监测数据目录绝对路径，或使用 `$HERMES_HOME/data/fire_safety_paper_monitor` 默认值；
- `journal_rss_table.xlsx`：放入监测目录；
- 大模型凭据：使用Secret Manager；
- Zotero授权：需要持久化时，只保存于Secret Manager或系统钥匙串；
- 投递目标：由宿主Agent配置Telegram、企业微信、邮件或其他渠道。

## 兼容性检查

系统、Python、Hermes、Zotero、Chrome、cua-driver或PDF库升级后：

1. 运行Python语法检查；
2. 在临时目录执行 `--no-update --debug`；
3. 核对期刊和来源数量；
4. 在非敏感出版社页面执行浏览器预检；
5. 验证Zotero Local API读写授权；
6. 创建测试分类并附加测试PDF；
7. 从Zotero打开PDF；
8. 删除测试产物；
9. 验证Telegram格式；
10. 全部通过后再恢复定时任务。
