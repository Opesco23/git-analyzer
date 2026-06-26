import subprocess
import os

def _run_git(args, repo):
    return subprocess.check_output(["git"] + args, cwd=repo, text=True)

def get_commits(repo='.', since=None, until=None):
    repo = os.path.abspath(repo)
    git_dir = os.path.join(repo, '.git')
    if not os.path.isdir(git_dir):
        raise ValueError(f"Not a git repository: {repo}")

    fmt = "%H|%an|%ai|%s"
    cmd = ['log', f'--pretty=format:{fmt}']
    if since:
        cmd.append(f'--since={since}')
    if until:
        cmd.append(f'--until={until}')

    try:
        raw = _run_git(cmd, repo)
    except subprocess.CalledProcessError:
        return []

    commits = []
    for line in raw.splitlines():
        parts = line.split('|', 3)
        if len(parts) < 4:
            continue
        chash, author, atime, message = parts
        date = atime.split()[0]
        # get files changed in that commit
        try:
            files_raw = _run_git(['diff-tree', '--no-commit-id', '--name-only', '-r', '--root', chash], repo)
            files = [f.strip() for f in files_raw.splitlines() if f.strip()]
        except subprocess.CalledProcessError:
            files = []

        commits.append({
            'hash': chash,
            'author': author,
            'date': date,
            'message': message,
            'files': files,
        })

    return commits
