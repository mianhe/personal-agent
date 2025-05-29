from abc import ABC, abstractmethod


class CommandLineInterface(ABC):
    """
    命令行界面（CLI）接口，定义用户交互入口的标准方法。
    负责启动 CLI 交互流程，处理用户输入与系统命令。
    """

    @abstractmethod
    async def start(self) -> None:
        """
        启动 CLI 界面，进入主交互循环。
        前置条件：无
        后置条件：CLI 交互流程正常启动，直到用户主动退出。
        """
        pass
