from pydantic import BaseModel, Field
from typing import Literal


class ShellCommand(BaseModel):
    command: Literal["git", "gh"] = Field(
        description="Choose a command as the base for the execution, either git or gh"
    )


class GitCommand(BaseModel):
    subcommand: Literal[
        # Start a working area
        "clone",
        "init",
        # Work on the current change
        "add",
        "mv",
        "restore",
        "rm",
        # Examine the history and state
        "bisect",
        "diff",
        "grep",
        "log",
        "show",
        "status",
        # Grow, mark, and tweak your common history
        "backfill",
        "branch",
        "commit",
        "merge",
        "rebase",
        "reset",
        "switch",
        "tag",
        # Collaborate
        "fetch",
        "pull",
        "push",
    ] = Field(
        description="Subcommand to use",
    )
    options: str = Field(
        description="Options for the subcommand.",
        examples=["origin feature-branch", "-m 'commit message'"],
    )


class GhCommand(BaseModel):
    command: Literal[
        # Core Commands
        "auth",
        "browse",
        "codespace",
        "gist",
        "issue",
        "org",
        "pr",
        "project",
        "release",
        "repo",
        # GitHub Actions Commands
        "cache",
        "run",
        "workflow",
        # Alias Commands
        "co",
        # Additional Commands
        "alias",
        "api",
        "attestation",
        "completion",
        "config",
        "extension",
        "gpg-key",
        "label",
        "preview",
        "ruleset",
        "search",
        "secret",
        "ssh-key",
        "status",
        "variable",
    ]
    subcommand: str = Field(
        description="Subcommand for the main gh command",
        examples=["create", "checkout"],
    )
    options: str = Field(
        description="Options for the command and subcommand combination",
        examples=["--fill", "view", "archive"],
    )


class CommandToExecute(BaseModel):
    command: str = Field(
        description="Command to execute",
        examples=["git commit -m 'first commit'", "gh pr checkout 1937"],
    )
    explanation: str = Field(
        description="Detailed-but-concise explanation of why is the command being executed."
    )
