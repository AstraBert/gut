from src.gut.workflow import GutWorkflow
from workflows import Workflow


def test_workflow_simple() -> None:
    wf = GutWorkflow(timeout=600)
    assert isinstance(wf, Workflow)
    assert wf._timeout == 600
