# 提交前勘察

GitHub API 实际返回：LFenX/AICS-CCDD，private=true，default_branch=main，size=0，push/admin=true；git ls-remote 成功且无引用。原 complaint-insights 不是 Git 仓库，3030仍运行。

看板读取预先生成的本地report/attachments/archives；源码位于insights与assets。现有根README主要介绍底座和MCP，不能直接作为此看板的运行手册。运行数据、附件、凭据、MCP门户及历史治理材料均不属于本次源码上传清单。

方案：在.runtime/github-delivery-20261030/AICS-CCDD新克隆中保留原相对目录，仅复制19项看板相关源码/配置/测试/第三方许可，编写看板README、依赖和排除规则；所有既有源码按SHA核对。使用同一serve_board入口，不改变运行中的服务或生产隔离。发布前核验整个暂存区而非仅.gitignore。

用户直接指定仓库并要求提交，授权范围包含在该私有仓库创建初始代码提交和推送；不包含上传客户数据或变更访问权限。没有阻断未知。
