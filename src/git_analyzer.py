import os
import subprocess

class GitAnalyzer:
    def __init__(self, repo_path):
        self.repo_path = repo_path

    def get_branch_info(self):
        os.chdir(self.repo_path)
        branches = subprocess.check_output(['git', 'branch']).decode('utf-8').splitlines()
        branch_info = []
        for branch in branches:
            if branch.startswith('*'):
                current_branch = branch.strip('* ')
            else:
                branch_info.append(branch.strip('* '))
        return current_branch, branch_info

    def get_commit_history(self):
        os.chdir(self.repo_path)
        commit_history = subprocess.check_output(['git', 'log', '--pretty=format:%h %an %ad %s']).decode('utf-8').splitlines()
        return commit_history

    def get_file_changes(self, branch='master'):
        os.chdir(self.repo_path)
        subprocess.check_output(['git', 'checkout', branch])
        file_changes = subprocess.check_output(['git', 'diff', '--name-only']).decode('utf-8').splitlines()
        return file_changes
