import sys
import os
from workflows import Workflow, Context, step
from workflows.resource import Resource
from llama_index.core.llms import LLM, ChatMessage
from typing import Annotated, Union
from pydantic import BaseModel, Field

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import XmlFormatter, Shell
from models import ShellCommand, GitCommand, GhCommand, CommandToExecute
from .events import (
    MessageEvent,
    GitOrGhEvent,
    CommandConstructedEvent,
    CommandExplanationEvent,
    HumanFeedbackEvent,
    ExecutedEvent,
    ProgressEvent,
)
from shell import get_command_info, get_subcommand_info
from .resources import get_shell, get_xml_formatter, get_llm


class WorkflowState(BaseModel):
    user_message: str = Field(default_factory=str)
    main_command: str = Field(default_factory=str)
    command: str = Field(default_factory=str)
    subcommand: str = Field(default_factory=str)
    options: str = Field(default_factory=str)


class GutWorkflow(Workflow):
    @step
    async def choose_command(
        self,
        ev: MessageEvent,
        ctx: Context[WorkflowState],
        llm: Annotated[LLM, Resource(get_llm)],
    ) -> GitOrGhEvent:
        messages = [
            ChatMessage(content=ev.message, role="user"),
            ChatMessage(
                content="Based on my previous message, can you choose, between git and gh, what command would better suit my needs?",
                role="user",
            ),
        ]
        sllm = llm.as_structured_llm(ShellCommand)
        response = await sllm.achat(messages)
        output = ShellCommand.model_validate_json(response.message.content)
        state = await ctx.store.get_state()
        state.user_message = ev.message
        state.main_command = output.command
        await ctx.store.set_state(state)
        ctx.write_event_to_stream(
            ProgressEvent(msg=f"Main command chosen: {output.command}")
        )
        return GitOrGhEvent(
            main_command=output.command,
            command_information=get_command_info(output.command),
        )

    @step
    async def build_command(
        self,
        ev: GitOrGhEvent,
        ctx: Context[WorkflowState],
        llm: Annotated[LLM, Resource(get_llm)],
        formatter: Annotated[XmlFormatter, Resource(get_xml_formatter)],
    ) -> CommandConstructedEvent:
        class Command(BaseModel):
            main_command: str
            command_infomation: str
            user_instructions: str

        state = await ctx.store.get_state()
        mod = Command(
            main_command=ev.main_command,
            command_infomation=ev.command_information,
            user_instructions=state.user_message,
        )
        messages = [
            ChatMessage(
                content=f"Based on this model:\n\n{formatter.to_xml(mod)}\n\nCan you please output the necessary command/subcommand and options to fulfil the user's instructions?"
            )
        ]
        if ev.main_command == "gh":
            sllm = llm.as_structured_llm(GhCommand)
            response = await sllm.achat(messages)
            output = GhCommand.model_validate_json(response.message.content)
            state.command = output.command
            state.subcommand = output.subcommand
            state.options = output.options
        else:
            sllm = llm.as_structured_llm(GitCommand)
            response = await sllm.achat(messages)
            output = GitCommand.model_validate_json(response.message.content)
            state.command = output.subcommand
            state.options = output.options
        await ctx.store.set_state(state)
        ctx.write_event_to_stream(
            ProgressEvent(
                msg=f"Produced command: {state.main_command} {state.command} {state.subcommand} {state.options}"
            )
        )
        return CommandConstructedEvent(
            **output.model_dump(),
            info=get_subcommand_info(
                main_command=ev.main_command, subcommand=state.command
            ),
        )

    @step
    async def explain_command(
        self,
        ev: CommandConstructedEvent,
        ctx: Context[WorkflowState],
        llm: Annotated[LLM, Resource(get_llm)],
        formatter: Annotated[XmlFormatter, Resource(get_xml_formatter)],
    ) -> CommandExplanationEvent:
        state = await ctx.store.get_state()
        command = (
            state.main_command
            + " "
            + state.command
            + " "
            + state.subcommand
            + " "
            + state.options
        )
        command = command.strip()
        command = command.replace("  ", " ")

        class CommandToExplain(BaseModel):
            command: str
            info: str
            user_instructions: str

        mod = CommandToExplain(
            command=command, info=ev.info, user_instructions=state.user_message
        )
        try:
            messages = [
                ChatMessage(
                    content=f"Based on this model:\n\n{formatter.to_xml(mod)}\n\nCan you please explain the command and how it fulfils the user's instructions?"
                )
            ]
        except Exception:
            messages = [
                ChatMessage(
                    content=f"Based on this JSOn:\n\n```json\n{mod.model_dump_json(indent=4)}\n```\n\nCan you please explain the command and how it fulfils the user's instructions?"
                )
            ]
        sllm = llm.as_structured_llm(CommandToExecute)
        response = await sllm.achat(messages)
        output = CommandToExecute.model_validate_json(response.message.content)
        ctx.write_event_to_stream(
            ProgressEvent(msg=f"Explanation for the command: {output.explanation}")
        )
        return CommandExplanationEvent(command=command, explanation=output.explanation)

    @step
    async def execute_command(
        self,
        ev: HumanFeedbackEvent,
        ctx: Context[WorkflowState],
        sh: Annotated[Shell, Resource(get_shell)],
    ) -> Union[MessageEvent, ExecutedEvent]:
        state = await ctx.store.get_state()
        command = (
            state.main_command
            + " "
            + state.command
            + " "
            + state.subcommand
            + " "
            + state.options
        )
        command = command.strip()
        command = command.replace("  ", " ")
        if ev.approved:
            out = sh.run(command)
            return ExecutedEvent(output=out, is_error="An error occurred\n\n:" in out)
        else:
            message = f"My first instructions were: {state.user_message} and you generated: `{command}`. Now I am asking it to re-generate the command with this feedback: {ev.feedback}"
            ctx.write_event_to_stream(MessageEvent(message=message))
            return MessageEvent(message=message)
