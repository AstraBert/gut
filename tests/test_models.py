import pytest
from pydantic import ValidationError

from src.gut.models import (
    ShellCommand,
    GhCommand,
    GitCommand,
    CommandToExecute,
    CommandAnalysis,
)


def test_shell_command():
    sh = ShellCommand(command="git")
    assert sh.command == "git"
    with pytest.raises(ValidationError):
        ShellCommand(comment="gut")


def test_gh_command():
    gh = GhCommand(command="pr", subcommand="checkout", options="1997")
    assert gh.command == "pr"
    assert gh.subcommand == "checkout"
    assert gh.options == "1997"
    with pytest.raises(ValidationError):
        GhCommand(command="hello", subcommand="world", options="--fix")


def test_git_command():
    gitcmd = GitCommand(subcommand="commit", options="-m 'first' commit")
    assert gitcmd.subcommand == "commit"
    assert gitcmd.options == "-m 'first' commit"
    with pytest.raises(ValidationError):
        GitCommand(subcommand="hello", options="--fix")


def test_final_command():
    cmd = CommandToExecute(
        command="git commit -m 'first commit'", explanation="This is a commit command."
    )
    assert cmd.command == "git commit -m 'first commit'"
    assert cmd.explanation == "This is a commit command."
    with pytest.raises(ValidationError):
        CommandToExecute(command=1, explanation="This is a wrong command.")


def test_command_analysis():
    cmd = CommandAnalysis(explanation="Explanation")
    assert cmd.explanation == "Explanation"
    assert cmd.corrected_command is None
    cmd = CommandAnalysis(
        explanation="Explanation", corrected_command="git commit -m 'first commit'"
    )
    assert cmd.corrected_command == "git commit -m 'first commit'"
    with pytest.raises(ValidationError):
        CommandAnalysis(explanation="Explanation", corrected_command=False)
