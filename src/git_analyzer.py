import os
import subprocess
import json

class GitAnalyzer:
    def __init__(self, repo_path):
        self.repo_path = repo_path

    def get_commit_history(self):
        os.chdir(self.repo_path)
        commit_history = subprocess.check_output(['git', 'log', '--pretty=format:"%h|%an|%ae|%ad|%s"'], universal_newlines=True)
        commits = []
        for line in commit_history.split('\n'):
            if line:
                commit = line.strip('"').split('|')
                commits.append({
                    'hash': commit[0],
                    'author_name': commit[1],
                    'author_email': commit[2],
                    'date': commit[3],
                    'message': commit[4]
                })
        return commits

    def get_branch_info(self):
        os.chdir(self.repo_path)
        branch_info = subprocess.check_output(['git', 'show-ref', '--heads'], universal_newlines=True)
        branches = []
        for line in branch_info.split('\n'):
            if line:
                branch = line.split(' ')
                branches.append({
                    'hash': branch[0],
                    'name': branch[1].replace('refs/heads/', '')
                })
        return branches

    def get_file_changes(self, commit_hash):
        os.chdir(self.repo_path)
        file_changes = subprocess.check_output(['git', 'show', '--name-status', commit_hash], universal_newlines=True)
        changes = []
        for line in file_changes.split('\n'):
            if line and not line.startswith('commit '):
                change = line.split('\t')
                changes.append({
                    'status': change[0],
                    'filename': change[1]
                })
        return changes

    def analyze_repository(self):
        commit_history = self.get_commit_history()
        branch_info = self.get_branch_info()
        return {
            'commit_history': commit_history,
            'branch_info': branch_info
        }
