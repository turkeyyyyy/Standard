# JSON Agents Validator - Setup Guide

## Quick Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/JSON-AGENTS/Validators.git
cd Validators/python

# Install dependencies
pip3 install -r requirements.txt

# Test it works
python3 test_manual.py
```

### For Development

```bash
# Install with dev dependencies
pip3 install -r requirements.txt
pip3 install pytest pytest-cov black ruff mypy

# Run tests
pytest

# Run with coverage
pytest --cov=jsonagents --cov-report=html
```

## Usage

### Python API

```python
from jsonagents import validate_manifest

# Validate a manifest file
result = validate_manifest("manifest.json")

if result.is_valid:
    print("✅ Valid!")
else:
    for error in result.errors:
        print(f"❌ {error}")
```

### Command Line (after pip install)

```bash
# Validate a file
python3 -m jsonagents.cli validate manifest.json

# Validate multiple files
python3 -m jsonagents.cli validate examples/*.json

# Check a URI
python3 -m jsonagents.cli check-uri ajson://example.com/agents/hello

# Check a policy expression
python3 -m jsonagents.cli check-policy "tool.type == 'http'"
```

## Testing with Standard Repo Examples

```bash
# Run the manual test script
python3 test_manual.py
```

This will validate all example manifests from the ../Standard/examples/ directory.

## Package Structure

```
jsonagents-validator/
├── jsonagents/
│   ├── __init__.py           # Package exports
│   ├── validator.py          # Core validator
│   ├── uri.py               # URI validation
│   ├── policy.py            # Policy expression parser
│   ├── cli.py               # Command-line interface
│   └── schemas/
│       └── json-agents.json  # Bundled schema
├── tests/
│   ├── test_validator.py
│   ├── test_uri.py
│   └── test_policy.py
├── pyproject.toml           # Package configuration
├── requirements.txt         # Dependencies
├── README.md
├── CHANGELOG.md
├── LICENSE
└── CONTRIBUTING.md
```

## Dependencies

- `jsonschema>=4.20.0` — JSON Schema validation
- `requests>=2.31.0` — HTTP requests (future: remote schema fetching)
- `click>=8.1.0` — CLI framework
- `rich>=13.0.0` — Rich terminal output
- `pyyaml>=6.0` — YAML support (future feature)

## Next Steps

1. Install dependencies: `pip3 install -r requirements.txt`
2. Run manual test: `python3 test_manual.py`
3. Try examples: `python3 -m jsonagents.cli validate ../Standard/examples/core.json`
4. Run test suite: `pytest` (requires `pip3 install pytest`)

## Publishing to PyPI

Once ready:

```bash
# Build package
python3 -m build

# Upload to PyPI
python3 -m twine upload dist/*
```

Then users can install with:
```bash
pip install jsonagents
```
