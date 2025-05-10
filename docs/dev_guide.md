# 开发指南

## 代码质量要求

在提交代码之前，所有代码都必须通过预提交检查。你可以通过以下两种方式运行检查：

1. 使用预提交钩子（自动）：
   - 当你执行 `git commit` 时，预提交钩子会自动运行
   - 如果检查失败，提交将被阻止

2. 手动运行检查：
   ```bash
   ./check.sh
   ```

### 检查项目

代码必须通过以下所有检查才能提交：

1. **代码格式化 (black)**
   - 所有 Python 代码必须符合 black 格式化标准
   - 最大行长度：100 字符
   - 使用 `black .` 可以自动格式化代码

2. **代码质量 (pylint)**
   - 代码质量分数必须达到 10/10
   - 主要检查项目：
     - 命名规范
     - 代码复杂度
     - 代码结构
     - 异常处理
     - 导入顺序
   - 特殊规则可以在 `.pylintrc` 中配置

3. **测试要求 (pytest)**
   - 所有测试必须通过
   - 测试覆盖率要求：
     - 总体覆盖率不低于 70%
   - 必须通过的测试：
     - 验收测试（Acceptance Test）
     - 接口测试（Interface Test）

### 测试策略

1. **验收测试（Acceptance Test）**
   - 目标：
     - 验证系统功能是否符合用户需求
     - 确保系统行为符合预期
   - 原则：
     - 从用户场景出发
     - 关注功能而不是实现
     - 测试即文档
     - 不关心具体实现细节

2. **接口测试（Interface Test）**
   - 目标：
     - 验证接口规范
     - 确保实现一致性
     - 保证接口的健壮性
   - 原则：
     - 验证接口规范
     - 测试正常和异常情况
     - 确保实现一致
     - Mock 模块的外部依赖（如数据库、第三方服务）

### 最佳实践

1. **代码组织**
   - 使用清晰的目录结构
   - 保持模块的单一职责
   - 将实现和测试代码分开放置

2. **接口设计**
   - 使用 ABC（Abstract Base Class）定义接口
   - 接口方法使用 @abstractmethod 装饰器
   - 提供完整的类型提示
   - 为所有方法添加文档字符串
   - 定义清晰的错误类型
   - 保持接口简单，只包含必要的方法

3. **版本控制**
   - 提交信息要清晰明了
   - 每个提交只做一件事
   - 保持提交粒度适中

4. **文档**
   - 为所有公共 API 提供文档字符串
   - 保持注释的及时性和准确性
   - 使用清晰的变量和函数命名

### 开发流程

1. **Outside-In Development with Interface Testing**
   - 从 Acceptance Test 开始
     - 写测试描述用户场景
     - 不关心具体实现
     - 测试即文档
   - 在实现过程中定义接口
     - 在写测试/使用代码时，假设需要的接口已经存在
     - 当发现需要新接口时，立即定义它
     - 接口定义要简单，只包含当前需要的功能
     - 接口是自然形成的，不是预先设计的
   - 编写接口测试
     - 验证接口规范
     - 测试正常和异常情况
     - 确保实现一致
   - 实现临时 Mock 版本
     - 实现最简单的版本
     - 用于运行验收测试
     - 验证接口设计
     - 最终会被真实实现替代
   - 实现真实版本
     - 通过接口测试
     - 通过验收测试
     - 保持接口不变

2. **关键原则**
   - 始终从用户场景出发
   - 接口是自然形成的，不是预先设计的
   - 测试驱动开发过程
   - 保持简单直接

3. **代码编写**
   - 遵循 Python 编码规范
   - 编写测试
   - 及时运行检查脚本

4. **提交代码前**
   - 运行 `pre-commit run --all-files` 确保所有检查通过
   - 检查文档是否更新
   - 确保提交信息符合规范

### 常见问题解决

1. black 格式化失败：
   ```bash
   black .
   ```

2. pylint 警告：
   - 检查 `.pylintrc` 中的规则
   - 必要时添加行内注释禁用特定警告

3. 测试失败：
   - 检查测试输出了解具体失败原因
   - 确保测试环境正确设置
   - 验证测试数据的有效性

# MCP Client 开发简明指南

本节为基于 fastmcp 框架开发 MCP client 的实用指导，涵盖能力发现、工具调用、采样、多协议支持、异常处理与业务封装等核心要点。

---

## 1. 快速入门

### 1.1 连接 MCP 服务器
```python
from fastmcp import Client

async with Client("http://your-mcp-server/sse") as client:
    ...
```
- 支持多种 transport（SSE、WebSocket、Stdio、本地对象等），可自动或手动选择。

### 1.2 能力发现与工具调用
```python
# 获取所有可用工具及参数 schema
tools = await client.list_tools()
for tool in tools:
    print(tool.name, tool.description, tool.inputSchema)

# 调用工具
data = await client.call_tool("weather", {"city": "北京"})
print(data)
```
- 工具参数 schema 可用于前端自动生成表单。

---

## 2. 进阶能力

### 2.1 采样（LLM completion）
- 支持服务端通过 context.sample 请求客户端 LLM 补全。
- 客户端可自定义采样 handler，实现本地推理或安全隔离。
```python
from fastmcp.client.sampling import SamplingMessage, SamplingParams

async def sampling_fn(messages: list[SamplingMessage], params: SamplingParams, ctx):
    # 用你自己的 LLM 客户端处理采样请求
    return "Python"

async with Client(mcp, sampling_handler=sampling_fn) as client:
    ...
```

### 2.2 多服务器与能力聚合
- 支持同时连接多个 MCP 服务器，动态切换或聚合多后端能力。
```python
from fastmcp.client.transports import SSETransport

async with Client(SSETransport("http://server1/sse")) as c1, \
           Client(SSETransport("http://server2/sse")) as c2:
    ...
```

---

## 3. 健壮性与业务封装

### 3.1 异常处理
- 工具调用失败（如工具不存在、参数错误、服务端异常等）会抛出异常，建议统一捕获并友好提示。
- 推荐封装一层业务逻辑，自动处理"无可用服务""连接失败"等场景。

### 3.2 业务封装建议
- 启动时自动拉取工具列表，缓存能力描述，便于 UI/业务层动态适配。
- 根据 inputSchema 自动校验和转换参数，提升健壮性。
- 根据用户意图和工具能力，自动选择最合适的工具和参数。
- 支持结构化内容（文本、图片、嵌入资源等）的统一处理和展示。

---

## 4. 典型场景举例
- 多后端聚合：统一入口，能力聚合
- 插件化扩展：运行时动态注册工具
- 安全隔离：采样能力下发本地 LLM
- 自动化表单：前端根据参数 schema 自动生成
- 快速对接现有 API：OpenAPI/FastAPI 生成 MCP 服务

---

## 5. 参考资料
- [fastmcp 官方文档](https://github.com/fastmcp/fastmcp)
- [gofastmcp.com 文档站](https://gofastmcp.com)
- `examples/` 目录下有丰富的 client/server 代码样例

如需进一步支持，欢迎联系项目维护者或参与社区讨论。 