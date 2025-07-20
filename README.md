# gut

## Trust your guts on git🫀

**gut** is an AI-powered CLI tool that executes all the `git`/`gh` commands you want from natural language queries.

### Set-up and Execution

**User settings**

**gut** is available as a python package, and cna be easily installed with:

```bash
pip install gut
```

You then just need to set `GROQ_API_KEY` as an environment variable, either exporting it on the console or in a `.env` file in the root folder where you are executing **gut**, and then you can simply launch it via:

```bash
gut
```

**Developer settings**

You can clone this repository:

```bash
git clone https://github.com/AstraBert/gut
cd gut/
```

And then install the needed dependencies with [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

You then just need to set `GROQ_API_KEY` as an environment variable, either exporting it on the console or in a `.env` file in the root folder where you are executing **gut**, and then you can simply launch it via:

```bash
uvx --from . gut
```

### How Does It Work?

**gut** leverages an AI-powered workflow (designed with [llama-index-workflows](https://github.com/run-llama/workflows-py)), whose steps are:

- Choose the main command to execute between `git` and `gh` based on the user's requirements
- Choose the command/subcommand and options to employ with the main command (e.g. `add .` for `git` if the user asked to add local changes to git)
- Produce an explanation for the command
- Expose the command and the explanation to the user, asking fot their feedback (human-in-the-loop or HITL approach).
- If the feedback is positive, the command gets executed, otherwise the workflow restarts from the beginning, re-using the initial instructions and the feedback that the user provided.

The whole workflow runs in a [Rich](hhttps://github.com/Textualize/rich) console and leverages structured inputs (through XML/JSON representations of Pydantic models) and outputs.

### Contributing

Contributions are always welcome - make sure to read the [contributions guide](CONTRIBUTING.md) before submitting yours!

### License

This project is provided under an [MIT License](./LICENSE).
