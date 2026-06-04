# Git Analyzer

Simple CLI tool to analyze a git repository and produce basic statistics.

Usage:

```bash
python main.py --repo /path/to/repo [--since YYYY-MM-DD] [--until YYYY-MM-DD]
```

This MVP reports:
- total commits
- top contributors
- most changed files
- average commit message length
