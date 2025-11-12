# Changelog

All notable changes to the JSON Agents validator will be documented in this file.

This project adheres to [Semantic Versioning 2.0.0](https://semver.org/).

---

## [1.0.0] — 2025-11-11
**Initial Release**

### Added
- Core validator with JSON Schema 2020-12 validation
- URI validator for `ajson://` scheme (RFC 3986 compliant)
- Policy expression parser and validator (Appendix B)
- CLI tool with rich output formatting
- Python API for programmatic validation
- Comprehensive test suite
- Documentation and examples

### Features
- Validates manifests against official JSON Agents schema
- Checks URI syntax and semantics
- Parses and validates policy `where` clauses
- Helpful error messages with context
- Strict mode (treat warnings as errors)
- JSON output format for CI/CD integration
- Batch validation of multiple files

---

## Future Releases

### [1.1.0] — Planned
- Auto-downloading of schemas from jsonagents.org
- Caching of remote schemas
- Schema version compatibility checking
- Enhanced policy expression suggestions
- IDE language server protocol (LSP) support

### [2.0.0] — Planned
- Support for custom validation rules
- Plugin system for extensions
- Performance optimizations for large manifests
- Graph validation (cyclic dependency detection)
- Advanced security auditing
