import argparse
from git_parser import get_commits
import stats as stats_mod
import formatters


def main():
    parser = argparse.ArgumentParser(description='Git Analyzer')
    parser.add_argument('--repo', default='.', help='Path to git repository')
    parser.add_argument('--since', help='Since date (YYYY-MM-DD)')
    parser.add_argument('--until', help='Until date (YYYY-MM-DD)')
    args = parser.parse_args()

    try:
        commits = get_commits(args.repo, since=args.since, until=args.until)
    except Exception as e:
        print('Error:', e)
        return

    stats = stats_mod.calculate_stats(commits)
    formatters.print_summary(stats, args.repo)


if __name__ == '__main__':
    main()
