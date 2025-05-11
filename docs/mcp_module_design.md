# MCP 模块设计文档（新版）

## 1. 模块定位与职责

### 1.1 MCP 模块的角色
- MCP（Model Context Protocol）模块是主系统与外部能力（工具/服务）之间的桥梁，负责聚合、发现、管理和调用多个 MCP server 上注册的工具。
- 其核心职责：
  - 动态发现和缓存所有已连接 MCP server 的工具能力（能力描述、参数 schema、功能说明等）
  - 提供统一的能力发现和工具调用接口，仅供 chat 模块调用
  - 负责与 MCP server 的通信、异常处理、能力缓存的刷新与失效

### 1.2 依赖关系
- MCP 依赖系统统一配置（如 server 列表、刷新策略等，统一在 src/config 目录下管理）
- MCP 作为中间层，**只为 chat 模块提供能力发现和工具调用接口**，向下对接多个 MCP server

```
用户 → CLI → chat → MCP → MCP-server（可多个）
           ↑      ↑
        配置模块  |
                 └─ 能力缓存
```

---

## 2. 代码结构与接口隔离

```
src/core/mcp/
├── mcp_client_api.py       # MCP 客户端主接口（能力发现、工具调用、能力缓存）
├── mcp_svc_manage_api.py   # 服务器管理与能力聚合
├── manager.py              # 能力缓存、刷新、懒加载等管理逻辑
├── exceptions.py           # MCP 相关自定义异常
├── types.py                # 类型定义与 schema（ToolDescription 等）
└── utils.py                # 工具函数
```
- **mcp_client_api.py**：只暴露 chat 模块需要的接口，chat 只依赖这里，便于解耦和后续替换。
- **manager.py**：负责能力缓存、懒加载、定期刷新、能力失效等机制。
- **mcp_svc_manage_api.py**：负责多 MCP server 的注册、连接、能力聚合。
- **types.py**：统一能力描述、参数 schema、异常类型等。

---

## 3. 主要功能点与接口说明

### 3.1 多 MCP server 支持与能力聚合
- 支持配置多个 MCP server，动态注册/注销。
- 聚合所有 server 的工具能力，统一对外暴露。
- 工具名可带 server 前缀区分（如 server1.weather）。

### 3.2 能力发现与能力缓存
- 提供 `list_tools()` 接口，返回所有聚合后的工具能力描述（含 name、description、input_schema、server 等）。
- 能力缓存支持懒加载、定期刷新、主动失效。
- 工具能力变更时可手动/自动刷新。

### 3.3 工具调用与异常处理
- 提供 `call_tool(tool_name, params)` 接口，自动路由到对应 server。
- 统一异常处理，chat 模块可获知"无此工具""调用失败""连接异常"等状态。

### 3.4 chat 决策链路支持
- MCP 提供能力发现接口，chat 可将能力描述拼进 prompt，辅助 chat 决策。
- MCP 不参与"要不要用工具"的决策，仅负责能力发现和调用。

---

## 4. 典型用例交互流程

### 4.1 系统初始化
- MCP 读取系统统一配置，注册 MCP server，能力缓存为空，等待懒加载。

### 4.2 用户询问"有哪些可用工具"
- CLI → chat：用户输入
- chat → MCP：请求工具能力描述
- MCP 若缓存为空则拉取所有 server 能力，返回聚合能力描述
- chat → CLI：输出工具列表
- CLI 展示工具列表

### 4.3 用户问题无需工具
- CLI → chat：用户输入
- chat → MCP：如需能力描述则获取
- chat 直接生成答案，CLI 输出

### 4.4 用户问题需用工具
- CLI → chat：用户输入
- chat → MCP：获取能力描述
- chat 输出结构化决策（用哪个工具/参数）
- chat → MCP：调用工具
- MCP → MCP-server：实际调用
- 返回结果，chat 生成最终答案，CLI 输出

---

## 5. MCP 对外接口设计

### 5.1 能力发现
```python
async def list_tools(self) -> list[ToolDescription]:
    """
    获取所有聚合后的工具能力描述
    返回: List[ToolDescription]
    """
```
- ToolDescription 包含 name、description、input_schema、server 等

### 5.2 工具调用
```python
async def call_tool(self, tool_name: str, params: dict) -> Any:
    """
    调用指定工具，自动路由到对应 server
    """
```

### 5.3 能力缓存刷新
```python
async def refresh_tools(self) -> None:
    """
    主动刷新能力缓存
    """
```

### 5.4 统一异常
- ToolNotFound, ToolCallError, MCPConnectionError 等

---

## 6. 总结
- MCP 作为能力聚合与发现中枢，支持多 server、能力缓存、懒加载、聚合能力发现。
- 只为 chat 模块暴露简单、解耦的接口，便于 chat 灵活集成。
- 能力描述结构化，便于自动化、低耦合、易扩展。

---

## 7. 术语表（领域模型）

> 代码实现和文档中应严格使用下列英文名，保持一致性。

| 中文名         | 英文名            | 说明                                                                 |
|----------------|-------------------|----------------------------------------------------------------------|
| 工具           | Tool              | MCP Server 提供的、可被调用的能力单元。每个工具有唯一标识、功能、参数等。 |
| 工具描述       | ToolDescription   | 工具的属性集合，包括名称、功能说明、参数定义、返回值说明等。             |
| 工具参数       | ToolParameter     | 工具调用时需要提供的输入信息。参数有名称、类型、是否必填、说明等。        |
| 工具返回值     | ToolOutput        | 工具调用后返回的结构化结果。                                           |
| MCP 服务器     | MCPServer         | 能力服务端，注册并管理一组工具，响应能力查询和工具调用请求。             |
| chat           | chat              | 理解用户意图、决定是否调用工具、生成答案的智能体。                      |
| 用户           | User              | 提出需求、发起请求的主体。                                             |

> 说明：如有新业务核心对象，请补充到本表，并在代码和文档中保持一致命名。

如需详细接口定义或调用流程示例，可进一步补充！ 