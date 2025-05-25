# 子系统职责与接口一览

## app

**职责**：负责系统的启动、初始化和生命周期管理，是各个子系统的容器和协调者

_无 API 接口定义_


---

## chat

**职责**：chat 子系统职责：管理与用户的对话过程及对话历史，提供对话会话的创建、消息发送、历史查询等能力。

### 接口类：ChatService

聊天服务接口

定义了聊天服务的基本功能，包括消息发送和上下文管理。

- `get_context()`

  - 获取当前对话上下文    Returns:      List[Dict[str, str]]: 对话历史，每个消息包含 role 和 content

- `clear_context()`

  - 清除当前对话上下文


---

## util

**职责**：subsystem responsibility to be added

_无 API 接口定义_


---

## config

**职责**：config 子系统职责：统一管理系统（包括子系统）的配置，负责响应各个模块的配置参数请求。

### 接口类：ConfigSupplier

- `get_llm_config()`

- `get_app_config()`


---

## mcp

**职责**：mcp 子系统职责：管理 MCP 服务器及其提供的工具的使用，负责响应工具的调用请求和工具能力的查询。

_无 API 接口定义_


---

## cli

**职责**：cli 子系统职责：用户操作界面，作为用户交互的入口，负责接受并回复用户消息，以及接受并回复用户输入的系统命令。

_无 API 接口定义_


---
