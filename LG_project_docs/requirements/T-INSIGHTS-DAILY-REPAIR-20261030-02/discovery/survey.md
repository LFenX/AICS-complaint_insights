# 勘察

生成器目前分开验证scope、mail_status合法枚举，但没有验证两者的逻辑关系。隔离临时目录中，明确标成resolved/inquiry/notice/suggestion却误填complaint的合成审阅可以build/publish并计入Top10。原话/最终标准规定已解决、纯咨询、商务和纯愿望不入客诉排行。问题属于可计算字段矛盾，可在组装及审计阻断，不能代替逐封语义分析。反例原件 .runtime/daily-automation-20261030/review-root/status-probe-results.json。历史10月29报告不含这类状态冲突，生产隔离和既有运行边界不变。

独立前向补充确认：7封+1历史/4附件的流程可运行，但read_packet遇长主题突破预算且未声明subject续读；publish同report校验工作目录却不校验既有发布目录原件；check带snapshot时未比对原始subject和recipients_original。证据 .runtime/daily-automation-20261030/review-02/forward-boundary-results.json及cases/report-subject-drift。旧报告to为展示归一化，原始To另存recipients_original，不能混淆。
