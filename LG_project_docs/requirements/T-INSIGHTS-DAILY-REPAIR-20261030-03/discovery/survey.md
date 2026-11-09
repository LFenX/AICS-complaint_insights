# 实际勘察

第三次完整独立报告.runtime/daily-automation-20261030/review-03/independent-report.md确认三项：缓存只按存在复用，错误/空图与无关日志能重签发布；103439/103469沿真实RFC链对应103426切图10%问题，却分入启动；103108与103665为英日同一脚本初始化失败弹窗，拆成两子ID。root另以私有探针复现缓存并核对五封原文，未改正式文件。

证据：review-root/preview-cache-probe-results.json、review-root/history-cases.json、review-03/historical-expected-revisions.json。预览转换由attachment_preview负责，日报build调用其公开接口；服务继续只加载预计算读取模型。旧报告为固定SHA兼容的已审格式，包含合法逐封子标签别名；仅把两个经过全量核验的确定旧格式字节纳入兼容，不按日期或可伪造元数据放宽新报告。
