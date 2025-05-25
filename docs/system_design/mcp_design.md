# MCP 模块设计文档（新版）

## 1. 模块上下文（定位与职责）

### 1.1 MCP 模块的角色与位置
- MCP（Model Context Protocol）模块是主系统与外部能力（工具/服务）之间的桥梁，负责聚合、发现、管理和调用多个 MCP server 上注册的工具。
- 只为 chat 模块提供能力发现和工具调用接口，向下对接多个 MCP server。

### 1.2 上下文架构图
```
用户 → CLI → chat → MCP → MCP-server（可多个）
           ↑      ↑
        配置模块  |
                 └─ 能力缓存
```
- MCP 依赖系统统一配置（如 server 列表、刷新策略等，统一在 config 模块管理）。
- MCP 作为中间层，聚合所有 MCP server 能力，统一对外暴露。

---

## 2. 核心能力

### 2.1 主要功能点
- 动态发现和缓存所有已连接 MCP server 的工具能力（能力描述、参数 schema、功能说明等）。
- 提供统一的能力发现和工具调用接口，仅供 chat 模块调用。
- 负责与 MCP server 的通信、异常处理、能力缓存的刷新与失效。
- 支持多 MCP server 的注册、注销与能力聚合。

### 2.2 典型用例/交互流程

#### 2.2.1 系统初始化
- MCP 读取系统统一配置，注册 MCP server，能力缓存为空，等待懒加载。

#### 2.2.2 用户询问"有哪些可用工具"
1. CLI → chat：用户输入
2. chat → MCP：请求工具能力描述
3. MCP 若缓存为空则拉取所有 server 能力，返回聚合能力描述
4. chat → CLI：输出工具列表
5. CLI 展示工具列表

#### 2.2.3 用户问题无需工具
1. CLI → chat：用户输入
2. chat → MCP：如需能力描述则获取
3. chat 直接生成答案，CLI 输出

#### 2.2.4 用户问题需用工具
1. CLI → chat：用户输入
2. chat → MCP：获取能力描述
3. chat 输出结构化决策（用哪个工具/参数）
4. chat → MCP：调用工具
5. MCP → MCP-server：实际调用
6. 返回结果，chat 生成最终答案，CLI 输出

---

## 3. 对外接口和服务

### 3.1 接口定义

MCP 对外提供如下接口：

- **list_tools()**
  - 说明：获取所有聚合后的工具能力描述。
  - 参数：无
  - 返回：工具能力描述列表（每项包含 name、description、input_schema、server 等）

- **call_tool(tool_name, params)**
  - 说明：调用指定工具，自动路由到对应的 MCP server。
  - 参数：
    - tool_name：工具名称（如 server1.weather）
    - params：调用参数（dict，需符合工具 input_schema）
  - 返回：工具调用结果（类型依赖具体工具）

- **refresh_tools()**
  - 说明：主动刷新能力缓存，重新拉取所有 MCP server 的能力信息。
  - 参数：无
  - 返回：无

### 3.2 异常与接口约定
- ToolNotFound, ToolCallError, MCPConnectionError 等。
- 所有接口为异步，返回统一结构，异常需带错误码。
- 工具名可带 server 前缀区分（如 server1.weather）。

---

## 4. 内部结构

### 4.1 子模块与职责
```
src/core/mcp/
├── mcp_client_api.py       # MCP 客户端主接口（抽象接口）
├── mcp_client_impl.py      # MCP 客户端实现
├── manager.py              # 能力缓存、聚合、生命周期管理（本地）
├── svc_manager.py          # MCP server 连接、注册、能力拉取（远端）
├── types.py                # 类型定义与 schema（ToolDescription 等）
├── exceptions.py           # MCP 相关自定义异常
└── utils.py                # 工具函数
```
- **mcp_client_api.py**：只定义抽象接口。
- **mcp_client_impl.py**：实现接口。
- **manager.py**：负责本地能力缓存、聚合、懒加载、定时刷新、能力失效等本地生命周期管理。
- **svc_manager.py**：负责与多个 MCP server 的连接、注册、能力拉取、健康检查等远端服务管理。
- **types.py**：统一能力描述、参数 schema、异常类型等。

### 4.2 子模块交互与内部流程
- mcp_client_api 作为唯一对外接口定义，mcp_client_impl 作为主要实现。
- manager 负责本地能力缓存和聚合，依赖 svc_manager 拉取远端能力。
- svc_manager 负责与各 MCP server 的连接、能力拉取、注册和健康检查。
- types.py 统一数据结构，exceptions.py 统一异常。

---

## 5. 变更历史/维护人/参考资料

| 版本 | 日期       | 作者     | 主要变更说明                 |
|------|------------|----------|------------------------------|
| 1.1  | 2024-05-31 | 你自己   | 明确接口与实现分离，补充示例  |

- 参考资料：
  - [overall_design.md](./overall_design.md)
  - [需求文档 req_and_ac.md](../requirement/req_and_ac.md)

