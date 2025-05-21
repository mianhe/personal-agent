import asyncio
from .container import AppContainer


def run_cli():
    """运行 CLI 界面。"""
    container = AppContainer()
    cli = container.cli_bot()
    asyncio.run(cli.start())


def main():
    run_cli()


if __name__ == "__main__":
    main()
