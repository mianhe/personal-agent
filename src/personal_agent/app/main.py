import asyncio
from personal_agent.app.container import AppContainer


def main():
    container = AppContainer()
    cli = container.cli_container().cli()
    asyncio.run(cli.start())


if __name__ == "__main__":
    main()
