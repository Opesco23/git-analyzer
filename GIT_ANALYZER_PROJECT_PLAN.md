# Git Log Analyzer — Project Plan

## What You're Building
A CLI tool that analyzes git repositories and shows useful stats:
- **Commits per day/week** — when is the team most active?
- **Top contributors** — who commits most?
- **Commit messages** — average length, most common words
- **File activity** — which files change most?
- **Streak analysis** — longest coding streak

## Tech Stack
- **Python 3.8+**
- **subprocess** — run git commands
- **argparse** — CLI argument parsing
- **collections.Counter** — frequency analysis
- **datetime** — date manipulation
- **matplotlib** (optional) — visualize trends

## Project Structure
```
git-analyzer/
├── README.md
├── main.py              # Entry point, CLI argument handling
├── git_parser.py        # Extract data from git log
├── stats.py             # Calculate statistics
├── formatters.py        # Pretty-print output
├── requirements.txt
└── .gitignore
```

## Phase 1: MVP (Week 1)
**Goal:** Basic stats working, deployable

### Tasks
1. **Setup**
   - Create repo, Python virtual environment
   - Initialize git, create requirements.txt
   - Write README with usage examples

2. **git_parser.py**
   - Run `git log --pretty=format` to extract:
     - Author name
     - Date (parse to YYYY-MM-DD)
     - Commit message
     - Files changed (from `git diff-tree`)
   - Return list of commit dictionaries
   - Handle errors gracefully (no git repo, empty repo)

3. **stats.py**
   - Count commits per author
   - Count commits per day
   - Calculate average message length
   - Find most changed files
   - Return dictionary of stats

4. **main.py**
   - CLI args: `--repo` (path), `--since` (date), `--until` (date)
   - Read git log from specified repo
   - Calculate stats
   - Format and print results

5. **formatters.py**
   - Pretty-print tables (authors, commits/day)
   - Use simple text formatting (ASCII tables)

### Output Example
```
$ python main.py --repo .

📊 Git Repository Stats
Repository: /path/to/repo

Total Commits: 342
Date Range: 2024-01-15 to 2026-06-04

Top Contributors:
  you               125 commits  (36.6%)
  teammate_1         98 commits  (28.7%)
  teammate_2         67 commits  (19.6%)

Most Active Days:
  Monday            58 commits
  Tuesday           52 commits
  Wednesday         41 commits

Most Changed Files:
  src/main.py       45 times
  README.md         28 times
  config.json       22 times

Average Commit Message Length: 47 characters
```

---

## Phase 2: Polish (Week 2)
**Goal:** Production-ready, better UX

### Tasks
1. **Better CLI**
   - Add subcommands: `analyze`, `streak`, `trending`
   - Color-coded output (colorama library)
   - Progress bar for large repos (tqdm)

2. **Advanced Stats**
   - Longest coding streak (consecutive days with commits)
   - Commits by hour of day
   - Most common words in commit messages
   - Author activity heatmap (day of week vs. time)

3. **Export Options**
   - `--format json` — export stats as JSON
   - `--format csv` — export for analysis
   - Save results to file

4. **Edge Cases**
   - Handle merge commits
   - Filter out bot commits
   - Deal with author name variations
   - Large repos (optimize git log queries)

5. **Tests**
   - Unit tests for stats calculations
   - Mock git output for testing
   - pytest setup

6. **Documentation**
   - Docstrings for all functions
   - Usage examples in README
   - Troubleshooting guide

---

## Phase 3: Advanced (Optional)
**Goal:** Wow factor for portfolio

### Tasks
1. **Visualizations**
   - Commit timeline (matplotlib)
   - Heatmap: author vs. weekday
   - Word cloud of commit messages
   - Save charts as PNG/SVG

2. **Collaboration Features**
   - Compare two authors
   - Team velocity over time
   - Code review backlog (based on merged PRs)

3. **Web Dashboard (Bonus)**
   - Flask app that serves interactive stats
   - Real-time updates
   - Deploy to Heroku/Railway

---

## Learning Outcomes
By completing this project, you'll:
- ✅ Master **subprocess** — running external commands safely
- ✅ Parse unstructured data — git log output
- ✅ Work with **datetime** — convert timestamps, calculate ranges
- ✅ Use **collections** — Counter, defaultdict for analysis
- ✅ Build a real **CLI tool** — argument parsing, user experience
- ✅ Write testable code — separation of concerns (parser, stats, display)
- ✅ Deploy to GitHub — real project people can install and use

---

## Getting Started
1. Create a new folder: `mkdir git-analyzer && cd git-analyzer`
2. Initialize git: `git init`
3. Create virtual env: `python -m venv venv && source venv/bin/activate`
4. Start with Phase 1, Task 1 (setup)
5. Build incrementally — commit after each task works

---

## Commands You'll Need
```bash
# Extract commit info
git log --pretty=format:"%an|%ai|%s" --name-only

# Get files in a commit
git diff-tree --no-commit-id --name-only -r COMMIT_HASH

# Since/until filters
git log --since="2024-01-01" --until="2024-12-31"
```

---

## Next Step
Pick **Phase 1, Task 1** and start here. I'll help you code it.
