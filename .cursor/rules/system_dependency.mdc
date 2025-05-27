# 子系统依赖与组装管理规范

为保证系统的可维护性、可扩展性和解耦性，子系统间的依赖与组装必须遵循如下规范：

1. **子系统间依赖解耦**
   - 各子系统不得直接依赖其他子系统的实现，仅可 import 其他子系统的接口（如 API 抽象类）。
   - 禁止跨子系统直接引用实现类或内部模块，确保各子系统的独立性和可替换性。

2. **依赖注入与组装方式**
   - 子系统间的依赖关系通过依赖注入（Dependency Injection, DI）进行管理，严禁在子系统内部硬编码依赖。
   - 推荐使用依赖注入框架（如 dependency_injector）统一管理依赖的声明与注入，避免手动实例化依赖对象。

3. **接口与容器的暴露**
   - 每个子系统仅通过 `__init__.py` 对外暴露接口（API 抽象类）和 container（依赖注入容器）。
   - 典型的 `__init__.py` 示例：
     ```python
     """
     chat 子系统职责：管理与用户的对话过程及对话历史，提供对话会话的创建、消息发送、历史查询等能力。
     """
     from .api.chat_service_api import ChatService
     from .container import Container

     __all__ = ["ChatService", "Container"]
     ```
   - 其他实现细节、工具类、内部模块等均不得对外暴露。

4. **子系统自包含与创建分离**
   - 每个子系统需提供独立的 container，负责本子系统内部所有依赖的声明与实例化。
   - 子系统 container 仅声明自身依赖（如通过 `providers.Dependency()`），不直接创建外部依赖对象。
   - 例如：
     ```python
     class Container(containers.DeclarativeContainer):
         configer = providers.Dependency()
         chat_service = providers.Singleton(ChatServiceImpl, configer=configer)
     ```

5. **顶层系统组装与依赖管理**
   - 顶层 app 层需提供统一的 AppContainer，负责所有子系统 container 的创建、依赖注入与组装。
   - AppContainer 通过 providers.Container 方式组合各子系统 container，并负责依赖的传递与实例的统一管理。
   - 典型的 app 层 container 示例：
     ```python
     class AppContainer(containers.DeclarativeContainer):
         config_container = providers.Container(ConfigContainer)
         configer = config_container.provided.configer

         chat_container = providers.Container(ChatContainer, configer=configer)
         chat_service = chat_container.provided.chat_service

         cli_container = providers.Container(CliContainer, chat_service=chat_service)
         cli_bot = cli_container.provided.cli()
     ```

6. **依赖声明与注入流程**
   - 子系统 container 通过 providers.Dependency() 显式声明外部依赖，由上层 container 注入具体实现。
   - 禁止在子系统内部直接实例化外部依赖，所有依赖均应通过容器注入。

7. **依赖与组装的唯一入口**
   - 系统的依赖关系和组装流程仅允许在顶层 app container 中进行，禁止在其他位置手动组装或注入依赖。
   - 这样可确保依赖关系的可追踪性和系统初始化流程的统一。

8. **对外部系统依赖的适配（Adapter 规范）**
   - 子系统如需依赖外部服务（如 LLM、数据库、第三方 API 等），必须通过 Adapter（适配器）进行解耦，严禁直接依赖外部库或服务的实现。
   - Adapter 必须定义为接口（抽象基类），并在子系统内部实现具体适配逻辑。
   - Adapter 的实例化与依赖注入应通过子系统的 container 管理，禁止在业务代码中直接实例化外部依赖。
   - 业务代码仅依赖 Adapter 接口，不关心具体实现，确保外部依赖的可替换性、可测试性和系统的解耦性。
   - 典型示例：
     ```python
     from abc import ABC, abstractmethod
     from typing import List, Dict

     class LLMAdapter(ABC):
         @abstractmethod
         async def chat(self, messages: List[Dict[str, str]]) -> str:
             """发送消息列表，返回回复内容"""
     ```
