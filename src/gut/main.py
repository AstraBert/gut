import asyncio
from argparse import ArgumentParser

from pydantic import ValidationError
from rich.console import Console
from rich.table import Table
from .workflow import GutWorkflow, CommandWorkflow
from .workflow.events import (
    MessageEvent,
    ProgressEvent,
    CommandExplanationEvent,
    HumanFeedbackEvent,
    ExecutedEvent,
    CommandMessageEvent,
)
from ._banner import _show_banner

cs = Console()


async def run_commands_workflow(start_event: CommandMessageEvent) -> int:
    wf = CommandWorkflow(timeout=600, disable_validation=True)
    cs.print(
        "[bold cyan]>[/bold cyan] Welcome to gut - your assistant for everything related to [code]git[/code] and [code]gh[/code]! I'll start analyzing your command shortly..."
    )
    handler = wf.run(start_event=start_event)
    with cs.status("[bold green]Working on your request...") as status:
        async for event in handler.stream_events():
            if isinstance(event, ProgressEvent):
                cs.log(event.msg)
                if event.msg.endswith("[yes/feedback]"):
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


async def run_gut_workflow() -> int:
    wf = GutWorkflow(timeout=600, disable_validation=True)
    cs.print(
        "[bold cyan]>[/bold cyan] Welcome to gut - your assistant for everything related to [code]git[/code] and [code]gh[/code]! Before we start, let me ask you a question: are you ready to trust your gut on git? [Yes/No]"
    )
    guts = cs.input("[bold magenta]>[/bold magenta]")
    if guts.lower() == "yes":
        cs.print("[bold cyan]> Fantastic[/bold cyan], let's start!")
    else:
        cs.print("[bold cyan]>[/bold cyan] Well, then, see you next time!")
        return 0
    while True:
        cs.print(
            "[bold cyan]>[/bold cyan] So, what would you like me to do now? (Use q to quit)"
        )
        user_message = cs.input("[bold magenta]>[/bold magenta]")
        if user_message == "q":
            return 0
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


async def run_workflow() -> int:
    parser = ArgumentParser()
    parser.add_argument(
        "-c",
        "--command",
        type=str,
        help="Command to be executed",
        required=False,
        default=None,
    )
    parser.add_argument(
        "-q",
        "--question",
        type=str,
        help="Question about the command",
        required=False,
        default=None,
    )
    args = parser.parse_args()
    _show_banner()
    if not args.command and not args.question:
        return await run_gut_workflow()
    else:
        try:
            start_event = CommandMessageEvent(
                message=args.question, command=args.command
            )
            return await run_commands_workflow(start_event=start_event)
        except ValidationError as e:
            cs.print(f"[bold red]ERROR:[/bold red]\n{str(e)}")
            return 1


def main():
    asyncio.run(run_workflow())
