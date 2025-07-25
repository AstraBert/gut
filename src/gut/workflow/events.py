from workflows.events import (
    StartEvent,
    Event,
    InputRequiredEvent,
    HumanResponseEvent,
    StopEvent,
)
from pydantic import Field, model_validator
from typing import Optional
from typing_extensions import Self


class MessageEvent(StartEvent):
    message: str


class ProgressEvent(Event):
    msg: str


class GitOrGhEvent(Event):
    main_command: str
    command_information: str


class CommandConstructedEvent(Event):
    command: Optional[str] = Field(default=None)
    subcommand: str
    options: str
    info: str


class CommandExplanationEvent(InputRequiredEvent):
    command: str
    explanation: str


class HumanFeedbackEvent(HumanResponseEvent):
    approved: bool
    feedback: str


class ExecutedEvent(StopEvent):
    is_error: Optional[bool] = Field(default=None)
    output: str

    @model_validator(mode="after")
    def validate_error(self) -> Self:
        if "An error occurred:\n\n" in self.output and not self.is_error:
            self.is_error = True
        elif "An error occurred:\n\n" not in self.output and self.is_error:
            self.is_error = False
        return self
