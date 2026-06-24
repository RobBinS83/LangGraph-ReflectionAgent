# ReflectAgent

A LangChain/LangGraph-based multi-agent system that iteratively improves written content (emails, articles, posts) through a generate-then-reflect loop.

## How It Works

The workflow follows a two-node cycle:

```
START → GENERATE → REFLECT → (if APPROVED or >20 messages) → END
                   ↓
            (if not approved)
                   ↓
              GENERATE (again)
```

1. **Generator** — an expert writer LLM produces or revises the content based on the input and any prior feedback.
2. **Reflector** — a strict editor LLM critiques the output, identifying missing information, logical flaws, or stylistic issues, and generates concrete recommendations.
3. The loop repeats until the reflector responds with exactly `APPROVED` or 20 messages have accumulated (safety cap).

A Mermaid workflow diagram is auto-generated as `flow.png` on every run.

## Project Structure

```
ReflectAgent/
├── main.py          # LangGraph workflow: state, nodes, edges, entry point
├── chains.py        # LLM prompt templates and chain definitions
├── pyproject.toml   # Project metadata and dependencies (uv)
├── uv.lock          # Locked dependency versions
├── flow.png         # Auto-generated workflow diagram
└── .env             # API keys and LangChain tracing config (not committed)
```

## Setup

**Requirements:** Python 3.13+, [uv](https://github.com/astral-sh/uv)

```bash
# Clone and enter the project
git clone <repo-url>
cd ReflectAgent

# Create virtual environment and install dependencies
uv sync

# Copy and fill in your API keys
cp .env.example .env
```

### Environment Variables

Create a `.env` file with the following:

```env
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key

# Optional: LangSmith tracing
LANGCHAIN_TRACING=true
LANGCHAIN_API_KEY=your_langchain_key
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_PROJECT=Reflection-Agent
```

## Running

```bash
python main.py
```

The default input in `main.py` is a Verizon HR leadership announcement email. Edit the `HumanMessage` in `main()` to use your own content.

## Tech Stack

| Library | Purpose |
|---|---|
| `langgraph` | Agentic workflow graph (nodes, edges, state) |
| `langchain` | LLM chain composition and prompt templates |
| `langchain-openai` | OpenAI model integration |
| `langchain-google-genai` | Google Gemini model integration |
| `python-dotenv` | `.env` file loading |

## Configuration

LLM models and temperatures are defined in `chains.py`:

- **Generator** — `ChatOpenAI`, temperature `0.5`
- **Reflector** — `ChatOpenAI`, temperature `0.3` (lower = more deterministic critique)

A `ChatGoogleGenerativeAI` instance (`llm2`) is also initialized for optional use.
