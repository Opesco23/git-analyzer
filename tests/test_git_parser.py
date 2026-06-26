import unittest
from unittest.mock import patch
import subprocess
import os
import tempfile
import shutil
from git_parser import get_commits, _run_git


GIT_LOG_OUTPUT = (
    "abc123|Alice|2026-01-01 12:00:00 +0000|Initial commit\n"
    "def456|Bob|2026-01-02 14:30:00 +0000|Add feature"
)

DIFF_TREE_OUTPUT_1 = "README.md\nmain.py"
DIFF_TREE_OUTPUT_2 = "main.py\nutils.py"


class TestRunGit(unittest.TestCase):

    @patch('git_parser.subprocess.check_output')
    def test_run_git_calls_check_output(self, mock_check_output):
        mock_check_output.return_value = "output"
        result = _run_git(['log', '--oneline'], '/repo')
        mock_check_output.assert_called_once_with(
            ['git', 'log', '--oneline'], cwd='/repo', text=True
        )
        self.assertEqual(result, 'output')


class TestGetCommits(unittest.TestCase):

    @patch('git_parser.os.path.isdir')
    @patch('git_parser._run_git')
    def test_get_commits_success(self, mock_run_git, mock_isdir):
        mock_isdir.return_value = True
        mock_run_git.side_effect = [
            GIT_LOG_OUTPUT,
            DIFF_TREE_OUTPUT_1,
            DIFF_TREE_OUTPUT_2,
        ]

        commits = get_commits('/repo')

        self.assertEqual(len(commits), 2)
        self.assertEqual(commits[0]['hash'], 'abc123')
        self.assertEqual(commits[0]['author'], 'Alice')
        self.assertEqual(commits[0]['date'], '2026-01-01')
        self.assertEqual(commits[0]['message'], 'Initial commit')
        self.assertEqual(commits[0]['files'], ['README.md', 'main.py'])

        self.assertEqual(commits[1]['hash'], 'def456')
        self.assertEqual(commits[1]['author'], 'Bob')
        self.assertEqual(commits[1]['date'], '2026-01-02')
        self.assertEqual(commits[1]['message'], 'Add feature')
        self.assertEqual(commits[1]['files'], ['main.py', 'utils.py'])

    @patch('git_parser.os.path.isdir')
    def test_raises_on_non_git_repo(self, mock_isdir):
        mock_isdir.return_value = False
        with self.assertRaises(ValueError) as ctx:
            get_commits('/not-a-repo')
        self.assertIn('Not a git repository', str(ctx.exception))

    @patch('git_parser.os.path.isdir')
    @patch('git_parser._run_git')
    def test_returns_empty_on_subprocess_failure(self, mock_run_git, mock_isdir):
        mock_isdir.return_value = True
        mock_run_git.side_effect = subprocess.CalledProcessError(128, ['git'])

        commits = get_commits('/repo')
        self.assertEqual(commits, [])

    @patch('git_parser.os.path.isdir')
    @patch('git_parser._run_git')
    def test_get_commits_with_since_until(self, mock_run_git, mock_isdir):
        mock_isdir.return_value = True
        mock_run_git.side_effect = [
            GIT_LOG_OUTPUT,
            DIFF_TREE_OUTPUT_1,
            DIFF_TREE_OUTPUT_2,
        ]

        commits = get_commits('/repo', since='2026-01-01', until='2026-01-31')

        log_call = mock_run_git.call_args_list[0]
        args = log_call[0][0]
        self.assertIn('--since=2026-01-01', args)
        self.assertIn('--until=2026-01-31', args)

    @patch('git_parser.os.path.isdir')
    @patch('git_parser._run_git')
    def test_get_commits_empty_output(self, mock_run_git, mock_isdir):
        mock_isdir.return_value = True
        mock_run_git.side_effect = [""]

        commits = get_commits('/repo')
        self.assertEqual(commits, [])

    @patch('git_parser.os.path.isdir')
    @patch('git_parser._run_git')
    def test_get_commits_malformed_lines_skipped(self, mock_run_git, mock_isdir):
        mock_isdir.return_value = True
        mock_run_git.side_effect = [
            "abc123|Alice|2026-01-01 12:00:00 +0000|Good\n"
            "bad_line_no_pipes\n"
            "def456|Bob|2026-01-02 14:30:00 +0000|Also good",
            DIFF_TREE_OUTPUT_1,
            DIFF_TREE_OUTPUT_2,
        ]

        commits = get_commits('/repo')
        self.assertEqual(len(commits), 2)

    @patch('git_parser.os.path.isdir')
    @patch('git_parser._run_git')
    def test_diff_tree_failure_returns_empty_files(self, mock_run_git, mock_isdir):
        mock_isdir.return_value = True
        mock_run_git.side_effect = [
            GIT_LOG_OUTPUT,
            subprocess.CalledProcessError(128, ['git']),
            DIFF_TREE_OUTPUT_2,
        ]

        commits = get_commits('/repo')
        self.assertEqual(len(commits), 2)
        self.assertEqual(commits[0]['files'], [])
        self.assertEqual(commits[1]['files'], ['main.py', 'utils.py'])


class TestGetCommitsIntegration(unittest.TestCase):
    """Integration tests using a real temporary git repository."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self._run(['git', 'init'])
        self._run(['git', 'config', 'user.email', 'test@test.com'])
        self._run(['git', 'config', 'user.name', 'Tester'])

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def _run(self, cmd):
        subprocess.check_call(cmd, cwd=self.test_dir)

    def test_integration_real_repo(self):
        open(os.path.join(self.test_dir, 'a.py'), 'w').close()
        self._run(['git', 'add', 'a.py'])
        self._run(['git', 'commit', '-m', 'first'])

        open(os.path.join(self.test_dir, 'b.py'), 'w').close()
        self._run(['git', 'add', 'b.py'])
        self._run(['git', 'commit', '-m', 'second'])

        commits = get_commits(self.test_dir)
        self.assertEqual(len(commits), 2)
        self.assertEqual(commits[0]['message'], 'second')
        self.assertEqual(commits[1]['message'], 'first')
        self.assertEqual(commits[0]['files'], ['b.py'])
        self.assertEqual(commits[1]['files'], ['a.py'])

    def test_integration_since_filter(self):
        open(os.path.join(self.test_dir, 'a.py'), 'w').close()
        self._run(['git', 'add', 'a.py'])
        env = dict(os.environ, GIT_AUTHOR_DATE='2025-01-01T12:00:00', GIT_COMMITTER_DATE='2025-01-01T12:00:00')
        subprocess.check_call(['git', 'commit', '-m', 'old'], cwd=self.test_dir, env=env)

        open(os.path.join(self.test_dir, 'b.py'), 'w').close()
        self._run(['git', 'add', 'b.py'])
        env = dict(os.environ, GIT_AUTHOR_DATE='2026-06-01T12:00:00', GIT_COMMITTER_DATE='2026-06-01T12:00:00')
        subprocess.check_call(['git', 'commit', '-m', 'new'], cwd=self.test_dir, env=env)

        commits = get_commits(self.test_dir, since='2026-01-01')
        self.assertEqual(len(commits), 1)
        self.assertEqual(commits[0]['message'], 'new')
