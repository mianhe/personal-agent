# 接口定义规范

为确保系统的可维护性、可扩展性和解耦性，所有子系统的接口定义必须遵循如下规范：

1. **接口文件的组织**
   - 接口文件必须放在子系统的 `api` 子目录下。
   - 默认情况下，一个子系统只需一个接口文件。接口文件命名应体现其主要职责，并以 `_api` 结尾，如：`user_management_api.py`。

2. **接口类的设计**
   - 一组紧密相关的接口方应组成一个接口类。
   - 接口类必须为纯抽象类（继承 `ABC`，所有方法用 `@abstractmethod` 标记），且每个接口类必须有 docstring 说明其职责。
   - 接口文件不得包含任何实现代码，仅可定义接口类及与接口直接相关的数据结构（如 dataclass、TypedDict、pydantic.BaseModel 等），用于描述接口的输入、输出或领域对象。如有多个接口类，需确保各自职责边界清晰，避免重复。
   - 所有接口类、方法及相关数据结构必须完整标注类型注解，明确参数和返回值类型，确保类型契约清晰、可静态检查。
   - 典型接口文件示例：
     ```python
     from abc import ABC, abstractmethod
     from dataclasses import dataclass

     @dataclass
     class UserInfo:
         user_id: str
         name: str
         email: str

     class UserManager(ABC):
         """
         用户管理接口，负责用户的创建、查询、更新、删除等基础用户管理操作。
         """
         @abstractmethod
         def create_user(self, user_info: UserInfo):
             """创建用户"""
             pass

         @abstractmethod
         def get_user(self, user_id: str) -> UserInfo:
             """获取用户信息"""
             pass

         @abstractmethod
         def update_user(self, user_id: str, user_info: UserInfo):
             """更新用户信息"""
             pass

         @abstractmethod
         def delete_user(self, user_id: str):
             """删除用户"""
             pass

     class UserAuthenticator(ABC):
         """
         用户认证接口，负责用户的身份认证、密码重置等安全相关操作。
         """
         @abstractmethod
         def authenticate(self, username: str, password: str) -> bool:
             """用户身份认证"""
             pass
     ```

3. **接口的对外暴露**
   - 子系统的接口通过 `__init__.py` 对外暴露，子系统只对外暴露接口和 container。
   - 其中 container 用于创建子系统内部元素，只能由 app 的 container 引用，用来创建和组装各个组件。
   - 典型的子系统 `__init__.py` 示例：
     ```python
     """
     chat 子系统职责：管理与用户的对话过程及对话历史，提供对话会话的创建、消息发送、历史查询等能力。
     """
     from .api.chat_service_api import ChatService
     from .container import Container

     __all__ = ["ChatService", "Container"]
     ```

4. **职责边界与唯一性**
   - 每个接口类应职责单一，避免接口方法职责重叠。
   - 如需扩展接口，应新建接口类并明确其边界，避免接口膨胀。
