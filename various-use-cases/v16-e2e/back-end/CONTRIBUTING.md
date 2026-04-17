# Contributing to MSEv15E2E

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

1. Fork the repository
2. Clone your fork
3. Create a virtual environment
4. Install dependencies including dev tools:
   ```bash
   pip install -r requirements.txt
   ```

## Code Style

- **Python**: Follow PEP 8 guidelines
- **Formatting**: Use Black formatter (line length: 88)
- **Linting**: Pass Flake8 checks
- **Type Hints**: Use type hints for all functions
- **Docstrings**: Use Google-style docstrings

### Running Code Quality Tools

```bash
# Format code
black app/ tests/

# Check linting
flake8 app/ tests/

# Type checking
mypy app/

# All checks
black app/ tests/ && flake8 app/ tests/ && mypy app/
```

## Commit Guidelines

Follow conventional commits format:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Example:
```
feat: add streaming chat endpoint
fix: resolve session cleanup issue
docs: update API documentation
```

## Branch Naming

- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `hotfix/description` - Critical fixes
- `docs/description` - Documentation updates

## Testing Requirements

All contributions must include tests:

- **Unit Tests**: For individual functions/classes
- **Integration Tests**: For API endpoints
- **Coverage**: Maintain >80% code coverage

```bash
# Run tests
pytest

# Check coverage
pytest --cov=app --cov-report=html
```

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes with appropriate tests
3. Ensure all tests pass
4. Update documentation if needed
5. Submit PR with clear description
6. Address review feedback

### PR Checklist

- [ ] Code follows style guidelines
- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
- [ ] Commit messages follow conventions
- [ ] Branch is up-to-date with main

## Code Review

All code goes through review process:

- At least one approval required
- CI checks must pass
- No merge conflicts
- Documentation complete

## Reporting Issues

When reporting issues, include:

- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Relevant logs/error messages

## Questions?

Contact the development team:
- Ramkumar
- Rahul

Or reach out to Product Manager: Hemanth Shah

---

Thank you for contributing! 🎉
