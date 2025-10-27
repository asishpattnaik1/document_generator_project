# ReflectDoc - Quick Reference

> **5-minute guide to get started with ReflectDoc**

## Installation

```bash
cd reflectdoc
uv sync
cp .env.example .env
# Add OPENAI_API_KEY to .env
```

## Common Commands

### Analyze (No API Key Needed)
```bash
uv run reflectdoc analyze ./src
```

### Generate Documentation
```bash
# Basic generation
uv run reflectdoc generate ./src

# With specific type
uv run reflectdoc generate ./src --type architecture --output DOCS.md

# Fast mode (no reflection)
uv run reflectdoc generate ./src --no-reflection

# Preview in terminal
uv run reflectdoc generate ./src --show-content
```

## CLI Options Quick Reference

| Option | Short | Values | Description |
|--------|-------|--------|-------------|
| `--type` | `-t` | architecture/api/troubleshooting/full | Documentation type |
| `--output` | `-o` | filepath | Output file path |
| `--model` | `-m` | gpt-4-turbo-preview, gpt-3.5-turbo, o1-mini | OpenAI model |
| `--no-reflection` | - | flag | Skip reflection (faster) |
| `--no-diagrams` | - | flag | Skip Mermaid diagrams |
| `--show-content` | - | flag | Display in terminal |

## REST API Quick Start

```bash
# Start server
uv run uvicorn reflectdoc.api:app --reload --port 8000

# Visit interactive docs
open http://localhost:8000/docs
```

### Key Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Analyze
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"path": "./src"}'

# Generate
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"path": "./src", "doc_type": "architecture"}'
```

## Python API Quick Start

```python
from reflectdoc import generate_docs

response = generate_docs(
    repo_path="./src",
    doc_type="architecture",
    use_reflection=True,
    model="gpt-4-turbo-preview"
)

if response.success:
    print(f"✅ Docs saved to: {response.output_file}")
    print(response.documentation)
```

## Documentation Types

- **architecture** - System structure and design
- **api** - API endpoints and usage
- **troubleshooting** - Common issues and solutions
- **full** - Complete documentation suite

## Model Selection Guide

| Model | Speed | Quality | Cost | Best For |
|-------|-------|---------|------|----------|
| gpt-3.5-turbo | ⚡⚡⚡ | ⭐⭐ | $ | Quick drafts, testing |
| gpt-4-turbo-preview | ⚡⚡ | ⭐⭐⭐ | $$ | Production docs |
| o1-mini | ⚡⚡ | ⭐⭐⭐ | $$ | Technical accuracy |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "OPENAI_API_KEY not found" | Add key to `.env` file |
| Generation is slow | Use `--no-reflection` |
| Empty output | Try `gpt-4-turbo-preview` model |
| Port already in use | Use `--port 8001` |

## Useful Patterns

```bash
# Test what will be analyzed
uv run reflectdoc analyze ./src

# Quick draft
uv run reflectdoc generate ./src --no-reflection --output draft.md

# Production quality
uv run reflectdoc generate ./src --model gpt-4-turbo-preview --output final.md

# Different doc types
uv run reflectdoc generate ./src --type architecture --output arch.md
uv run reflectdoc generate ./src --type api --output api.md
uv run reflectdoc generate ./src --type troubleshooting --output trouble.md
```

## Next Steps

📖 **Full Documentation**: See [README.md](README.md) for comprehensive guide
🔧 **Configuration**: Check `.env.example` for all options
📚 **Examples**: Explore `examples/demo.py` for Python API usage
🌐 **API Docs**: Run server and visit http://localhost:8000/docs

---

*For detailed documentation, see [README.md](README.md)*
