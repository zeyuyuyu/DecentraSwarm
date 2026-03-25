import os
import subprocess
import json

class GitAnalyzer:
    def __init__(self, repo_path):
        self.repo_path = repo_path

    def get_commit_history(self):
        os.chdir(self.repo_path)
        try:
            output = subprocess.check_output(['git', 'log', '--pretty=format:%H|%an|%ae|%ad|%s'], universal_newlines=True)
            commits = []
            for line in output.splitlines():
                commit_data = line.split('|')
                commit = {
                    'hash': commit_data[0],
                    'author_name': commit_data[1],
                    'author_email': commit_data[2],
                    'date': commit_data[3],
                    'message': commit_data[4]
                }
                commits.append(commit)
            return commits
        except subprocess.CalledProcessError as e:
            print(f'Error getting commit history: {e}')
            return []

    def get_branch_info(self):
        os.chdir(self.repo_path)
        try:
            output = subprocess.check_output(['git', 'branch', '-vv'], universal_newlines=True)
            branches = []
            for line in output.splitlines():
                if line.startswith('*'):
                    branch_data = line[2:].split()
                    branch = {
                        'name': branch_data[0],
                        'commit': branch_data[1],
                        'status': ' '.join(branch_data[2:])
                    }
                    branches.append(branch)
            return branches
        except subprocess.CalledProcessError as e:
            print(f'Error getting branch info: {e}')
            return []

    def get_repo_info(self):
        os.chdir(self.repo_path)
        try:
            output = subprocess.check_output(['git', 'remote', '-v'], universal_newlines=True)
            remotes = []
            for line in output.splitlines():
                remote_data = line.split()
                remote = {
                    'name': remote_data[0],
                    'url': remote_data[1]
                }
                remotes.append(remote)

            output = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], universal_newlines=True)
            current_branch = output.strip()

            return {
                'remotes': remotes,
                'current_branch': current_branch
            }
        except subprocess.CalledProcessError as e:
            print(f'Error getting repository info: {e}')
            return {}
