from utils import Shell
from typing import Literal

sh = Shell()


def get_command_info(command: Literal["gh", "git"]) -> str:
    if command == "gh":
        return sh.run("gh help")
    else:
        return sh.run("git --help")


def get_subcommand_info(main_command: Literal["gh", "git"], subcommand: str) -> str:
    return sh.run(f"{main_command} {subcommand} --help")
