# Contributing to Biomedical Data Platform

## Development Setup

```bash
pip install -r requirements.txt
pip install pytest pytest-cov black ruff
```

## Code Style

- **Formatting**: Black
- **Linting**: Ruff
- **Type hints**: Preferred for public APIs

## Testing

```bash
pytest tests/ -v --cov=src
```

## Pull Request Process

1. Fork and create a feature branch
2. Add tests for new functionality
3. Run `black` and `ruff` before pushing
4. Open a PR with a clear description

## Documentation

- Update `docs/` for architecture or pipeline changes
- Keep `README.md` in sync with new features
