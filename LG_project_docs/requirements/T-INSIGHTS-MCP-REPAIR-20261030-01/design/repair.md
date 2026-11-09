# MCP审查返修设计

需求、授权和四项原始反例见 discovery/survey.md。原需求和权限基线引用父任务 before.json，不重写原结果或正式人类门禁。

|问题|修复与故障边界|验证|
|---|---|---|
|R1-01 匿名占满挑战|有效Cookie重载复用挑战；按实际TCP来源限制8个活跃挑战和30次/分钟新建；全局512个挑战、1024个来源的内存硬上限；挑战10分钟且绑定peer、单次使用|同浏览器512次刷新和清Cookie8次后的另一peer仍可登录；限额来源429且601秒恢复；HTTPS、Host、Origin和登录失败窗口不变|
|R1-02 元数据故障无法网页撤销|token_inventory分离授权与展示元数据读取；元数据损坏保留有效身份和撤销表单，隐藏发放；issue_token仍拒绝损坏元数据，revoke_token先提交授权撤销；授权文件损坏仍全部拒绝|真实产品网页隔离夹具：登录303、管理200、发放400未写、撤销303授权归零；原元数据损坏字节不覆盖|
|R1-03 输入宽松转换|MCPServer公开list_tools/call_tool扩展点，在SDK预解析前按当前公开JSON Schema和日期format校验；inputSchema明确additionalProperties=false；不回显无效参数值|原始HTTP错误整数/布尔/数字日期/无效日期/额外参数均isError，FakeAPI调用数为0；合法日期布尔整数控制案例正常查询|
|R1-04 未知工具错误分层|已知工具仍执行错误isError；未知工具MCPError(-32602)由SDK保留为顶层JSON-RPC错误|原始HTTP响应保留请求id，有error.code=-32602且无result|

jsonschema4.26.0已安装且为MCP2.3声明依赖；本项目显式锁定版本，不引入未核实模块。只重启本项目desk/mcp，公开Schema从实际服务tools/list捕获后重建指南/ZIP。真实验证临时签发身份并在finally撤销；不故障注入真实文件、不运行真实登录洪泛、不改变管理员密码或现有接收人授权。

残余限制：分布式请求仍受全局内存硬上限，不能声称消除所有DoS；共享同一TCP出口共用登录限额。另一内网电脑路由/私有CA安装未实测。正式人类门禁和用户验收仍Pending，机器对抗审查登记因父结果Deferred被拒绝，不能据独立报告冒称机器Passed。

协议依据：[MCP 2025-11-25 Tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)。
