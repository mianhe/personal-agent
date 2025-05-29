import asyncio
from personal_agent.app import Container
from personal_agent.cli import CommandLineInterface


def main():
    container = Container()
    cli: CommandLineInterface = container.cli_container().cli()
    asyncio.run(cli.start())


if __name__ == "__main__":
    main()
