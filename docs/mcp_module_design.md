# MCP 模块设计文档

## 1. 模块定位与依赖关系

### 1.1 MCP 模块的角色
- MCP（Model Context Protocol）模块是系统中负责与外部 MCP 服务器通信、能力发现、工具调用、服务能力聚合的独立子系统。
- 其核心职责是：根据主系统需求，动态发现 MCP 服务器能力，智能决策是否调用 MCP 服务，并将结果返回给主系统。

### 1.2 依赖关系梳理
- **CLI（命令行/入口）**：负责接收用户输入、参数解析、流程调度等。
  - 依赖 LLM/对话模块
- **LLM/对话模块**：负责理解用户意图、对话管理、生成回复。需要外部知识/工具时，调用 MCP 能力。
  - 依赖 MCP 客户端模块
- **MCP 客户端模块**：负责与 MCP 服务器通信，发现能力、调用工具、返回结构化结果。
  - 依赖 fastmcp、配置管理、日志等基础设施

依赖链：
```
CLI → LLM/对话 → MCP → fastmcp/配置/日志
```

---

## 2. 代码结构与接口隔离

```
src/core/mcp/
├── api/                # 对外接口层（主系统只依赖这里）
│   ├── __init__.py
│   ├── client.py       # MCP 客户端主接口（如 connect, list_tools, call_tool, ...）
│   ├── service.py      # 服务器管理与能力发现接口
│   └── __init__.py
├── config.py           # 配置加载与校验（依赖主系统的统一配置模块）
├── manager.py          # 服务器连接与状态管理（如连接池、健康检查等）
├── exceptions.py       # MCP 相关自定义异常
├── types.py            # 类型定义与 schema
├── decision.py         # 智能决策逻辑（内部使用，不对外暴露）
└── utils.py            # 工具函数（如日志、参数校验等）
```
- **api/**：只暴露主系统需要的接口，主系统只依赖这里，便于解耦和后续替换。
- **config.py**：通过主系统的统一配置模块获取和校验 MCP 相关配置。
- **manager.py**：统一管理 MCP 服务器连接、能力缓存、健康检查等。
- **decision.py**：内部实现"是否用 MCP 回答"的智能决策逻辑，主系统无需感知。
- **exceptions.py/types.py**：统一异常和类型，便于主系统友好处理和类型安全。

---

## 3. 主要功能点与接口说明

### 3.1 服务器配置与能力发现
- 支持多 MCP 服务器配置，动态加载和切换。
- 提供接口查询所有可用服务器及其能力（如有哪些工具、参数、描述等）。

### 3.2 工具调用与异常处理
- 提供接口指定服务器、指定工具进行调用，返回结构化结果。
- 统一异常处理，主系统可获知"无服务""连接失败""无有效响应"等状态。

### 3.3 智能决策（内部实现）
- 根据用户问题、能力描述、服务器状态等，自动判断是否用 MCP 服务回答。
- 若无需 MCP 或 MCP 无法提供有效信息，则直接返回本地结果或提示。

### 3.4 健壮性与扩展性
- 支持能力缓存、断线重连、健康检查等机制，提升健壮性。
- 便于后续扩展更多 MCP 服务器或协议。

---

## 4. 技术选型说明

- **fastmcp**：作为底层协议库，负责与 MCP 服务器通信，能力发现、工具调用等。
- **pydantic/omegaconf**：用于配置管理和类型校验，保证配置安全和灵活。
- **自定义异常与类型**：保证主系统与 MCP 解耦，便于维护和测试。
- **接口隔离**：主系统只依赖 api/ 下的接口，内部实现可灵活替换。

---

## 5. 依赖关系图（谁依赖谁）

CLI
 │
 ▼
LLM/对话
 │
 ▼
MCP
 │
 ▼
fastmcp/配置/日志
```

---

## 6. 总结

- MCP 作为独立、解耦的能力服务模块，主系统只需通过 api/ 层接口与之交互。
- MCP 依赖 fastmcp、配置管理、日志等基础设施，内部实现细节对主系统透明。
- 结构清晰、易于维护、便于扩展和团队协作。

如需详细接口定义或调用流程示例，可进一步补充！ 