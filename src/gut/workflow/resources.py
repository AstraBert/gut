import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from llama_index.llms.groq import Groq
from llama_index.core.llms import LLM
from utils import Shell, XmlFormatter
from dotenv import load_dotenv

load_dotenv()

llm = Groq(api_key=os.getenv("GROQ_API_KEY"), model="llama-3.3-70b-versatile")


def get_shell(*args, **kwargs) -> Shell:
    return Shell()


def get_xml_formatter(*args, **kwargs) -> XmlFormatter:
    return XmlFormatter()


def get_llm(*args, **kwargs) -> LLM:
    return llm
