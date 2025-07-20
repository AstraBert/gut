# gut 🫀

**Trust your guts on git** — An AI-powered CLI tool that executes `git` and `gh` commands from natural language queries.

Transform commands like "add all my changes and commit with a meaningful message" into the exact git commands you need, with AI-powered intelligence and human-in-the-loop validation.

## ✨ Features

- 🤖 **Natural Language Processing**: Describe what you want to do in plain English
- 🔄 **Human-in-the-Loop**: Review and approve commands before execution
- 🎯 **Smart Command Selection**: Automatically chooses between `git` and `gh` commands
- 📖 **Command Explanation**: Get clear explanations of what each command does
- 🎨 **Rich Console Interface**: Beautiful terminal experience with syntax highlighting

## 🚀 Quick Start

### Installation

Install gut using pip:

```bash
pip install gut-ai
```

### Setup

1. Get a [Groq API key](https://console.groq.com/keys)
2. Set your API key as an environment variable:

```bash
export GROQ_API_KEY="your_api_key_here"
```

Or create a `.env` file in your project directory:

```
GROQ_API_KEY=your_api_key_here
```

### Usage

Simply run gut and describe what you want to do:

```bash
gut-ai
```

Example interactions:

- "Add all my current changes to git"
- "Create a new branch called feature/login"
- "Push my changes to origin"
- "Create a pull request"

## 🔧 Development Setup

### Prerequisites

- [uv](https://docs.astral.sh/uv/) package manager

### Clone and Install

```bash
git clone https://github.com/AstraBert/gut
cd gut/
uv sync
```

### Run from Source

```bash
uvx --from . gut-ai
```

## 🛠️ How It Works

gut uses an AI-powered workflow built with [llama-index-workflows](https://github.com/run-llama/workflows-py) that follows these steps:

1. **Command Analysis**: Analyzes your natural language input to understand intent
2. **Command Selection**: Chooses between `git` and `gh` based on your requirements
3. **Parameter Mapping**: Determines the specific subcommands and options needed
4. **Explanation Generation**: Creates a clear explanation of what the command will do
5. **Human Validation**: Shows you the command and explanation for approval
6. **Execution**: Runs the command if approved, or restarts the process with your feedback

The entire experience runs in a beautiful [Rich](https://github.com/Textualize/rich) console interface with structured inputs and outputs using Pydantic models.

## 📋 Requirements

- **Groq API Key**: Required for AI functionality
- **Git**: Must be installed and configured
- **GitHub CLI (optional)**: Required only for GitHub-related commands (`gh`)

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guide](CONTRIBUTING.md) to get started.

## 📄 License

This project is licensed under the [MIT License](./LICENSE).

## 🙋‍♀️ Support

- 🐛 **Bug Reports**: [Open an issue](https://github.com/AstraBert/gut/issues)
- 💡 **Feature Requests**: [Start a discussion](https://github.com/AstraBert/gut/discussions)
- 📧 **Questions**: Check existing [issues](https://github.com/AstraBert/gut/issues) and [discussions](https://github.com/AstraBert/gut/discussions)

---

_Made with ❤️ for developers who want to git things done faster_
