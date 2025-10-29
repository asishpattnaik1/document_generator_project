# ReflectDoc - AI Documentation Generator with Reflection

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **A powerful, reflection-based documentation generator** that uses AI agents to create comprehensive documentation for your codebase with iterative quality improvement.

## 🌟 Overview

ReflectDoc is an intelligent documentation generator that follows the **Reflection Agent Pattern** from the neural-maze/agentic-patterns-course. It uses two specialized AI agents working together:

1. **Generator Agent** - Creates initial documentation drafts
2. **Reflection Agent** - Critiques and improves the documentation through multiple refinement iterations

This approach ensures high-quality, accurate, and comprehensive documentation that truly reflects your codebase.

## ✨ Key Features

- 🤖 **Dual AI Agent System**: Generator creates, Reflector improves
- 🔄 **Iterative Refinement**: Multiple rounds of self-reflection for quality
- 📊 **Multiple Documentation Types**: Architecture, API, Troubleshooting, or Full documentation
- 🎨 **Mermaid Diagrams**: Automatic generation of visual architecture diagrams
- 💻 **Dual Interface**: Both CLI and REST API for maximum flexibility
- ⚡ **Fast Mode**: Optional quick generation without reflection when speed matters
- 🔍 **Deep Code Analysis**: AST-based Python code parsing with detailed structure extraction
- ✅ **Accuracy Validation**: Validates documentation against actual code structure
- 📝 **Live Content Display**: View generated documentation in terminal with rich formatting
- 🎯 **IDE/CI Integration Ready**: Works in any environment
- ☁️ **Multi-Provider Support**: Works with both OpenAI and Azure OpenAI services
- 🔧 **Flexible Model Configuration**: Support for GPT-3.5, GPT-4, O1 series, and custom deployment names

## 🏗️ Architecture

### Core Components

```
reflectdoc/
├── src/reflectdoc/
│   ├── __init__.py          # Package initialization and exports
│   ├── core.py              # Main orchestrator coordinating agents
│   ├── cli.py               # Beautiful CLI interface with Rich
│   ├── api.py               # FastAPI REST API with Swagger docs
│   ├── llm_client.py        # LLM client factory (OpenAI/Azure)
│   ├── py.typed             # PEP 561 type hints marker
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── generator_agent.py    # Creates documentation drafts
│   │   └── reflection_agent.py   # Reviews and improves quality
│   ├── models/
│   │   └── __init__.py           # Pydantic models for type safety
│   └── utils/
│       └── __init__.py           # AST parsing, repo scanning utilities
├── examples/
│   ├── __init__.py
│   └── welcome_mailer/           # Sample project for testing
│       ├── __init__.py
│       ├── main.py
│       ├── user.py
│       ├── email_service.py
│       ├── config.py
│       └── docs/                 # Generated documentation samples
├── pyproject.toml           # Project dependencies and metadata
├── uv.lock                  # Locked dependency versions
├── .env                     # Environment configuration (API keys)
├── .python-version          # Python version specification
├── README.md                # This file
├── QUICKSTART.md            # Quick start guide
├── NOTES.md                 # Development notes
└── LESSONS_LEARNED.md       # Project insights and learnings
```

### Reflection Pattern Flow

```
1. Repository Input
   ↓
2. Deep Code Analysis (AST parsing with method signatures & attributes)
   ↓
3. Generator Agent (creates initial draft using actual code structure)
   ↓
4. Reflection Agent (critiques for accuracy, completeness, specificity)
   ↓
5. Generator Agent (improves based on critique)
   ↓
6. Reflection Agent (validates technical accuracy)
   ↓
7. Final Documentation Output (with live preview)
```

## 🚀 Quick Start

### Installation

```bash
# Navigate to the project
cd reflectdoc

# Install dependencies with uv
uv sync

# Configure OpenAI API Key
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=your-key-here
```

### Basic Usage

```bash
# Analyze repository structure (no API key needed)
uv run reflectdoc analyze ./src

# Generate architecture documentation
uv run reflectdoc generate ./src --type architecture --output DOCS.md

# Generate with content preview in terminal
uv run reflectdoc generate ./src --show-content

# Fast mode (no reflection, quicker results)
uv run reflectdoc generate ./src --no-reflection

# Use different OpenAI models
uv run reflectdoc generate ./src --model gpt-4-turbo-preview
uv run reflectdoc generate ./src --model gpt-3.5-turbo --no-reflection
```

## 📖 Comprehensive Usage Guide

### CLI Commands

#### 1. **Analyze Command** (No API Key Required)

Inspect your repository structure before generating documentation:

```bash
uv run reflectdoc analyze ./src

# Example output:
# 🔍 Analyzing Repository
# Repository: ./src
# Total Files: 12
# Total Lines: 2,450
# Language: python
# Modules: cli, core, api, agents, models, utils
# Dependencies: fastapi, openai, click, rich, pydantic...
```

#### 2. **Generate Command** (Requires OpenAI API Key)

Generate comprehensive documentation with various options:

```bash
# Full documentation with all features
uv run reflectdoc generate ./src

# Architecture documentation only
uv run reflectdoc generate ./src --type architecture --output ARCHITECTURE.md

# API documentation
uv run reflectdoc generate ./src --type api --output API_DOCS.md

# Troubleshooting guide
uv run reflectdoc generate ./src --type troubleshooting --output TROUBLESHOOTING.md

# Disable Mermaid diagrams
uv run reflectdoc generate ./src --no-diagrams

# Fast generation (skip reflection)
uv run reflectdoc generate ./src --no-reflection --output QUICK_DOCS.md

# Display content in terminal
uv run reflectdoc generate ./src --show-content

# Use specific OpenAI model
uv run reflectdoc generate ./src --model gpt-4-turbo-preview
uv run reflectdoc generate ./src --model o1-mini
```

**Available Options:**
- `--type, -t`: Documentation type (architecture/api/troubleshooting/full)
- `--output, -o`: Output file path
- `--no-diagrams`: Disable Mermaid diagram generation
- `--no-reflection`: Skip reflection agent (faster, lower quality)
- `--model, -m`: OpenAI model (gpt-4-turbo-preview, gpt-3.5-turbo, o1-mini, etc.)
- `--show-content`: Display generated content in terminal with rich formatting

#### 3. **Info Command**

Get information about ReflectDoc:

```bash
uv run reflectdoc info
```

### REST API Usage

#### Starting the API Server

```bash
# Method 1: Using uvicorn directly
uv run uvicorn reflectdoc.api:app --reload --port 8000

# Method 2: Background mode
uv run uvicorn reflectdoc.api:app --host 0.0.0.0 --port 8000 &
```

#### Interactive API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

#### API Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Get API information
curl http://localhost:8000/

# Analyze repository
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"path": "./src"}'

# Generate documentation with reflection
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "path": "./src",
    "doc_type": "architecture",
    "output_file": "API_DOCS.md",
    "include_diagrams": true,
    "use_reflection": true
  }'

# Fast generation (no reflection)
curl -X POST http://localhost:8000/generate/fast \
  -H "Content-Type: application/json" \
  -d '{
    "path": "./src",
    "doc_type": "full"
  }'
```

### Python API Usage

```python
from reflectdoc import generate_docs, DocumentationType

# Generate architecture documentation
response = generate_docs(
    repo_path="./src",
    doc_type="architecture",
    output_file="docs/architecture.md",
    include_diagrams=True,
    use_reflection=True,
    model="gpt-4-turbo-preview",
    max_iterations=2
)

if response.success:
    print(f"✅ Documentation saved to: {response.output_file}")
    print(f"📊 Analyzed {response.metadata['total_files_analyzed']} files")
    print(f"📏 Total lines: {response.metadata['total_lines']}")
    print(f"🔄 Reflection iterations: {response.metadata.get('total_iterations', 0)}")
    print(f"📝 Length: {len(response.documentation)} characters")
else:
    print(f"❌ Error: {response.error}")

# Fast generation without reflection
fast_response = generate_docs(
    repo_path="./src",
    doc_type="api",
    use_reflection=False,
    model="gpt-3.5-turbo"
)
```

## 📋 Documentation Types

| Type | Description | Best For | Includes |
|------|-------------|----------|----------|
| **architecture** | System architecture and design | Understanding system structure | Components, patterns, diagrams, data flow |
| **api** | API endpoints and usage | API consumers | Endpoints, request/response, authentication, errors |
| **troubleshooting** | Common issues and solutions | Support teams | Issue matrix, debug guide, FAQ |
| **full** | Complete documentation suite | Comprehensive reference | All of the above combined |

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Required - Choose one of the following:

# Option 1: OpenAI (Standard)
OPENAI_API_KEY=your-openai-api-key-here

# Option 2: Azure OpenAI
AZURE_OPENAI_API_KEY=your-azure-api-key-here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Optional
DEFAULT_MODEL=gpt-4-turbo-preview  # or your Azure deployment name
API_HOST=0.0.0.0
API_PORT=8000
```

### Azure OpenAI Setup

ReflectDoc fully supports Azure OpenAI services. To use Azure OpenAI:

1. **Create Azure OpenAI Resource** in the Azure Portal
2. **Deploy a Model** (e.g., gpt-4, gpt-35-turbo)
3. **Configure Environment Variables**:

```bash
# .env file
AZURE_OPENAI_API_KEY=your-azure-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

4. **Use with CLI**:

```bash
# The system automatically detects Azure configuration
uv run reflectdoc generate ./src --model your-deployment-name

# Or use the deployment name directly
uv run reflectdoc generate ./src --type architecture
```

**Note**: When using Azure OpenAI, the `--model` parameter should match your Azure deployment name, not the OpenAI model name.

### Supported OpenAI Models

- `gpt-4-turbo-preview` - Best quality, slower, more expensive
- `gpt-4` - High quality, balanced
- `gpt-3.5-turbo` - Fast, economical
- `o1-mini` - Optimized reasoning model
- Custom models - Any OpenAI-compatible model

## 🎯 Advanced Features

### 1. Detailed Code Structure Extraction

ReflectDoc performs deep AST analysis to extract:
- **Exact method signatures** with arguments and return types
- **Class attributes** with type annotations
- **Function definitions** with docstrings
- **Import dependencies** and module structure

This ensures documentation is grounded in actual code, preventing hallucinations.

### 2. Iterative Reflection Process

The Reflection Agent performs multiple validation passes:

1. **Accuracy Check**: Verifies all mentioned APIs exist in code
2. **Completeness Check**: Identifies missing coverage
3. **Specificity Check**: Flags generic descriptions
4. **Improvement Generation**: Creates enhanced version
5. **Final Validation**: Technical accuracy verification

### 3. Rich Terminal Output

View documentation directly in terminal with:
- Color-coded sections (green for generator, red for reflector)
- Formatted Markdown rendering
- Token usage tracking
- Progress indicators
- Panel displays with borders

### 4. Model Compatibility

Automatically handles different OpenAI model types:
- Older models (GPT-3.5, GPT-4) use `max_tokens`
- Newer models (GPT-5, O1 series) use `max_completion_tokens`
- Adaptive temperature settings per model

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.11+ | Modern Python features |
| **Dependency Manager** | uv | Fast, reliable dependency management |
| **CLI Framework** | Click + Rich | Beautiful command-line interface |
| **API Framework** | FastAPI + Uvicorn | High-performance REST API |
| **Data Validation** | Pydantic | Type-safe models |
| **LLM Integration** | OpenAI SDK | AI agent communication |
| **Code Analysis** | Python AST | Deep code structure parsing |

## 📊 What Makes ReflectDoc Different?

### Comparison with Traditional Doc Generators

| Feature | ReflectDoc | Traditional Tools |
|---------|------------|-------------------|
| AI-Powered | ✅ Dual agent system | ❌ Template-based |
| Self-Improvement | ✅ Reflection iterations | ❌ Single pass |
| Accuracy Validation | ✅ Against actual code | ⚠️ Limited |
| Natural Language | ✅ Human-readable docs | ⚠️ Technical only |
| Diagrams | ✅ Auto-generated Mermaid | ❌ Manual |
| Multiple Formats | ✅ Architecture/API/Troubleshooting | ⚠️ Single format |
| IDE Integration | ✅ CLI/API/Python | ⚠️ Limited |

## 🎓 Design Patterns Used

1. **Reflection Agent Pattern** - Generator creates, Reflector improves
2. **Factory Pattern** - Core module creates appropriate agents
3. **Strategy Pattern** - Different doc types use different strategies
4. **Repository Pattern** - Code analysis abstracted from generation
5. **Single Responsibility** - Each agent has one clear purpose

## 🔧 Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "OPENAI_API_KEY not found" | Missing API key | Create `.env` file with your key |
| "Model not found" | Invalid model name | Use `--model gpt-4-turbo-preview` or `gpt-3.5-turbo` |
| Generation is slow | Reflection enabled + large codebase | Use `--no-reflection` flag |
| Empty content generated | Wrong model or token limits | Try `gpt-4-turbo-preview` or `gpt-3.5-turbo` |
| Analysis includes .venv | No filtering | Run from `src/` folder or add filters |
| Port 8000 in use | Another service running | Use `--port 8001` |
| Mermaid diagram parse errors | Node labels too long | **Fixed in latest version** - diagrams now use short labels |

### Debug Mode

For verbose output:

```bash
# See detailed token usage and API calls
uv run reflectdoc generate ./src --show-content

# Check what will be analyzed
uv run reflectdoc analyze ./src
```

## 🎉 Recent Enhancements & Updates

### Version 0.1.1 - Latest Improvements

#### 🔧 Mermaid Diagram Fixes
**Problem**: Mermaid diagrams were generating parse errors due to long node labels with function signatures being wrapped across multiple lines.

**Solution**: 
- ✅ **Enhanced Generator Agent**: Now creates concise Mermaid diagrams with SHORT node labels (max 20 characters)
- ✅ **Updated Reflection Agent**: Validates diagram node lengths and suggests simpler alternatives
- ✅ **Better Examples**: Clear guidelines for GOOD vs BAD diagram patterns

**Before** (caused parse errors):
```mermaid
graph TD
  A[get_user_input() -> User] --> B[display_user_info(user) -> None]
```

**After** (clean and working):
```mermaid
graph TD
  A[User Input] --> B[Validation] 
  B --> C[Display Info]
```

#### 🎯 Improved Prompt Engineering
- **Generator Agent**: Enhanced prompts to create more accurate, grounded documentation
- **Reflection Agent**: Better critique format with specific validation rules
- **Accuracy Focus**: Explicit instructions to avoid hallucinations and verify against actual code

#### ☁️ Multi-Provider Support
- ✅ **OpenAI Support**: Standard OpenAI API with all GPT models
- ✅ **Azure OpenAI Support**: Full Azure OpenAI integration with custom deployments
- ✅ **Flexible Configuration**: Automatic provider detection from environment variables
- ✅ **Model Compatibility**: Handles both `max_tokens` and `max_completion_tokens` parameters

#### 🎨 Enhanced Code Analysis
- **Deep AST Parsing**: Extracts exact method signatures with type annotations
- **Attribute Detection**: Identifies class and instance attributes with types
- **Import Analysis**: Tracks dependencies and module relationships
- **Docstring Extraction**: Preserves existing documentation

#### 📊 Better Validation
- **Accuracy Checks**: Validates all mentioned APIs exist in actual code
- **Signature Verification**: Ensures method signatures match reality
- **Completeness Review**: Identifies missing important components
- **Specificity Enforcement**: Prevents generic descriptions

### Key Features Added in This Release

1. **Mermaid Diagram Robustness**: Fixed all parsing issues with automatic label shortening
2. **Azure OpenAI Integration**: Full support for Azure deployments and custom model names
3. **LLM Client Factory**: Centralized client management with automatic provider selection
4. **Enhanced Reflection**: More thorough critique with diagram validation
5. **Token Usage Tracking**: Detailed metrics for prompt and completion tokens
6. **Improved Error Handling**: Better error messages and validation feedback

### Technical Improvements

- **Modular Architecture**: Separated LLM client creation into factory pattern
- **Type Safety**: Enhanced Pydantic models for better validation
- **Code Quality**: Improved prompts to reduce hallucinations
- **Performance**: Optimized token usage and API calls
- **Maintainability**: Cleaner code structure with better separation of concerns

### Configuration Enhancements

**New LLM Client Factory** (`llm_client.py`):
```python
from reflectdoc.llm_client import LLMClientFactory, LLMProvider

# Automatic provider detection
client = LLMClientFactory.create_client(provider="auto", model="gpt-4")

# Explicit OpenAI
client = LLMClientFactory.create_client(provider="openai", model="gpt-4-turbo")

# Explicit Azure OpenAI
client = LLMClientFactory.create_client(provider="azure", model="my-deployment")
```

**Supported Environment Configurations**:
```bash
# OpenAI (Standard)
OPENAI_API_KEY=sk-...

# Azure OpenAI
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4-deployment
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### Breaking Changes

None! All changes are backward compatible. Existing configurations and usage patterns continue to work.

### Migration Guide

If you're upgrading from an earlier version:

1. **No changes required** - everything works as before
2. **Optional**: Add Azure OpenAI configuration if you want to use Azure
3. **Optional**: Update your `.env` file with new Azure variables
4. **Benefit**: Mermaid diagrams now work reliably without parse errors

### What's Next

See the [Roadmap](#-roadmap) section for planned features in upcoming releases.

## 📚 Examples

### Example 1: Document a Flask API

```bash
uv run reflectdoc generate ./my-flask-app \
  --type api \
  --output docs/API.md \
  --model gpt-4-turbo-preview
```

### Example 2: Quick Architecture Overview

```bash
uv run reflectdoc generate ./project \
  --type architecture \
  --no-reflection \
  --no-diagrams \
  --output QUICK_ARCH.md
```

### Example 3: Full Documentation Suite

```bash
uv run reflectdoc generate ./enterprise-app \
  --type full \
  --output COMPLETE_DOCS.md \
  --model gpt-4-turbo-preview
  # This will take longer but produce comprehensive docs
```

### Example 4: CI/CD Integration

```yaml
# .github/workflows/docs.yml
name: Generate Documentation
on: [push]
jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install uv
        run: pip install uv
      - name: Generate docs
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          cd reflectdoc
          uv sync
          uv run reflectdoc generate ./src --output docs/GENERATED.md
      - name: Commit docs
        run: |
          git config user.name github-actions
          git config user.email github-actions@github.com
          git add docs/GENERATED.md
          git commit -m "Auto-generate documentation" || exit 0
          git push
```

## 🚦 Best Practices

1. **Start with `analyze`** - Always check what will be processed first
2. **Use `--no-reflection` for testing** - Iterate quickly during development
3. **Enable reflection for production** - Get highest quality documentation
4. **Specify output paths** - Keep documentation organized
5. **Choose appropriate doc type** - Don't generate full docs if you only need API docs
6. **Use `--show-content`** - Preview before committing
7. **Version control your docs** - Track changes over time
8. **Update regularly** - Re-generate when code changes significantly

## 📈 Roadmap

### Current (v0.1.0)
- ✅ CLI interface with rich output
- ✅ REST API with OpenAPI docs
- ✅ Reflection agent pattern
- ✅ Multiple documentation types
- ✅ AST-based code analysis
- ✅ Mermaid diagram generation
- ✅ Type-safe with Pydantic

### Planned (v0.2.0)
- [ ] Multi-language support (JavaScript, TypeScript, Java)
- [ ] Repository filtering (exclude .venv, node_modules)
- [ ] Caching for repeated analysis
- [ ] WebSocket for real-time progress
- [ ] Database for async task tracking
- [ ] Rate limiting for API
- [ ] Authentication for API
- [ ] Docker container
- [ ] Unit tests with pytest
- [ ] Metrics and monitoring

## 🤝 Contributing

Contributions are welcome! This project follows modern Python best practices:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Inspired by the **neural-maze/agentic-patterns-course**
- Built with modern Python tools: uv, FastAPI, Click, Rich, Pydantic
- Powered by OpenAI's GPT models

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/asishpattnaik1/reflectdoc/issues)
- **Documentation**: This README and interactive API docs at `/docs`
- **Examples**: See `examples/` directory

---

**Made with ❤️ using the Reflection Agent Pattern**

*ReflectDoc - Because your code deserves documentation that reflects its true quality.*
