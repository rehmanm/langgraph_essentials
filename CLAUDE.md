# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A learning repository exploring LangGraph essentials — building stateful graph-based workflows using LangGraph with Google Gemini as the LLM provider.

## Setup

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows Git Bash
pip install -r requirements.txt
```

Requires a `.env` file with `GOOGLE_API_KEY` for the Gemini integration.

## Running Notebooks

Notebooks are the primary interface for experimenting with graphs. Run them in VS Code or Jupyter:

```bash
jupyter notebook
```

Each notebook imports its graph definition from `studio/`, uses `autoreload` for live reloading, and visualizes the graph with `graph.get_graph(xray=1).draw_mermaid_png()`.

## Architecture

- **`studio/`** — Graph definitions (the actual LangGraph `StateGraph` code). Each file defines a `State` TypedDict, node functions, and compiles a `graph` object. These are also registered in `studio/langgraph.json` for LangGraph Studio.
- **Root notebooks (`*.ipynb`)** — Import graphs from `studio/`, visualize them, and invoke them with test state.
- **`graph_helper.py`** — Monkey-patches `requests` to disable SSL verification for corporate proxy compatibility. Import this before any HTTP-using code if behind a corporate proxy.

## Key Patterns

- State is defined as a `TypedDict` with fields like `nList: List[str]`
- For accumulating state across parallel branches, use `Annotated[List[str], operator.add]` as the reducer
- Graphs are built with `StateGraph(State)`, nodes added via `add_node()`, edges via `add_edge()`, then compiled with `builder.compile()`
- LangGraph Studio config lives in `studio/langgraph.json` — update the `graphs` dict when adding new graph modules
