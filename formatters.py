def print_summary(stats, repo):
    print("📊 Git Repository Stats")
    print(f"Repository: {repo}")
    print()
    print(f"Total Commits: {stats['total_commits']}")

    dates = sorted(stats['commits_by_date'].keys())
    if dates:
        print(f"Date Range: {dates[0]} to {dates[-1]}")

    print()
    print("Top Contributors:")
    for author, count in stats['authors'].most_common(10):
        pct = (count / stats['total_commits'] * 100) if stats['total_commits'] else 0
        print(f"  {author:17} {count} commits  ({pct:.1f}%)")

    print()
    print("Most Changed Files:")
    for fname, cnt in stats['most_changed_files']:
        print(f"  {fname:17} {cnt} times")

    print()
    print(f"Average Commit Message Length: {stats['avg_msg_len']:.0f} characters")
