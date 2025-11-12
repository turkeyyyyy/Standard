# JSON Agents Validators

Official validators for the [JSON Agents](https://jsonagents.org) specification.

---

## 📦 Available Validators

### Python Validator

**Location:** [`python/`](python/)  
**Language:** Python 3.8+  
**Status:** ✅ Production Ready (v1.0.0)

Comprehensive validator for JSON Agents manifests with:
- ✅ JSON Schema validation (JSON Schema 2020-12)
- ✅ URI validation (`ajson://` scheme per RFC 3986)
- ✅ Policy expression validation (Appendix B grammar)
- ✅ Rich CLI with colored output
- ✅ Python API for programmatic use

**Quick Start:**
```bash
cd python/
pip3 install -r requirements.txt
python3 -m jsonagents.cli validate ../../examples/*.json
```

**Documentation:**
- [README.md](python/README.md) - Main documentation
- [INSTALL.md](python/INSTALL.md) - Installation guide
- [PURPOSE.md](python/PURPOSE.md) - What validators are for
- [TEST-RESULTS.md](python/TEST-RESULTS.md) - Test coverage (47/47 passing)

---

## 🚀 Coming Soon

### JavaScript/TypeScript Validator
- Node.js and Deno support
- Integration with VS Code extension
- npm package

### Rust Validator
- High-performance validation
- WASM bindings for browser use
- Command-line tool

### Go Validator
- Native performance
- Minimal dependencies
- Container-friendly

---

## 🎯 Features Across All Validators

| Feature | Python | JS/TS | Rust | Go |
|---------|--------|-------|------|-----|
| JSON Schema Validation | ✅ | 🔜 | 🔜 | 🔜 |
| URI Validation | ✅ | 🔜 | 🔜 | 🔜 |
| Policy Expression Parser | ✅ | 🔜 | 🔜 | 🔜 |
| CLI Tool | ✅ | 🔜 | 🔜 | 🔜 |
| Library API | ✅ | 🔜 | 🔜 | 🔜 |
| Test Coverage | 100% | - | - | - |

---

## 📚 Documentation

- [JSON Agents Specification](../json-agents.md)
- [Examples](../examples/)
- [Schema Files](../schema/)
- [Registry](../registry/)

---

## 🤝 Contributing

We welcome validators in other languages! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

### Requirements for New Validators

1. ✅ **JSON Schema Validation** - Validate against official schema
2. ✅ **URI Validation** - Implement RFC 3986 compliant `ajson://` parser
3. ✅ **Policy Validation** - Parse and validate Appendix B expressions
4. ✅ **Test Coverage** - Minimum 80% code coverage
5. ✅ **Integration Tests** - Pass all examples from `../examples/`
6. ✅ **Documentation** - README, installation guide, API docs
7. ✅ **License** - Apache 2.0

---

## 📋 Validator Comparison

### Python
**Best For:** Python developers, data science, ML workflows  
**Pros:** Mature, well-tested, comprehensive CLI  
**Cons:** Slower than compiled languages

### JavaScript/TypeScript (Coming Soon)
**Best For:** Web developers, Node.js apps, browser validation  
**Pros:** Universal (runs anywhere), npm ecosystem  
**Cons:** Less strict typing than Rust/Go

### Rust (Coming Soon)
**Best For:** High-performance apps, WASM, system tools  
**Pros:** Fastest, memory-safe, WASM support  
**Cons:** Steeper learning curve

### Go (Coming Soon)
**Best For:** Cloud services, microservices, CLI tools  
**Pros:** Fast, simple, great for containers  
**Cons:** Less rich ecosystem than JS/Python

---

## 🔗 Resources

- [Specification](../json-agents.md)
- [Website](https://jsonagents.org)
- [Discussion Forum](https://github.com/orgs/JSON-AGENTS/discussions)
- [Issue Tracker](https://github.com/JSON-AGENTS/Standard/issues)

---

<div align="center">

**Building interoperable AI agents, one validator at a time** 🚀

[Specification](../json-agents.md) • [Examples](../examples/) • [Documentation](../docs/)

</div>
