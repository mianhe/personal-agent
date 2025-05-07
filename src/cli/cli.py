import os
from typing import Dict, Callable


class CommandLineInterface:
    """Command Line Interface implementation for the personal agent."""

    def __init__(self):
        self.running = True
        self.cli_commands: Dict[str, Callable] = {
            "help": self._show_help,
            "exit": self._exit,
            "clear": self._clear_screen,
        }

    def start(self):
        """启动CLI界面"""
        self._show_welcome()
        while self.running:
            try:
                user_input = input("> ").strip()
                if not user_input:
                    continue
                self._process_input(user_input)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                self.running = False
            except Exception as e:
                print(f"Error: {str(e)}")
                self.running = False

    def _process_input(self, user_input: str) -> None:
        """处理用户输入"""
        if user_input.startswith("/"):
            self._handle_cli_command(user_input[1:])
        else:
            print(f"You said: {user_input}")

    def _show_welcome(self):
        """显示欢迎信息"""
        print("Welcome to Personal Agent CLI!")
        print("Type /help for available commands")

    def _handle_cli_command(self, command: str):
        """处理CLI命令"""
        cmd = command.lower()
        if cmd in self.cli_commands:
            self.cli_commands[cmd]()
            return  # 执行完命令后立即返回

        print(f"Unknown command: {command}")
        print("Available commands:")
        self._show_help()

    def _show_help(self):
        """显示帮助信息"""
        print("\nAvailable CLI commands:")
        for cmd in self.cli_commands:  # 直接迭代字典
            print(f"/{cmd}")

    def _exit(self):
        """退出程序"""
        print("Goodbye!")
        self.running = False

    def _clear_screen(self):
        """清屏"""
        os.system("cls" if os.name == "nt" else "clear")
        self._show_welcome()


def main():
    """程序入口点"""
    CommandLineInterface().start()


if __name__ == "__main__":
    main()
