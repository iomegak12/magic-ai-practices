# Contributing to MSAv15Service

Thank you for your interest in contributing to MSAv15Service! This document provides guidelines for development and contribution.

## 👥 Team

- **Product Manager**: Ramkumar (Ram)
- **Development Team (CAP)**:
  - Chandini
  - Ashok
  - Priya

## 🔄 Development Workflow

### 1. Setup Development Environment

```bash
# Clone repository
git clone <repository-url>
cd v15-e2e-casestudy/api-service

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials
```

### 2. Branch Strategy

- `main` - Production-ready code
- `develop` - Development branch
- `feature/<name>` - Feature branches
- `bugfix/<name>` - Bug fix branches

### 3. Making Changes

1. Create a feature branch from `develop`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following our coding standards

3. Write or update tests for your changes

4. Update documentation if needed

5. Commit with clear, descriptive messages:
   ```bash
   git commit -m "feat: add new order filtering capability"
   ```

### 4. Commit Message Format

Follow the Conventional Commits specification:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Test additions or changes
- `chore:` - Build process or auxiliary tool changes

### 5. Pull Request Process

1. Update CHANGELOG.md with your changes
2. Ensure all tests pass
3. Update README.md if adding new features
4. Create PR against `develop` branch
5. Request review from team members
6. Address review feedback
7. Merge after approval

## 🎨 Code Standards

### Python Style Guide

- Follow PEP 8 guidelines
- Use type hints for function parameters and return values
- Maximum line length: 100 characters
- Use docstrings for all classes and functions

**Example:**

```python
def create_order(
    customer_name: str,
    product_sku: str,
    quantity: int
) -> Order:
    """
    Create a new customer order.
    
    Args:
        customer_name: Full name of the customer
        product_sku: Product SKU code
        quantity: Order quantity (must be > 0)
        
    Returns:
        Created Order object
        
    Raises:
        ValidationException: If input validation fails
    """
    # Implementation
```

### Project-Specific Guidelines

1. **Tool Functions**: All MAF tools must return strings (not objects)
2. **Error Handling**: Use try-except blocks and return user-friendly messages
3. **Logging**: Use print statements for important events (to be replaced with proper logging)
4. **Configuration**: All configurable values must be in `.env` or `config.py`

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_health.py -v
```

### Writing Tests

- Place tests in `tests/` directory
- Name test files with `test_` prefix
- Use descriptive test function names
- Cover both success and failure cases

**Example:**

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check_returns_200():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_chat_requires_message():
    response = client.post("/chat", json={})
    assert response.status_code == 422  # Validation error
```

## 📝 Documentation

### Code Documentation

- Add docstrings to all public functions and classes
- Keep inline comments concise and meaningful
- Update API documentation when endpoints change

### User Documentation

- Update README.md for user-facing changes
- Add examples for new features
- Keep configuration documentation current

## 🐛 Bug Reports

When reporting bugs, include:

1. **Description**: Clear description of the issue
2. **Steps to Reproduce**: Detailed steps to recreate the bug
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**: OS, Python version, Docker version
6. **Logs**: Relevant log output

## 💡 Feature Requests

For feature requests, provide:

1. **Use Case**: Why is this feature needed?
2. **Proposed Solution**: How should it work?
3. **Alternatives**: Other approaches considered
4. **Impact**: Who benefits from this feature?

## 🔒 Security

- Never commit sensitive credentials (API keys, passwords)
- Use `.env` files for secrets (excluded from git)
- Report security vulnerabilities privately to the team

## 📦 Dependencies

- Keep dependencies up to date
- Document reasons for new dependencies
- Check for security vulnerabilities regularly

## ⚡ Performance

- Profile code for performance bottlenecks
- Optimize database queries
- Consider caching strategies
- Monitor memory usage for session management

## 🎯 Code Review Checklist

Before requesting review, ensure:

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated
- [ ] No sensitive data in commits
- [ ] Error handling is comprehensive
- [ ] Type hints are present
- [ ] Functions have docstrings

## 📞 Communication

- Use GitHub issues for bug tracking
- Use PRs for code discussions
- Tag team members for urgent issues
- Keep commit history clean and meaningful

## 🎓 Resources

- [Microsoft Agent Framework Docs](https://microsoft.github.io/agent-framework/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

---

Thank you for contributing to MSAv15Service! 🚀
