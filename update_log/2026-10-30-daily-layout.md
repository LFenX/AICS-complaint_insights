# 日报补充统计下移

时间：2026-10-30T14:49:16.843096+08:00。

用户原文：请将图中叉掉的部分下移到底部。

- `assets/daily-board.js`：仅移动shell模板，后三项指标和两张收件图放在原信明细及分页之后；前三项指标继续在结论下。原图表、筛选和下载ID及事件保持一致。
- `assets/daily-board.css`：指标容器改为三列，窄屏单列，去掉旧六格专用边框规则。
- `assets/daily-board.html`：资源版本更新为20261030-layout-01。
- `LG_project_docs/requirements/T-INSIGHTS-DAILY-20261030-01/prd/daily-report.md`：同步页面顺序和实施状态。

验证：node --check通过；真实浏览器1280/1488宽度看到顶部3项、底部3项、15根趋势柱及24根分时柱；点击18时柱筛选79封，重置恢复634封。两地址实际返回新版静态资源且与磁盘SHA一致。报告SHA、后端代码、网络配置及生产隔离不变。没有新建或重跑后端测试，未从移动设备实测；原小时联动通过真实浏览器完成。

首次刷新后过早读取main时DOM尚未完成渲染，探查出现null；改为显式等待Top10可见后核验成功。测试期间发现原浏览器已打开邮件详情，后续改用独立隐藏测试页；未关闭用户详情。

证据：`.runtime/daily-layout-20261030/verification.json`、`browser-verification.json`、`top-final.jpg`、`bottom-test-final.jpg`。原文件备份在同目录before/，可以恢复四个同名文件；本轮未重启服务或推送GitHub。
