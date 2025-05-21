import os
from typing import Dict, Callable, Optional
from prompt_toolkit import PromptSession
from personal_agent.chat import ChatService


class CommandLineInterface:
    """Command Line Interface implementation for the personal agent."""

    def __init__(self, chat_service: Optional[ChatService] = None):
        self.running = True
        self.cli_commands: Dict[str, Callable] = {
            "help": self._show_help,
            "exit": self._exit,
            "clear": self._clear_screen,
            "server": self._server_command,  # 预留server命令
        }
        self.chat_service = chat_service()
        self.session = PromptSession()
        # self.server_registry = ServerRegistry()  # 具体实现后添加

    async def start(self):
        """启动CLI界面"""
        self._show_welcome()

        while self.running:
            try:
                user_input = (await self.session.prompt_async("> ")).strip()
                if not user_input:
                    continue
                await self._process_input(user_input)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                self.running = False
            except Exception as e:
                print(f"Error: {str(e)}")

    async def _process_input(self, user_input: str) -> None:
        """处理用户输入"""
        if self._is_cmd(user_input):
            self._handle_cli_command(user_input[1:])
        else:
            try:
                print("Thinking...", end="", flush=True)
                response = await self.chat_service.get_response(user_input)
                print("\b" * len("Thinking..."), end="", flush=True)  # 用退格键清除
                print(f"Assistant: {response}")
            except Exception as e:
                print(f"Error: {e}")

    def _is_cmd(self, user_input):
        return user_input.startswith("/")

    def _show_welcome(self):
        """显示欢迎信息"""
        print("Welcome to Personal Agent CLI!")
        print("Type /help for available commands")

    def _handle_cli_command(self, command: str):
        """处理CLI命令"""
        parts = command.strip().split()
        if not parts:
            print("No command entered.")
            return
        cmd = parts[0].lower()
        args = parts[1:]
        if cmd in self.cli_commands:
            self.cli_commands[cmd](*args)
            return  # 执行完命令后立即返回
        print(f"Unknown command: {command}")
        print("Available commands:")
        self._show_help()

    def _show_help(self):
        """显示帮助信息"""
        print("\nAvailable CLI commands:")
        for cmd in self.cli_commands:
            print(f"/{cmd}")
        print("\nServer management:")
        print("  /server add <name> <url> [description]   添加服务器")
        print("  /server list                           列出所有服务器")
        print("  /server remove <name>                  删除服务器")
        print("  /server info <name>                    查看服务器详情")
        print("  /server edit <name> <url> [desc]       编辑服务器")

    def _exit(self):
        """退出程序"""
        print("Goodbye!")
        self.running = False

    def _clear_screen(self):
        """清屏"""
        os.system("cls" if os.name == "nt" else "clear")
        self._show_welcome()

    def _server_command(self, *args):
        """
        服务器配置管理命令分发接口。
        支持子命令：add、list、remove、info、edit。
        这里只定义接口，不实现具体逻辑。
        """
        if not args:
            print("Usage: /server <add|list|remove|info|edit> ...")
            return
        subcmd = args[0].lower()
        if subcmd == "add":
            self._server_add(*args[1:])
        elif subcmd == "list":
            self._server_list()
        elif subcmd == "remove":
            self._server_remove(*args[1:])
        elif subcmd == "info":
            self._server_info(*args[1:])
        elif subcmd == "edit":
            self._server_edit(*args[1:])
        else:
            print(f"未知子命令: {subcmd}")
            print("用法: /server <add|list|remove|info|edit> ...")

    def _server_add(self, *args):
        """
        /server add <name> <url> [description]
        添加服务器。仅定义接口。
        """
        pass

    def _server_list(self):
        """
        /server list
        列出所有服务器。仅定义接口。
        """
        pass

    def _server_remove(self, *args):
        """
        /server remove <name>
        删除服务器。仅定义接口。
        """
        pass

    def _server_info(self, *args):
        """
        /server info <name>
        查看服务器详情。仅定义接口。
        """
        pass

    def _server_edit(self, *args):
        """
        /server edit <name> <url> [description]
        编辑服务器。仅定义接口。
        """
        pass
