# Contributing to JSON Agents Validator

Thank you for your interest in contributing! We welcome contributions of all kinds.

## Ways to Contribute

- 🐛 **Bug Reports**: File issues for bugs you find
- 💡 **Feature Requests**: Suggest new features or improvements
- 📝 **Documentation**: Improve docs, add examples, fix typos
- 🔧 **Code**: Submit pull requests for bug fixes or features
- 🧪 **Tests**: Add or improve test coverage

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/JSON-AGENTS/Validators.git
   cd Validators/python
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in development mode**:
   ```bash
   pip install -e ".[dev]"
   ```

4. **Run tests**:
   ```bash
   pytest
   ```

## Code Style

We use:
- **Black** for formatting
- **Ruff** for linting
- **MyPy** for type checking

Run before committing:
```bash
black jsonagents tests
ruff check jsonagents tests
mypy jsonagents
```

## Testing

- Write tests for all new features
- Maintain test coverage above 80%
- Run full test suite before submitting PR

```bash
pytest --cov=jsonagents --cov-report=html
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Add tests
5. Run linting and tests
6. Commit with clear messages
7. Push to your fork
8. Open a pull request

## Commit Messages

Use clear, descriptive commit messages:

```
feat: add support for YAML manifest validation
fix: correct URI validation for localhost
docs: update README with new examples
test: add tests for policy validator edge cases
```

## Questions?

- Open a [GitHub Discussion](https://github.com/JSON-AGENTS/Validators/discussions)
- Email: spec@jsonagents.org

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://github.com/JSON-AGENTS/Standard/blob/main/CODE_OF_CONDUCT.md).
