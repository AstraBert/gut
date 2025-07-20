from src.gut.workflow import GutWorkflow
from src.gut.workflow.events import ExecutedEvent
from workflows import Workflow


def test_workflow_simple() -> None:
    wf = GutWorkflow(timeout=600)
    assert isinstance(wf, Workflow)
    assert wf._timeout == 600


def test_executed_event() -> None:
    ev = ExecutedEvent(output="An error occurred:\n\nError")
    assert ev.is_error
    ev = ExecutedEvent(output="A correct output", is_error=True)
    assert not ev.is_error
