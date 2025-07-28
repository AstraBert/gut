import pytest

from pydantic import ValidationError
from src.gut.workflow import GutWorkflow, CommandWorkflow
from src.gut.workflow.events import (
    ExecutedEvent,
    CommandMessageEvent,
    AnalyzeCommandEvent,
)
from workflows import Workflow


def test_gut_workflow_simple() -> None:
    wf = GutWorkflow(timeout=600)
    assert isinstance(wf, Workflow)
    assert wf._timeout == 600


def test_command_workflow_simple() -> None:
    wf = CommandWorkflow(timeout=600)
    assert isinstance(wf, Workflow)
    assert wf._timeout == 600


def test_command_message_event() -> None:
    ev = CommandMessageEvent(message="message", command="git push origin main")
    assert ev.message == "message"
    assert ev.command == "git push origin main"
    with pytest.raises(ValidationError):
        CommandMessageEvent(message="message", command="echo 'gut is awesome'")


def test_analyze_command_event() -> None:
    ev = AnalyzeCommandEvent(explanation="explanation")
    assert ev.corrected_command is None


def test_executed_event() -> None:
    ev = ExecutedEvent(output="An error occurred:\n\nError")
    assert ev.is_error
    ev = ExecutedEvent(output="A correct output", is_error=True)
    assert not ev.is_error
