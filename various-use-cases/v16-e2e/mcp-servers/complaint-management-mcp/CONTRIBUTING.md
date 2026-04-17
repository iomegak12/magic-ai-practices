# Contributing to Complaint Management MCP Server

Thank you for your interest in contributing to the Complaint Management MCP Server! 🎉

---

## 👥 Team

**Core Developer:** Ramkumar  
**Team Members:** Chandini, Priya, Ashok

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Git
- Familiarity with FastMCP, SQLAlchemy, and Python

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd complaint-management-mcp
   ```

2. **Activate virtual environment**
   ```bash
   # From workspace root
   env\Scripts\activate  # Windows
   source env/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment**
   ```bash
   copy .env.example .env
   ```

5. **Run the server**
   ```bash
   python server.py
   ```

---

## 📋 How to Contribute

### 1. Find an Issue or Feature

- Check existing issues in the repository
- Discuss new features with the core team before implementing
- Look for issues tagged with `good first issue` for beginners

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 3. Make Changes

- Write clean, readable code
- Follow Python PEP 8 style guidelines
- Add docstrings to all functions and classes
- Update documentation if needed

### 4. Test Your Changes

```bash
# Run all tests
pytest tests/

# Test specific module
pytest tests/test_tools.py

# Check code style
flake8 src/
```

### 5. Commit Your Changes

Follow conventional commit format:
```bash
git commit -m "feat: add new search filter option"
git commit -m "fix: resolve database connection issue"
git commit -m "docs: update README with new examples"
```

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on the repository.

---

## 📝 Code Style Guidelines

### Python Style

- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use meaningful variable names

### Example:

```python
def validate_order_number(order_num: str) -> tuple[bool, str]:
    """
    Validate order number format.
    
    Args:
        order_num: Order number string to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    pattern = r'^ORD-\d{5,}$'
    if not re.match(pattern, order_num):
        return False, "Order number must match format ORD-XXXXX"
    return True, ""
```

### Docstrings

Use Google-style docstrings:

```python
def register_complaint(title: str, description: str, customer_name: str,
                      order_number: str, priority: str = "MEDIUM") -> dict:
    """
    Register a new customer complaint.
    
    Args:
        title: Complaint title (5-200 characters)
        description: Detailed complaint description
        customer_name: Name of the customer
        order_number: Order number (format: ORD-XXXXX)
        priority: Priority level (default: MEDIUM)
        
    Returns:
        Dictionary with success status and complaint data
        
    Raises:
        ValidationError: If input validation fails
        DatabaseError: If database operation fails
    """
    pass
```

---

## 🧪 Testing Requirements

### Unit Tests

- Write tests for all new functions
- Aim for 80%+ code coverage
- Use pytest fixtures for setup

### Integration Tests

- Test complete workflows
- Verify database operations
- Test error handling

### Test Structure

```python
import pytest
from src.tools.register import register_complaint

def test_register_complaint_success():
    """Test successful complaint registration."""
    result = register_complaint(
        title="Test complaint",
        description="This is a test description",
        customer_name="John Doe",
        order_number="ORD-10001"
    )
    assert result["success"] is True
    assert "complaint_id" in result

def test_register_complaint_invalid_order():
    """Test registration with invalid order number."""
    result = register_complaint(
        title="Test complaint",
        description="This is a test description",
        customer_name="John Doe",
        order_number="INVALID"
    )
    assert result["success"] is False
    assert result["error"]["code"] == "VALIDATION_ERROR"
```

---

## 📖 Documentation

### Update Documentation When:

- Adding new features
- Changing existing functionality
- Fixing bugs that affect behavior
- Adding new configuration options

### Documentation Files to Update:

- `README.md` - User-facing documentation
- `CHANGELOG.md` - Version history
- Docstrings - In-code documentation
- `docs/` folder - Technical documentation

---

## 🔍 Pull Request Process

### PR Checklist

Before submitting a PR, ensure:

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] Descriptive PR title and description
- [ ] Referenced related issues

### PR Review Process

1. **Submission** - Submit PR with clear description
2. **Automated Checks** - CI/CD runs tests
3. **Code Review** - Team reviews changes
4. **Feedback** - Address review comments
5. **Approval** - Core developer approves
6. **Merge** - Changes merged to main branch

---

## 🐛 Reporting Bugs

### Bug Report Template

```markdown
**Description:**
Brief description of the bug

**Steps to Reproduce:**
1. Step one
2. Step two
3. ...

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- OS: Windows/Linux/Mac
- Python version: 3.12.x
- FastMCP version: 2.10.6

**Additional Context:**
Any other relevant information
```

---

## 💡 Feature Requests

### Feature Request Template

```markdown
**Feature Description:**
Clear description of the proposed feature

**Use Case:**
Why is this feature needed?

**Proposed Solution:**
How would you implement this?

**Alternatives Considered:**
Other approaches you've thought about

**Additional Context:**
Mockups, examples, or references
```

---

## 🎯 Development Areas

### Areas for Contribution

1. **Core Features** - New MCP tools and capabilities
2. **Testing** - Expand test coverage
3. **Documentation** - Improve guides and examples
4. **Performance** - Optimize database queries
5. **Error Handling** - Better error messages
6. **Validation** - Enhanced input validation
7. **Logging** - Improved observability

---

## 📞 Communication

### Contact the Team

- **Issues** - Use GitHub issues for bug reports and feature requests
- **Discussions** - Use GitHub discussions for questions
- **Email** - Contact core team for urgent matters

### Response Times

- Bug reports: 1-2 business days
- Feature requests: 3-5 business days
- Pull requests: 2-3 business days

---

## 🏆 Recognition

Contributors will be acknowledged in:
- `CHANGELOG.md` for each release
- Project README
- Release notes

---

## 📜 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behaviors:**
- Being respectful and inclusive
- Providing constructive feedback
- Accepting constructive criticism gracefully
- Focusing on what is best for the community

**Unacceptable behaviors:**
- Harassment or discriminatory comments
- Trolling or insulting/derogatory comments
- Public or private harassment
- Publishing others' private information

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing! 🙏**

---

**Questions?** Contact Ramkumar or the team members: Chandini, Priya, Ashok
