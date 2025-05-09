import asyncio
from core.cli_initialization import create_chat_service
from .cli import CommandLineInterface


def run_cli():
    """运行 CLI 界面。"""
    chat_service = create_chat_service()
    cli = CommandLineInterface(chat_service)
    asyncio.run(cli.start())


def main():
    run_cli()


if __name__ == "__main__":
    main()
