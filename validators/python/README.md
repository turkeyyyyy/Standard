# JSON Agents Validator

[![PyPI version](https://img.shields.io/pypi/v/jsonagents.svg)](https://pypi.org/project/jsonagents/)
[![Python versions](https://img.shields.io/pypi/pyversions/jsonagents.svg)](https://pypi.org/project/jsonagents/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)

# 🧪 JSON Agents Validator

Official Python validator for the [JSON Agents](https://jsonagents.org) (Portable Agent Manifest) specification.

## Features

- ✅ **JSON Schema Validation** — Validates manifests against the official JSON Agents schema
- 🔗 **URI Validation** — Ensures `ajson://` URIs conform to RFC 3986
- 📜 **Policy Expression Parsing** — Validates policy `where` clauses
- 🎨 **Rich Error Messages** — Clear, actionable validation feedback
- 🛠️ **CLI & Python API** — Use from command line or in your code
- 📦 **Zero Config** — Works out of the box

## Installation

```bash
pip install jsonagents
```

For development:
```bash
pip install jsonagents[dev]
```

## Quick Start

### Command Line

Validate a manifest file:
```bash
jsonagents validate manifest.json
```

Validate with verbose output:
```bash
jsonagents validate manifest.json --verbose
```

Validate multiple files:
```bash
jsonagents validate examples/*.json
```

### Python API

```python
from jsonagents import validate_manifest

# Validate a manifest
result = validate_manifest("manifest.json")

if result.is_valid:
    print("✅ Manifest is valid!")
else:
    print("❌ Validation errors:")
    for error in result.errors:
        print(f"  - {error}")
```

Advanced usage:
```python
from jsonagents import Validator

# Create validator instance
validator = Validator()

# Validate from dict
manifest = {
    "manifest_version": "1.0",
    "agent": {
        "id": "ajson://example.com/agents/hello",
        "name": "Hello Agent"
    }
}

result = validator.validate(manifest)
print(f"Valid: {result.is_valid}")
print(f"Errors: {result.errors}")
print(f"Warnings: {result.warnings}")
```

## Validation Features

### JSON Schema Validation
Validates against the official JSON Agents schema:
- Required fields (manifest_version, profiles, etc.)
- Profile-specific requirements (core, exec, gov, graph)
- Data types and constraints
- Extension namespaces

### URI Validation
Checks `ajson://` URIs for:
- RFC 3986 syntax compliance
- Valid authority (domain/host)
- Proper path structure
- Fragment identifiers

### Policy Expression Validation
Parses and validates policy `where` clauses:
- Grammar compliance (Appendix B)
- Operator usage (==, !=, ~, in, etc.)
- Variable references (tool.*, message.*, etc.)
- Logical expressions (&&, ||, not)

## CLI Usage

```bash
# Basic validation
jsonagents validate manifest.json

# Verbose output
jsonagents validate manifest.json -v

# Validate directory
jsonagents validate examples/

# Output as JSON
jsonagents validate manifest.json --json

# Strict mode (warnings as errors)
jsonagents validate manifest.json --strict

# Check specific profile
jsonagents validate manifest.json --profile exec
```

## Examples

### Valid Minimal Manifest
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

### Common Validation Errors

**Missing required field:**
```
❌ ValidationError: Missing required field 'manifest_version'
   → Add "manifest_version": "1.0" at the top level
```

**Invalid URI:**
```
❌ URIError: Invalid ajson:// URI syntax
   → Expected: ajson://authority/path
   → Got: ajson:example.com/agent
```

**Invalid policy expression:**
```
❌ PolicyError: Invalid operator in where clause
   → Line 1: tool.type === 'http'
   → Use '==' instead of '==='
```

## Development

### Setup
```bash
git clone https://github.com/JSON-AGENTS/Validators.git
cd Validators/python
pip install -e ".[dev]"
```

### Run Tests
```bash
pytest
```

### Run with Coverage
```bash
pytest --cov=jsonagents --cov-report=html
```

### Lint and Format
```bash
black jsonagents tests
ruff check jsonagents tests
mypy jsonagents
```

## API Reference

### `validate_manifest(path_or_dict, strict=False)`
Validate a manifest from file path or dictionary.

**Parameters:**
- `path_or_dict` (str | dict): Path to manifest file or manifest dictionary
- `strict` (bool): Treat warnings as errors

**Returns:** `ValidationResult`

### `Validator`
Main validator class.

**Methods:**
- `validate(manifest: dict) -> ValidationResult`
- `validate_uri(uri: str) -> URIValidationResult`
- `validate_policy(expression: str) -> PolicyValidationResult`

### `ValidationResult`
Result object from validation.

**Attributes:**
- `is_valid` (bool): Whether validation passed
- `errors` (list[str]): Validation errors
- `warnings` (list[str]): Non-critical issues
- `manifest` (dict): The validated manifest

## Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Apache 2.0 — See [LICENSE](LICENSE) for details.

## Resources

- [JSON Agents Specification](https://github.com/JSON-AGENTS/Standard)
- [Documentation](https://jsonagents.org)
- [Issue Tracker](https://github.com/JSON-AGENTS/Validators/issues)
- [PyPI Package](https://pypi.org/project/jsonagents/)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.
