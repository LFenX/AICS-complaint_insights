# 实际补充反例

root以独立R05原始9封/2附件候选作局部反例，报告的图片ready=false/status=failed，删除原图片且维持quality的report SHA一致；source及manifest仍要求该附件，publish却返回published，随后audit_published_report返回validated。实际结果publication-followup-probe/result.json已登记父Blocked，不计完整一轮。源码audit_report只在item.ready为真时核验字节，未先要求全部附件完成。

正式c5150286报告405件均为布尔True/ready，未修改正式数据或服务。修复在共享audit_report前置强制ready is True且status=ready；完整冻结集合和现有摘要/原件/预览/ZIP/source校验继续执行；零附件为合法空集合。需要验证低报就绪、状态冲突和非布尔声明不能使缺失资源逃过检验，即使quality摘要自洽。

仅数据完整性检查与测试，不改变身份、凭据、网络、权限、数据访问范围、生产/IMAP/数据库/调度或任何服务。沿用Full返修检查覆盖，不新增安全门或风险接受。
