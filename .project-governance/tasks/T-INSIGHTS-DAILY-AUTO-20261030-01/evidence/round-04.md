# 第四轮审查：中断，覆盖不完整

原审查者：/root/adversarial_round04；开始于2026-10-30T21:14:04.2603521+08:00。
root在2026-10-30T18:10:28.851689+00:00检查实际落盘证据并汇总。原审查运行已不在活动Agent列表，未产生独立完整报告；不推断中断的具体原因或准确时刻，不将本轮计为干净轮次。

交付：T-INSIGHTS-DAILY-REPAIR-20261030-03，subject e7a90e31fdf6f7e57d6fa3d785ce3a3e81cdf23167e28ebe70274e4aa57572ce；当前46项交付清单逐项重核无漂移。

## 已确认问题 R04-IMAP-01（P1）

同邮箱、同文件夹复用IMAP连接时，只在首次EXAMINE后比较UIDVALIDITY；第二封不同冻结epoch仍执行FETCH，并将冻结值写为identity_verified=true。

输入：第一封冻结77、第二封冻结66，服务实际INBOX=77，UID为201/202；两个真实内存MIME均能匹配附件part和摘要。
预期：第一封ready，第二封UIDVALIDITY_MISMATCH，第二封不得FETCH或保存。
实际：ready=2、failed=0；第二封manifest标identity_verified=true和uidvalidity=66，实际连接仍为77。
位置：insights/attachment_fetcher.py work()中UIDVALIDITY比较位于selected != folder分支内（首次读取源码约152–158行）。
影响：源清单跨UID epoch时，复用连接绕过邮件身份边界；即便MIME摘要/Message-ID还有检查，也不能把未核验epoch的附件认证为已核验。未连接真实IMAP，不能据此声称历史405附件发生了取错。

独立正反控制还覆盖：同folder同epoch两封正常复用；切换folder正确epoch通过/错误epoch拒绝；瞬断后正确epoch重连通过/错误epoch拒绝；首封错误epoch拒绝后次封正确epoch重新建立连接。完整输入、调用与manifest见review-04/imap-controls/summary.json。

## 已有实际证据与未完成边界

- results.json：75项回归0失败/0跳过；新9封邮件经完整读取、Agent逐封归类、build及私有publish/重复发布，源分类不决定归组，纯咨询不入客诉榜，零前值不伪造增幅。
- formal-results.json与independent-history-delta.json：634来源字段/一次计数，405原件、358预览、35ZIP及815文件初版归档一致；业务修订限定3封，原件及ZIP不变。
- ui-evidence.json与four-sort-independent-comparison.json：四排序逐页各634唯一ID，顺序与独立比较一致；日期缺报、昨天、原译、侧栏、子组ZIP等已有实际操作。
- all-resources-http.json：798次真实只读HTTP请求（405原件/358预览/35ZIP）字节摘要一致。
- uid-evidence-all.json：150个有UID证据的记录完成原始RFC图检查；26个机械原句匹配告警尚未由原审查者完成语义裁决，不能将数字直接称为UID错误。root另核对若干原句，存在换行引号/全半角等标准化差异，但没有据此裁决全部26项。

本轮未完成：全量UID证据告警裁决；PDF/视频等附件类型完整UI矩阵；原文完整逐项最终矩阵和最终独立结论。旧R03三项在本轮不补造Fixed，交由下一完整轮以新证据裁决。

限制：既有本地副本DEGRADED和生产隔离；未连真实生产/IMAP或外部模型，未证实首次00:30真实执行结果，未热部署旧API元数据。中断不是用户要求停止，后续沿用父Accepted审查及同范围修复授权。
