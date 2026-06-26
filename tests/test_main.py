import unittest
from unittest.mock import patch
import io
from contextlib import redirect_stdout
import subprocess
import os
import tempfile
import shutil
import sys

from main import main


class TestMainIntegration(unittest.TestCase):
    """Integration tests for main() using a real temp git repo."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        subprocess.check_call(['git', 'init'], cwd=self.test_dir)
        subprocess.check_call(['git', 'config', 'user.email', 'test@test.com'], cwd=self.test_dir)
        subprocess.check_call(['git', 'config', 'user.name', 'Tester'], cwd=self.test_dir)
        open(os.path.join(self.test_dir, 'a.py'), 'w').close()
        subprocess.check_call(['git', 'add', 'a.py'], cwd=self.test_dir)
        subprocess.check_call(['git', 'commit', '-m', 'initial commit'], cwd=self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_main_default_repo(self):
        buf = io.StringIO()
        test_args = ['main.py', '--repo', self.test_dir]
        with patch('sys.argv', test_args):
            with redirect_stdout(buf):
                main()
        output = buf.getvalue()
        self.assertIn('Total Commits: 1', output)

    @patch('sys.argv', ['main.py', '--repo', '/nonexistent'])
    def test_main_invalid_repo(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            main()
        output = buf.getvalue()
        self.assertIn('Error', output)
        self.assertIn('Not a git repository', output)
