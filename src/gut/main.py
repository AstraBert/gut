import asyncio

from rich.console import Console
from rich.columns import Columns
from .workflow import GutWorkflow
from .workflow.events import (
    MessageEvent,
    GitOrGhEvent,
    CommandConstructedEvent,
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
    with cs.status("[bold green]Working on your request...") as _:
        mc = ""
        async for event in handler.stream_events():
            if isinstance(event, MessageEvent):
                cs.log(
                    f"Starting the workflow with the following instructions from the user: {event.message}"
                )
            elif isinstance(event, GitOrGhEvent):
                mc = event.main_command
                cs.log(f"Your problem requires {event.main_command}")
                cs.log(f"Collected information about {event.main_command}")
            elif isinstance(event, CommandConstructedEvent):
                command = (
                    mc + " " + event.command
                    if event.command
                    else "" + " " + event.subcommand
                    if event.subcommand
                    else "" + " " + event.options
                )
                command = command.strip()
                command = command.replace("  ", " ")
                cs.log(f"Constructed your command: {command}")
            elif isinstance(event, CommandExplanationEvent):
                cs.log("Here is the explanation of the command:")
                cs.log(event.explanation)
                cs.log("Should I go on with executing this command? [Yes/feedback]")
                hitl = cs.input("[bold magenta]>[/bold magenta]")
                if hitl.strip().lower() == "yes":
                    handler.ctx.send_event(
                        HumanFeedbackEvent(
                            approved=True,
                            feedback="",
                        )
                    )
                else:
                    handler.ctx.send_event(
                        HumanFeedbackEvent(
                            approved=False,
                            feedback=hitl,
                        )
                    )
    result: ExecutedEvent = await handler
    error = "no" if not result.is_error else "yes"
    columns = [f"Errors: {error}", f"Output: {result.output}"]
    cs.print("[bold cyan]>[/bold cyan] Execution status:")
    cs.print(Columns(columns))
    return 0


def main():
    asyncio.run(run_workflow())
