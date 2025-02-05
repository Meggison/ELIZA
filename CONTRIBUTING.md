# Contributing to Modern ELIZA

Thank you for your interest in contributing to the Modern ELIZA project! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/yourusername/ELIZA.git
cd ELIZA
```

3. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all public functions and classes
- Keep functions focused and single-purpose
- Use meaningful variable names

## Testing

1. Write tests for new features
2. Ensure all tests pass before submitting:
```bash
python -m pytest tests/
```

## Pull Request Process

1. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes
3. Update documentation if needed
4. Run tests
5. Commit your changes:
```bash
git add .
git commit -m "Description of changes"
```

6. Push to your fork:
```bash
git push origin feature/your-feature-name
```

7. Create a Pull Request

## Adding New Features

### New Response Patterns

1. Open `eliza/core/response_patterns.py`
2. Add your pattern following the existing format
3. Add appropriate tests in `tests/`
4. Update documentation if needed

### Web Interface Changes

1. Modify files in `eliza/web/`
2. Test thoroughly in different browsers
3. Ensure mobile responsiveness
4. Update documentation if needed

## Documentation

- Update README.md for user-facing changes
- Update docstrings for code changes
- Create/update API documentation as needed
- Include examples for new features

## Questions?

Feel free to open an issue for any questions or concerns.
