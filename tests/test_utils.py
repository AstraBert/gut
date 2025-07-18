import pytest
import xml.etree.ElementTree as ET

from subprocess import CompletedProcess
from xml.dom.minidom import parseString
from pydantic import BaseModel
from src.gut.utils import Shell, XmlFormatter


def mock_run_factory(
    command: str, shell: bool, capture_output: bool
) -> CompletedProcess:
    if command != "git hello":
        return CompletedProcess(
            args=command, returncode=0, stdout=b"hello world", stderr=b""
        )
    return CompletedProcess(
        args=command, returncode=1, stdout=b"", stderr=b"Command is not allowed"
    )


@pytest.fixture
def xml_string_from_basemodel() -> str:
    model = ET.Element("person")
    age = ET.SubElement(model, "age")
    age.text = "30"
    name = ET.SubElement(model, "name")
    name.text = "John Doe"
    xml_str = ET.tostring(model, encoding="unicode")
    return parseString(xml_str).toprettyxml().replace('<?xml version="1.0" ?>\n', "")  # noqa: S318


@pytest.fixture
def starting_value() -> BaseModel:
    class Person(BaseModel):
        age: int
        name: str

    return Person(age=30, name="John Doe")


@pytest.fixture
def sh() -> Shell:
    return Shell(run_factory=mock_run_factory)


def test_shell(sh: Shell):
    assert sh.run("git --help") == "hello world"
    assert sh.run("gh repo") == "hello world"
    assert "An error occurred:\n\n" in sh.run("git hello")


def test_xml(xml_string_from_basemodel: str, starting_value: BaseModel):
    xml = XmlFormatter()
    assert xml.to_xml(starting_value) == xml_string_from_basemodel
