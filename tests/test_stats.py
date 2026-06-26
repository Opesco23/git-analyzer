import unittest
from stats import calculate_stats


class TestCalculateStats(unittest.TestCase):

    def test_empty_commits(self):
        stats = calculate_stats([])
        self.assertEqual(stats['total_commits'], 0)
        self.assertEqual(len(stats['authors']), 0)
        self.assertEqual(len(stats['commits_by_date']), 0)
        self.assertEqual(stats['most_changed_files'], [])
        self.assertEqual(stats['avg_msg_len'], 0)

    def test_single_commit(self):
        commits = [
            {'author': 'Alice', 'date': '2026-01-01', 'message': 'Initial', 'files': ['README.md']},
        ]
        stats = calculate_stats(commits)
        self.assertEqual(stats['total_commits'], 1)
        self.assertEqual(stats['authors']['Alice'], 1)
        self.assertEqual(stats['commits_by_date']['2026-01-01'], 1)
        self.assertEqual(stats['most_changed_files'], [('README.md', 1)])
        self.assertEqual(stats['avg_msg_len'], 7)

    def test_multiple_authors(self):
        commits = [
            {'author': 'Alice', 'date': '2026-01-01', 'message': 'a', 'files': []},
            {'author': 'Bob', 'date': '2026-01-02', 'message': 'b', 'files': []},
            {'author': 'Alice', 'date': '2026-01-03', 'message': 'c', 'files': []},
        ]
        stats = calculate_stats(commits)
        self.assertEqual(stats['total_commits'], 3)
        self.assertEqual(stats['authors']['Alice'], 2)
        self.assertEqual(stats['authors']['Bob'], 1)

    def test_file_counting(self):
        commits = [
            {'author': 'A', 'date': '2026-01-01', 'message': 'm1', 'files': ['a.py', 'b.py']},
            {'author': 'A', 'date': '2026-01-02', 'message': 'm2', 'files': ['a.py']},
            {'author': 'A', 'date': '2026-01-03', 'message': 'm3', 'files': ['c.py']},
        ]
        stats = calculate_stats(commits)
        top = stats['most_changed_files']
        self.assertEqual(top[0], ('a.py', 2))
        self.assertIn(('b.py', 1), top)
        self.assertIn(('c.py', 1), top)

    def test_average_message_length(self):
        commits = [
            {'author': 'A', 'date': '2026-01-01', 'message': 'ab', 'files': []},
            {'author': 'A', 'date': '2026-01-02', 'message': 'abcd', 'files': []},
        ]
        stats = calculate_stats(commits)
        self.assertEqual(stats['avg_msg_len'], 3.0)

    def test_top_ten_files(self):
        files = [f'file{i}.py' for i in range(15)]
        commits = [
            {'author': 'A', 'date': '2026-01-01', 'message': 'm', 'files': files},
        ]
        stats = calculate_stats(commits)
        self.assertEqual(len(stats['most_changed_files']), 10)

    def test_message_length_with_no_commits(self):
        stats = calculate_stats([])
        self.assertEqual(stats['avg_msg_len'], 0)

    def test_commits_by_date(self):
        commits = [
            {'author': 'A', 'date': '2026-01-01', 'message': 'm1', 'files': []},
            {'author': 'A', 'date': '2026-01-01', 'message': 'm2', 'files': []},
            {'author': 'B', 'date': '2026-01-02', 'message': 'm3', 'files': []},
        ]
        stats = calculate_stats(commits)
        self.assertEqual(stats['commits_by_date']['2026-01-01'], 2)
        self.assertEqual(stats['commits_by_date']['2026-01-02'], 1)
