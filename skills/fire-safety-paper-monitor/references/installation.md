# Installation and Release

## English (Normative)

## Manual installation from ZIP

1. Extract `fire-safety-paper-monitor-skill.zip`.
2. Copy the `fire-safety-paper-monitor` directory into the active agent profile's skill directory under the `research` category.
3. Start a new agent session so the skill index refreshes.
4. Confirm `fire-safety-paper-monitor` appears in the installed skill list.
5. Load the skill and inspect its linked files before scheduling jobs.

For Hermes, the destination is normally relative to the active `$HERMES_HOME`:

```text
$HERMES_HOME/skills/research/fire-safety-paper-monitor/
```

Do not hardcode another user's absolute path.

## Installation from GitHub

When the repository exposes a valid `SKILL.md`, install by repository identifier or direct raw URL:

```bash
hermes skills install owner/repository/fire-safety-paper-monitor
```

or:

```bash
hermes skills install https://raw.githubusercontent.com/owner/repository/main/fire-safety-paper-monitor/SKILL.md --category research
```

Inspect and audit a third-party skill before installing it.

## Quick setup

1. Copy `templates/journal-rss-table.xlsx` to the chosen monitor directory as `journal_rss_table.xlsx`.
2. Set `FIRE_SAFETY_MONITOR_DIR` to that directory.
3. Run the collector dry test:

```bash
python scripts/weekly-scan.py --no-update --debug
```

4. Inspect source counts and candidate titles.
5. Run one updating collector.
6. Run `scripts/weekly-send.py` within eight hours.
7. Configure optional Zotero 10+ and browser tools.
8. Create the Monday 13:00 and 14:00 schedules only after the manual run passes.

## Zotero version

The automated Local API workflow is supported for Zotero 10 and newer. Earlier versions are not validated. The monitor and Telegram digest can run without Zotero.

The installed Zotero version must expose local application communication, collection writes, item writes, and the chosen PDF attachment method. Test these capabilities before enabling unattended scheduling.

## Browser limitations

The browser fallback cannot bypass Cloudflare, Turnstile, reCAPTCHA, hCaptcha, login, payment, or publisher-specific bot verification. A blocked challenge is a valid terminal outcome, not an error to evade.

## Publishing to GitHub

Use a public repository with:

- bilingual `README.md`;
- `CHANGELOG.md`;
- `SECURITY.md`;
- the complete skill directory;
- a release ZIP;
- screenshots that contain no private data.

Publish from Hermes:

```bash
hermes skills publish <skill-directory> --to github --repo owner/repository
```

## Publishing to ClawHub

After the GitHub source and first release are stable:

```bash
hermes skills publish <skill-directory> --to clawhub
```

Suggested discovery tags:

```text
academic-research
literature-monitoring
rss
zotero
paper-digest
fire-safety
scholarly-workflow
```

## Gitee mirror

Use GitHub as the upstream source of truth and Gitee as a read-only mirror for users in China. Do not develop independent versions in both places.

## Release verification

Before publishing:

- run Python syntax checks;
- dry-run the collector in a temporary directory;
- verify the Excel workbook journal count;
- scan for secrets and absolute personal paths;
- verify every linked reference exists;
- test the release ZIP;
- confirm README version requirements and CAPTCHA limits;
- confirm no screenshot reveals private chat or library data.

---

## Chinese Translation (Reference Only)

The following Chinese text is provided only as a translation to help Chinese-speaking readers. The English section above is the normative version.

## 从ZIP手动安装

1. 解压 `fire-safety-paper-monitor-skill.zip`；
2. 将 `fire-safety-paper-monitor` 目录复制到当前Agent配置的 `research` Skill目录；
3. 新建Agent会话以刷新技能索引；
4. 确认技能列表出现 `fire-safety-paper-monitor`；
5. 创建定时任务前先加载Skill并查看关联文件。

Hermes通常使用：

```text
$HERMES_HOME/skills/research/fire-safety-paper-monitor/
```

不得复制其他用户的绝对路径。

## 从GitHub安装

仓库提供合法 `SKILL.md` 时，可以使用仓库标识：

```bash
hermes skills install owner/repository/fire-safety-paper-monitor
```

或直接使用SKILL.md地址：

```bash
hermes skills install https://raw.githubusercontent.com/owner/repository/main/fire-safety-paper-monitor/SKILL.md --category research
```

安装第三方Skill前应先检查和安全审计。

## 快速配置

1. 将 `templates/journal-rss-table.xlsx` 复制到监测目录并改名为 `journal_rss_table.xlsx`；
2. 设置 `FIRE_SAFETY_MONITOR_DIR`；
3. 干运行：

```bash
python scripts/weekly-scan.py --no-update --debug
```

4. 检查来源数量和题名；
5. 正式运行一次采集；
6. 在8小时内运行 `scripts/weekly-send.py`；
7. 按需配置Zotero 10+和浏览器工具；
8. 手动测试全部通过后，才建立周一13:00和14:00任务。

## Zotero版本

自动Local API流程支持Zotero 10及更新版本，旧版本未验证。没有Zotero时，监测和Telegram周报仍可运行。

安装的Zotero必须提供本机应用通信、分类写入、条目写入和选定的PDF附件方法。无人值守运行前必须实际测试。

## 浏览器限制

浏览器后备无法跳过Cloudflare、Turnstile、reCAPTCHA、hCaptcha、登录、付费或出版社机器人验证。遇到验证是合法终止状态，不得规避。

## 发布到GitHub

公开仓库建议包含：

- 中英双语 `README.md`；
- `CHANGELOG.md`；
- 中英双语 `SECURITY.md`；
- 完整Skill目录；
- Release ZIP；
- 不含私人信息的截图。

Hermes发布命令：

```bash
hermes skills publish <skill目录> --to github --repo owner/repository
```

## 发布到ClawHub

GitHub源码和首个Release稳定后：

```bash
hermes skills publish <skill目录> --to clawhub
```

建议标签：

```text
academic-research
literature-monitoring
rss
zotero
paper-digest
fire-safety
scholarly-workflow
```

## Gitee镜像

以GitHub为上游主仓库，Gitee仅作国内只读镜像。不要在两边独立开发。

## 发布验证

发布前：

- Python语法检查；
- 临时目录干运行；
- 核对Excel期刊数；
- 扫描密钥和个人路径；
- 检查全部关联文件；
- 测试Release ZIP；
- 确认系统/Zotero版本与验证码边界；
- 确认截图不含私人聊天或文库数据。
