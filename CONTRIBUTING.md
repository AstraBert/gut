# Contributing to `gut`

Do you want to contribute to this project? Make sure to read this guidelines first :)

## Issue

**When to do it**:

- You found bugs but you don't know how to solve them or don't have time/will to do the solve
- You want new features but you don't know how to implement them or don't have time/will to do the implementation

> ⚠️ _Always check open and closed issues before you submit yours to avoid duplicates_

**How to do it**:

- Open an issue
- Give the issue a meaningful title (short but effective problem/feature request description)
- Describe the problem/feature request

## Traditional contribution

**When to do it**:

- You found bugs and corrected them
- You optimized/improved the code
- You added new features that you think could be useful to others

**How to do it**:

1. Fork this repository
2. Install `pre-commit` and make sure to have it within the Git Hooks for your fork:

```bash
pip install pre-commit
pre-commit install
```

3. Change the things you want, and make sure tests still pass or add new ones:

```bash
pytest tests/test_*.py
```

3. Commit your changes
4. Make sure your changes pass the pre-commit linting/type checking, if not modify them so that they pass
5. Submit pull request (make sure to provide a thorough description of the changes)

### Thanks for contributing!
