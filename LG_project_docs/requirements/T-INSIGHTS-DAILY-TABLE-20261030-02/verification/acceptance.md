# 表格与子问题日志 ZIP 工程核验

核验日期：2026-10-30，Asia/Shanghai。任务：T-INSIGHTS-DAILY-TABLE-20261030-02。

交付入口：http://127.0.0.1:3030/ 。报告日期：2026-10-29；读取模型 SHA-256：`b2658daf25058d0ce07ee620d60266039998b5c767ddd0d81721698b3de93760`。

## 实际结果

| 原文要求 | 工程结果 | 证据 |
| --- | --- | --- |
| 压缩底部空白，留自然间距 | 桌面底部 padding 20px；实际浏览器文档底部间距 19.515625px；移动样式 16px | browser-result.json、bottom-final.jpg；移动尺寸未单独实机核验 |
| 去掉截图中的底部说明 | 原底部说明及版本尾栏已删除；浏览器无 footer | browser-result.json |
| 去掉时间、主键列 | 表格现有 9 列；时间和内部主键保留在详情、搜索及数据中 | browser-verification.json |
| UID 第一列 | 首列表头为“游戏 UID / 依据” | browser-result.json、subgroup-zip-final.jpg |
| 按 UID、日志、图片、其他文件是否存在分别排序，有的放前面 | 默认有 UID 优先；四种排序各遍历全部分页，634 个邮件 ID 无缺失或重复；有内容分别为 150、50、175、41 封 | browser-verification.json、browser-result.json |
| 子问题日志批量 ZIP 下载 | 全部 35 个 ZIP 实际 HTTP 获取并核验，覆盖 86 个日志；归属、原件字节摘要、清单和 ZIP 摘要一致 | archive-verification.json |
| 下载入口结合问题组筛选 | 子问题工具行右侧显示文件数、邮件数和下载按钮；无日志子问题显示禁用原因；实际浏览器下载成功 | browser-verification.json、subgroup-zip-final.jpg |

上述运行证据统一位于项目 `.runtime/daily-table-20261030/`。逐句对应记录见 [requirements-coverage.md](requirements-coverage.md)。

## 验证方法和边界

- `.venv/Scripts/python.exe -m unittest discover -s tests -v`：106 项通过，耗时 34.928 秒，原始输出 `tests.log`。测试总数包含并行 MCP 会话已有测试，不代表该会话已交付。
- `verify_archives.py`：校验全部 35 包/86 个日志、完整子问题归属、压缩路径安全、原件和 ZIP 摘要，以及未知资源 404、旧版本 409、Host/Origin 拒绝。
- `verify_browser.py`：独立读取真实浏览器导出的四种分页 ID 顺序，以报告中的实际 UID/文件判定存在性；全量覆盖 634 封。校验 UID 首列、9 列、无旧 footer、底部间距、无控制台错误及两次实际下载字节摘要。
- 浏览器实际切换到没有日志的“启动黑屏，无法进入游戏”，确认按钮禁用且没有下载链接；随后返回“登录或账号验证失败”。搜索结果为 0 时，已选择子问题的整组下载仍覆盖该组全部日志。
- `tests/test_log_archive.py`：确定性、同名文件隔离、坏文件/缺失文件拒绝、身份/权限/Feature/资源/版本/方法限制及审计内容核对。
- 与本轮 before 报告逐封对照：634 封业务字段与原分类不变，仅增加证据存在性和 ZIP 元数据。原件未修改。
- `isolation.json`，2026-10-30 04:54:05 +08:00：生产读取开关 false、生产 5432 连接数 0、watch 进程 0、3030 仅监听 127.0.0.1。

## 运行与正式记录状态

本轮七项功能均已实现并完成上述工程核验，可在 3030 使用。用户决定仍为 Pending，未将测试通过登记成人工验收。

任务已声明的 `security-privacy-review` 尚无绑定此版本的人工通过记录，因此正式工程状态保存为 Deferred；测试不替代该门禁。没有宣称本版本已完成连续两轮完整对抗性审查。

正式任务包校验另有未解决工具问题：`validate_task_package.py --check-mapping` 两次报告 active query 为 S4，而本任务 Tailoring/NormPacket 为 S5。经官方 `compile_norm_context.py --stage S5 --enforce` 和新 `get_context.py` 重建后仍相同，保留 `task-validation.log`、`task-validation-a3.log`，未修改 skill、查询缓存或规范来消除报错；这项治理校验未通过，与上述产品测试分开记录。

源数据仍为隔离快照，冻结时间为 2026-10-30 01:13:42 +08:00；本轮未验证生产实时完整性或增量时效。移动端 16px 为代码核对，未做移动设备实机测试。
