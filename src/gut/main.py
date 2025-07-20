import asyncio

from rich.console import Console
from rich.table import Table
from .workflow import GutWorkflow
from .workflow.events import (
    MessageEvent,
    ProgressEvent,
    CommandExplanationEvent,
    HumanFeedbackEvent,
    ExecutedEvent,
)


async def run_workflow() -> int:
    wf = GutWorkflow(timeout=600, disable_validation=True)
    cs = Console()
    cs.print(
        "[bold cyan]>[/bold cyan] Welcome to gut - your assistant for everything related to [code]git[/code] and [code]gh[/code]! Before we start, let me ask you a question: are you ready to trust your guts on git? [Yes/No]"
    )
    guts = cs.input("[bold magenta]>[/bold magenta]")
    if guts.lower() == "yes":
        cs.print("[bold cyan]> Fantastic[/bold cyan], let's start!")
    else:
        cs.print("[bold cyan]>[/bold cyan] Well, then, see you next time!")
        return 0
    cs.print("[bold cyan]>[/bold cyan] So, what would you like me to do today?")
    user_message = cs.input("[bold magenta]>[/bold magenta]")
    handler = wf.run(start_event=MessageEvent(message=user_message))
    with cs.status("[bold green]Working on your request...") as status:
        async for event in handler.stream_events():
            if isinstance(event, ProgressEvent):
                cs.log(event.msg)
            elif isinstance(event, CommandExplanationEvent):
                cs.log("Here is the explanation of the command:")
                cs.log(event.explanation)
                cs.log("Should I go on with executing this command? [Yes/feedback]")
                status.stop()
                hitl = cs.input("[bold magenta]>[/bold magenta]")
                if hitl.strip().lower() == "yes":
                    handler.ctx.send_event(  # type: ignore[union-attr]
                        HumanFeedbackEvent(
                            approved=True,
                            feedback="",
                        )
                    )
                else:
                    handler.ctx.send_event(  # type: ignore[union-attr]
                        HumanFeedbackEvent(
                            approved=False,
                            feedback=hitl,
                        )
                    )
    result: ExecutedEvent = await handler
    error = "No Errors" if not result.is_error else "yes"
    output = "No Output Captured" if not result.output else result.output
    table = Table(show_footer=False)
    table.title = "Execution Details"
    table.add_column("Captured Output", justify="center")
    table.add_column("Errors", justify="center")
    table.add_row(
        output,
        error,
    )
    cs.print(table)
    return 0


def main():
    asyncio.run(run_workflow())
