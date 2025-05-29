# 子系统职责与接口一览

## app

**职责**：负责系统的启动、初始化和生命周期管理，是各个子系统的容器和协调者

_无 API 接口定义_


---

## chat

**职责**：chat 子系统职责：负责与LLM模型交互，处理用户输入，并返回响应。

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

**职责**：负责提供配置信息，包括LLM模型配置、服务器配置等。

### 接口类：ConfigSupplier

- `get_llm_config()`

- `get_app_config()`


---

## mcp

**职责**：mcp 子系统职责：管理 MCP 服务器及其提供的工具的使用，负责响应工具的调用请求和工具能力的查询。

### 接口类：ServerRegistry

MCP服务器注册与管理接口，负责服务器的增删查改。

- `list_servers()`

  - 获取所有已注册的服务器信息。

- `add_server(name, url)`

  - 添加新服务器。若名称重复则添加失败。

- `remove_server(name)`

  - 删除指定名称的服务器。  若服务器不存在则删除失败。

- `get_server(name)`

  - 获取指定名称服务器的详细信息。  若不存在则返回 None。

- `edit_server(name, url)`

  - 修改指定服务器的地址。  若服务器不存在则修改失败。


---

## cli

**职责**：cli 子系统职责：用户操作界面，作为用户交互的入口，负责接受并回复用户消息，以及接受并回复用户输入的系统命令。

_无 API 接口定义_


---
