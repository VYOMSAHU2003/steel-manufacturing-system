# 🤝 Contributing to Steel Manufacturing Plant Management System

Thank you for your interest in contributing to our project! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Feature Requests](#feature-requests)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

### Our Pledge

- **Be Respectful**: Treat everyone with respect and kindness
- **Be Collaborative**: Work together towards common goals
- **Be Inclusive**: Welcome newcomers and help them succeed
- **Be Professional**: Maintain professional communication

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- VS Code (recommended) with Python extension
- Basic understanding of Streamlit, SQLAlchemy, and Python web development

### Development Setup

1. **Fork the Repository**
   ```bash
   # Fork the repo on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/steel-manufacturing-system.git
   cd steel-manufacturing-system
   ```

2. **Set Up Development Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Install development dependencies
   pip install -r requirements-dev.txt  # If exists
   ```

3. **Initialize Database**
   ```bash
   python scripts/init_db.py
   ```

4. **Verify Setup**
   ```bash
   streamlit run app.py
   ```

## 🔄 Development Workflow

### Branch Naming Convention

Use descriptive branch names following this pattern:
- `feature/description` - for new features
- `bugfix/description` - for bug fixes
- `docs/description` - for documentation updates
- `refactor/description` - for code refactoring
- `test/description` - for adding tests

### Workflow Steps

1. **Create a New Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Write clean, documented code
   - Follow our coding standards
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Your Changes**
   ```bash
   # Run the application
   streamlit run app.py
   
   # Test all modules thoroughly
   # Verify database operations work correctly
   ```

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "✨ Add your descriptive commit message"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   # Then create a pull request on GitHub
   ```

## 📏 Coding Standards

### Python Style Guide

- **Follow PEP 8**: Use Python's official style guide
- **Line Length**: Maximum 100 characters
- **Imports**: Group imports (standard library, third-party, local)
- **Docstrings**: Use Google-style docstrings

### Example Code Style

```python
"""
Module for handling raw materials operations.

This module provides functions for managing raw material inventory,
including adding new materials, updating quantities, and tracking usage.
"""

import logging
from datetime import datetime
from typing import List, Optional

import streamlit as st
import pandas as pd
from sqlalchemy.orm import Session

from config.database import get_db_session
from models.database_models import RawMaterial


def add_raw_material(
    name: str,
    category: str,
    quantity: float,
    unit: str,
    quality_grade: str,
    batch_number: str,
    db: Session
) -> Optional[RawMaterial]:
    """
    Add a new raw material to the inventory.
    
    Args:
        name: Name of the raw material
        category: Material category (e.g., 'Iron Ore', 'Coal')
        quantity: Quantity in stock
        unit: Unit of measurement (e.g., 'tons', 'kg')
        quality_grade: Quality classification
        batch_number: Unique batch identifier
        db: Database session
        
    Returns:
        RawMaterial: Created material object or None if failed
        
    Raises:
        ValueError: If required parameters are invalid
    """
    try:
        # Validation
        if not all([name, category, quantity, unit, quality_grade, batch_number]):
            raise ValueError("All parameters are required")
            
        # Create new material
        material = RawMaterial(
            name=name,
            category=category,
            quantity=quantity,
            unit=unit,
            quality_grade=quality_grade,
            batch_number=batch_number,
            status='available',
            created_at=datetime.now()
        )
        
        db.add(material)
        db.commit()
        db.refresh(material)
        
        logging.info(f"Added new material: {name} (Batch: {batch_number})")
        return material
        
    except Exception as e:
        db.rollback()
        logging.error(f"Failed to add material {name}: {str(e)}")
        st.error(f"Error adding material: {str(e)}")
        return None
```

### Streamlit Best Practices

- **Use Session State**: For maintaining state across interactions
- **Cache Functions**: Use `@st.cache_data` for expensive operations
- **Error Handling**: Always include try-catch blocks with user-friendly messages
- **Responsive Design**: Test on different screen sizes

### Database Guidelines

- **Use Transactions**: Wrap database operations in transactions
- **Handle Rollbacks**: Always rollback on errors
- **Optimize Queries**: Use appropriate indexes and query optimization
- **Connection Management**: Properly close database connections

## 🧪 Testing Guidelines

### Manual Testing Checklist

Before submitting a PR, test the following scenarios:

#### Authentication
- [ ] Login with valid credentials
- [ ] Login with invalid credentials
- [ ] Role-based access control
- [ ] Session timeout handling

#### Raw Materials Module
- [ ] Add new material
- [ ] Update existing material
- [ ] View inventory list
- [ ] Check analytics charts
- [ ] Verify transaction logs

#### Production Planning
- [ ] Create new production order
- [ ] Update order status
- [ ] Assign operators
- [ ] View production timeline

#### Quality Assurance
- [ ] Create quality inspection
- [ ] Enter test measurements
- [ ] Generate quality reports
- [ ] View quality metrics

#### Database Operations
- [ ] Test with SQLite (development)
- [ ] Test Oracle connection if available
- [ ] Verify data persistence
- [ ] Check for SQL injection vulnerabilities

### Test Data

Use the provided test data or create realistic sample data:

```python
# Example test material
test_material = {
    'name': 'High-Grade Iron Ore',
    'category': 'Iron Ore',
    'quantity': 500.0,
    'unit': 'tons',
    'quality_grade': 'Premium',
    'batch_number': 'IO-2024-001',
    'supplier': 'ABC Mining Co.',
    'cost_per_unit': 120.50
}
```

## 📬 Pull Request Process

### Before Submitting

1. **Self-Review**: Review your own code changes
2. **Test Thoroughly**: Ensure all functionality works as expected
3. **Update Documentation**: Update README, docstrings, and comments
4. **Check Dependencies**: Ensure no unnecessary dependencies are added

### PR Template

Use this template for your pull request:

```markdown
## 📝 Description
Brief description of changes and motivation.

## 🎯 Type of Change
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work)
- [ ] Documentation update

## ✅ Testing
- [ ] Manual testing completed
- [ ] All modules tested
- [ ] Database operations verified
- [ ] No errors in console

## 📷 Screenshots (if applicable)
Add screenshots to demonstrate UI changes.

## 📋 Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
```

### Review Process

1. **Automatic Checks**: GitHub Actions (if configured)
2. **Code Review**: At least one maintainer review required
3. **Testing**: Reviewer will test the changes
4. **Approval**: Changes must be approved before merging

## 🐛 Issue Reporting

### Before Creating an Issue

1. **Search Existing Issues**: Check if the issue already exists
2. **Use Latest Version**: Ensure you're using the latest version
3. **Check Documentation**: Review documentation and troubleshooting

### Bug Report Template

```markdown
## 🐛 Bug Report

### Description
A clear description of what the bug is.

### Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

### Expected Behavior
What you expected to happen.

### Actual Behavior
What actually happened.

### Environment
- OS: [e.g., Windows 10, macOS 11.0, Ubuntu 20.04]
- Python Version: [e.g., 3.9.7]
- Streamlit Version: [e.g., 1.28.1]
- Database: [SQLite/Oracle]

### Screenshots
If applicable, add screenshots.

### Additional Context
Any other context about the problem.
```

## 💡 Feature Requests

### Feature Request Template

```markdown
## 🚀 Feature Request

### Is your feature request related to a problem?
A clear description of what the problem is.

### Describe the solution you'd like
A clear description of what you want to happen.

### Describe alternatives you've considered
A clear description of alternative solutions.

### Additional context
Any other context or screenshots about the feature request.

### Implementation Ideas
If you have ideas on how to implement this feature.
```

## 🏷️ Commit Message Convention

Use conventional commits for better changelog generation:

- `✨ feat:` New feature
- `🐛 fix:` Bug fix
- `📚 docs:` Documentation changes
- `♻️ refactor:` Code refactoring
- `⚡ perf:` Performance improvements
- `✅ test:` Adding tests
- `🔧 chore:` Maintenance tasks

Example:
```bash
git commit -m "✨ feat: Add real-time inventory tracking dashboard"
git commit -m "🐛 fix: Resolve login session timeout issue"
git commit -m "📚 docs: Update API documentation for quality module"
```

## 📞 Getting Help

- **GitHub Discussions**: For questions and general discussion
- **GitHub Issues**: For bug reports and feature requests
- **Code Review**: Tag maintainers for code review help

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Annual contributor appreciation

---

Thank you for contributing to the Steel Manufacturing Plant Management System! 🏭✨