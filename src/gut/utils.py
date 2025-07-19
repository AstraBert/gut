import subprocess as sp

from dataclasses import dataclass
from pydantic import BaseModel
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from xml.sax.saxutils import escape
from typing import Callable


@dataclass
class Shell:
    shell: bool = True
    capture_output: bool = True
    run_factory: Callable[..., sp.CompletedProcess] = sp.run

    def run(self, command: str) -> str:
        return self._process_output(
            self.run_factory(
                command, shell=self.shell, capture_output=self.capture_output
            )
        )

    def _process_output(self, output: sp.CompletedProcess):
        if output.returncode == 0:
            return str(output.stdout, encoding="utf-8")
        else:
            return "An error occurred:\n\n" + str(output.stderr, encoding="utf-8")


class XmlFormatter:
    def __init__(self):
        pass

    def to_xml(self, model: BaseModel):
        root_tag = model.__class__.__name__.lower()
        xml = ET.Element(root_tag)
        for k, v in model.model_dump().items():
            sub = ET.SubElement(xml, k.lower())
            safe_text = escape(str(v), entities={"'": "&apos;", '"': "&quot;"})
            sub.text = safe_text
        xml_str = ET.tostring(xml, encoding="unicode")
        return (
            parseString(xml_str).toprettyxml().replace('<?xml version="1.0" ?>\n', "")
        )
