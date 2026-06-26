# Git Analyzer

Simple CLI tool to analyze a git repository and produce basic statistics.

Usage:

```bash
python main.py --repo /path/to/repo [--since YYYY-MM-DD] [--until YYYY-MM-DD]
```

Reports:
- total commits
- top contributors
- most changed files
- average commit message length

## Running Tests

```bash
python -m unittest discover -s tests -v
```

Tests are automatically run via GitHub Actions on every push and pull request.
