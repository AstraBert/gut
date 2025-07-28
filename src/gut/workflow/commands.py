import sys
import os
from workflows import Workflow, Context, step
from workflows.resource import Resource
from llama_index.core.llms import LLM, ChatMessage
from typing import Annotated, Union, Optional
from pydantic import BaseModel, Field

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from .events import (
    CommandMessageEvent,
    ProgressEvent,
    AnalyzeCommandEvent,
    HumanFeedbackEvent,
    ExecutedEvent,
)
from .resources import get_llm, get_shell, get_xml_formatter
from utils import Shell, XmlFormatter
from models import CommandAnalysis


class CommandAndQuestion(BaseModel):
    command: str = Field(default_factory=str)
    question: str = Field(default_factory=str)
    corrected_command: Optional[str] = Field(default=None, exclude=True)


class CommandWorkflow(Workflow):
    @step
    async def analyze_command(
        self,
        ctx: Context[CommandAndQuestion],
        ev: CommandMessageEvent,
        llm: Annotated[LLM, Resource(get_llm)],
        xml_formatter: Annotated[XmlFormatter, Resource(get_xml_formatter)],
    ) -> Union[AnalyzeCommandEvent, ExecutedEvent]:
        sllm = llm.as_structured_llm(CommandAnalysis)
        state = await ctx.store.get_state()
        state.command = ev.command
        if ev.message:
            state.question = ev.message
        else:
            state.question = "Can you help me understand this command better and, if the command is wrong, correct it?"
        await ctx.store.set_state(state)
        try:
            message_content = xml_formatter.to_xml(state)
        except Exception:
            message_content = state.model_dump_json(indent=4)
        messages = [ChatMessage(role="user", content=message_content)]
        response = await sllm.achat(messages)
        if response.message.content is not None:
            return_event = AnalyzeCommandEvent.model_validate_json(
                response.message.content
            )
            pg_msg = f"Explanation: {return_event.explanation}\n"
            if return_event.corrected_command:
                state = await ctx.store.get_state()
                state.corrected_command = return_event.corrected_command
                await ctx.store.set_state(state)
                pg_msg += (
                    f"Proposed Corrected Command: {return_event.corrected_command}\n"
                )
                pg_msg += "Do you want to execute the corrected command? [yes/feedback]"
                pg_ev = ProgressEvent(msg=pg_msg)
            else:
                pg_msg += "Do you want to execute your command? [yes/feedback]"
                pg_ev = ProgressEvent(msg=pg_msg)
            ctx.write_event_to_stream(pg_ev)
            return return_event
        return ExecutedEvent(
            is_error=True,
            output="It was impossible to analyze the command you provided",
        )

    @step
    async def execute_command(
        self,
        ev: HumanFeedbackEvent,
        ctx: Context[CommandAndQuestion],
        sh: Annotated[Shell, Resource(get_shell)],
    ) -> Union[CommandMessageEvent, ExecutedEvent]:
        state = await ctx.store.get_state()
        command = state.corrected_command or state.command
        if ev.approved:
            out = sh.run(command)
            return ExecutedEvent(output=out, is_error="An error occurred\n\n:" in out)
        else:
            message = f"My first instructions were: {state.question} and you generated: `{command}`. Now I am asking it to re-generate the command with this feedback: {ev.feedback}"
            ctx.write_event_to_stream(
                ProgressEvent(msg="Retrying execution based on human feedback")
            )
            return CommandMessageEvent(message=message, command=command)
