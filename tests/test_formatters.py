import unittest
import io
from contextlib import redirect_stdout
from collections import Counter
from formatters import print_summary


class TestPrintSummary(unittest.TestCase):

    def setUp(self):
        self.stats = {
            'total_commits': 5,
            'authors': Counter({'Alice': 3, 'Bob': 2}),
            'commits_by_date': Counter({'2026-01-01': 2, '2026-01-02': 3}),
            'most_changed_files': [('a.py', 3), ('b.py', 2)],
            'avg_msg_len': 20.5,
        }

    def test_output_contains_repo_path(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            print_summary(self.stats, '/some/path')
        output = buf.getvalue()
        self.assertIn('/some/path', output)

    def test_output_contains_total_commits(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            print_summary(self.stats, '.')
        output = buf.getvalue()
        self.assertIn('Total Commits: 5', output)

    def test_output_contains_date_range(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            print_summary(self.stats, '.')
        output = buf.getvalue()
        self.assertIn('2026-01-01 to 2026-01-02', output)

    def test_output_contains_top_contributors(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            print_summary(self.stats, '.')
        output = buf.getvalue()
        self.assertIn('Alice', output)
        self.assertIn('Bob', output)
        self.assertIn('3 commits', output)
        self.assertIn('2 commits', output)

    def test_output_contains_percentages(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            print_summary(self.stats, '.')
        output = buf.getvalue()
        self.assertIn('60.0%', output)
        self.assertIn('40.0%', output)

    def test_output_contains_most_changed_files(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            print_summary(self.stats, '.')
        output = buf.getvalue()
        self.assertIn('a.py', output)
        self.assertIn('3 times', output)
        self.assertIn('b.py', output)

    def test_output_contains_avg_msg_len(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            print_summary(self.stats, '.')
        output = buf.getvalue()
        self.assertIn('Average Commit Message Length: 20 characters', output)

    def test_no_date_range_when_no_dates(self):
        stats = {
            'total_commits': 0,
            'authors': Counter(),
            'commits_by_date': Counter(),
            'most_changed_files': [],
            'avg_msg_len': 0,
        }
        buf = io.StringIO()
        with redirect_stdout(buf):
            print_summary(stats, '.')
        output = buf.getvalue()
        self.assertNotIn('Date Range', output)
