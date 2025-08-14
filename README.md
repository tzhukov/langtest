# LangEst - LangGraph Project

A LangGraph application for building stateful, multi-actor applications with LLMs.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -e .
   ```

3. For development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Copy the environment file and add your Groq API key:
   ```bash
   cp .env.example .env
   # Edit .env with your Groq API key from https://console.groq.com/keys
   ```

## Project Structure

```
langest/
├── src/
│   └── langest/
│       ├── __init__.py
│       ├── agents/
│       │   └── __init__.py
│       ├── graphs/
│       │   └── __init__.py
│       └── tools/
│           └── __init__.py
├── tests/
│   └── __init__.py
├── examples/
├── pyproject.toml
├── README.md
└── .env.example
```

## Usage

```python
from langest.graphs.simple_graph import create_simple_graph

# Create and run a simple graph
graph = create_simple_graph()
result = graph.invoke({"input": "Hello, world!"})
print(result)
```

## Development

Run tests:
```bash
pytest
```

Format code:
```bash
black src/ tests/
isort src/ tests/
```

Type checking:
```bash
mypy src/
```
