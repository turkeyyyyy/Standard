# 🧪 JSON Agents Validator

Official Python validator for the [JSON Agents](https://jsonagents.org) (Portable Agent Manifest) specification.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-success.svg)](tests/)

## ✨ Features

✅ **JSON Schema Validation** — Validates manifests against the official specification  
🔗 **URI Validation** — Ensures `ajson://` URIs conform to RFC 3986  
📜 **Policy Expression Parsing** — Validates policy `where` clauses  
🎨 **Rich Error Messages** — Clear, actionable validation feedback  
🛠️ **CLI & Python API** — Use from command line or in your code  
📦 **Zero Config** — Works out of the box with bundled schemas  

---

## 🚀 Quick Start

### Install Dependencies

```bash
pip3 install jsonschema click rich requests pyyaml
```

Or from requirements.txt:
```bash
pip3 install -r requirements.txt
```

### Validate a Manifest

```python
from jsonagents import validate_manifest

result = validate_manifest("manifest.json")

if result.is_valid:
    print("✅ Manifest is valid!")
else:
    print("❌ Validation errors:")
    for error in result.errors:
        print(f"  • {error}")
```

### Command Line Usage

```bash
# Validate single file
python3 -m jsonagents.cli validate manifest.json

# Validate multiple files
python3 -m jsonagents.cli validate examples/*.json

# With verbose output
python3 -m jsonagents.cli validate manifest.json --verbose

# Strict mode (warnings as errors)
python3 -m jsonagents.cli validate manifest.json --strict

# Check a URI
python3 -m jsonagents.cli check-uri ajson://example.com/agents/hello

# Check policy expression
python3 -m jsonagents.cli check-policy "tool.type == 'http'"
```

---

## 📦 What's Included

### Core Modules

| Module | Purpose |
|--------|---------|
| `validator.py` | Main validator with JSON Schema validation |
| `uri.py` | `ajson://` URI validator (RFC 3986) |
| `policy.py` | Policy expression parser (Appendix B) |
| `cli.py` | Rich command-line interface |

### Test Suite

Comprehensive tests covering:
- ✅ Valid and invalid manifests
- ✅ URI syntax and semantics
- ✅ Policy expression grammar
- ✅ Edge cases and error handling

Run tests:
```bash
pytest
```

---

## 💡 Examples

### Validate Minimal Manifest

```json
{
  "manifest_version": "1.0",
  "agent": {
    "id": "ajson://example.com/agents/hello",
    "name": "Hello Agent",
    "version": "1.0.0"
  }
}
```

### Check URI Syntax

```python
from jsonagents.uri import URIValidator

validator = URIValidator()
result = validator.validate("ajson://example.com/agents/router")

if result.is_valid:
    print(f"Authority: {result.parsed['authority']}")
    print(f"Path: {result.parsed['path']}")
    print(f"HTTPS: {validator.to_https(result.uri)}")
```

### Validate Policy Expression

```python
from jsonagents.policy import PolicyValidator

validator = PolicyValidator()
result = validator.validate("tool.type == 'http' && tool.endpoint !~ 'external'")

if result.is_valid:
    print("✅ Valid policy expression")
else:
    for error in result.errors:
        print(f"❌ {error}")
```

---

## 🧪 Testing

### Manual Test

Test against Standard repo examples:

```bash
python3 test_manual.py
```

This validates all manifests in `../Standard/examples/`.

### Unit Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=jsonagents --cov-report=html

# Specific test file
pytest tests/test_validator.py -v
```

---

## 📚 Documentation

| Resource | Description |
|----------|-------------|
| [README.md](README.md) | This file - main documentation |
| [INSTALL.md](INSTALL.md) | Detailed installation and setup guide |
| [CHANGELOG.md](CHANGELOG.md) | Version history and changes |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute |
| [API Docs](jsonagents/) | Python API documentation |

---

## 🛠️ Development

### Setup

```bash
# Clone repository
git clone https://github.com/JSON-AGENTS/Validators.git
cd Validators/python

# Install dependencies
pip3 install -r requirements.txt
pip3 install pytest pytest-cov black ruff mypy

# Run tests
pytest
```

### Code Quality

```bash
# Format code
black jsonagents tests

# Lint
ruff check jsonagents tests

# Type check
mypy jsonagents
```

### Project Structure

```
jsonagents-validator/
├── jsonagents/              # Main package
│   ├── __init__.py         # Package exports
│   ├── validator.py        # Core validator
│   ├── uri.py             # URI validation
│   ├── policy.py          # Policy parser
│   ├── cli.py             # CLI interface
│   └── schemas/           # Bundled schemas
│       └── json-agents.json
├── tests/                  # Test suite
│   ├── test_validator.py
│   ├── test_uri.py
│   └── test_policy.py
├── pyproject.toml         # Package metadata
├── requirements.txt       # Dependencies
├── test_manual.py         # Manual test script
├── README.md
├── INSTALL.md
├── CHANGELOG.md
├── LICENSE
└── CONTRIBUTING.md
```

---

## 🎯 Validation Features

### JSON Schema Validation
- ✅ Required fields (manifest_version, profiles, etc.)
- ✅ Profile-specific requirements (core, exec, gov, graph)
- ✅ Data types and constraints
- ✅ Extension namespaces

### URI Validation
- ✅ RFC 3986 syntax compliance
- ✅ Valid authority (domain/host)
- ✅ Proper path structure
- ✅ Fragment identifiers
- ✅ HTTPS transformation

### Policy Expression Validation
- ✅ Grammar compliance (Appendix B)
- ✅ Operator usage (==, !=, ~, in, etc.)
- ✅ Variable references (tool.*, message.*, etc.)
- ✅ Logical expressions (&&, ||, not)
- ✅ Parentheses balancing

---

## 📋 Requirements

- Python 3.8+
- jsonschema >= 4.20.0
- click >= 8.1.0
- rich >= 13.0.0
- requests >= 2.31.0
- pyyaml >= 6.0

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:

- 🐛 Bug reports
- 💡 Feature requests
- 📝 Documentation improvements
- 🔧 Code contributions
- 🧪 Test additions

---

## 📜 License

Apache 2.0 — See [LICENSE](LICENSE) for details.

---

## 🔗 Resources

- [JSON Agents Specification](https://github.com/JSON-AGENTS/Standard)
- [Website](https://jsonagents.org)
- [Issue Tracker](https://github.com/JSON-AGENTS/Validators/issues)
- [Discussions](https://github.com/orgs/JSON-AGENTS/discussions)

---

## 🏆 Status

| Aspect | Status |
|--------|--------|
| **Core Validation** | ✅ Complete |
| **URI Validation** | ✅ Complete |
| **Policy Validation** | ✅ Complete |
| **CLI** | ✅ Complete |
| **Tests** | ✅ Comprehensive |
| **Documentation** | ✅ Complete |
| **PyPI Package** | 🔨 Coming Soon |

---

<div align="center">

**Built with ❤️ by the JSON Agents community**

[Specification](https://github.com/JSON-AGENTS/Standard) • [Documentation](https://jsonagents.org) • [Discussions](https://github.com/orgs/JSON-AGENTS/discussions)

</div>
