from collections import Counter

def calculate_stats(commits):
    total = len(commits)
    authors = Counter(c['author'] for c in commits)
    commits_by_date = Counter(c['date'] for c in commits)
    file_counter = Counter()
    msg_lengths = [len(c.get('message', '')) for c in commits]

    for c in commits:
        file_counter.update(c.get('files', []))

    avg_msg_len = (sum(msg_lengths) / len(msg_lengths)) if msg_lengths else 0

    return {
        'total_commits': total,
        'authors': authors,
        'commits_by_date': commits_by_date,
        'most_changed_files': file_counter.most_common(10),
        'avg_msg_len': avg_msg_len,
    }
