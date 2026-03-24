import os
import subprocess
import json

class GitAnalyzer:
    def __init__(self, repo_path):
        self.repo_path = repo_path

    def get_commit_history(self):
        os.chdir(self.repo_path)
        output = subprocess.check_output(['git', 'log', '--pretty=format:"%h,%an,%ae,%ad,%s"'], universal_newlines=True)
        commits = []
        for line in output.strip().split('\
'):
            commit_data = line.strip('"').split(',')
            commits.append({
                'hash': commit_data[0],
                'author_name': commit_data[1],
                'author_email': commit_data[2],
                'date': commit_data[3],
                'message': commit_data[4]
            })
        return commits

    def get_file_changes(self, since_commit=None):
        os.chdir(self.repo_path)
        if since_commit:
            output = subprocess.check_output(['git', 'diff', '--name-status', since_commit], universal_newlines=True)
        else:
            output = subprocess.check_output(['git', 'diff', '--name-status'], universal_newlines=True)
        file_changes = []
        for line in output.strip().split('\
'):
            status, filename = line.split('\\t')
            file_changes.append({
                'status': status,
                'filename': filename
            })
        return file_changes

    def get_branch_info(self):
        os.chdir(self.repo_path)
        output = subprocess.check_output(['git', 'branch', '-vv'], universal_newlines=True)
        branches = []
        for line in output.strip().split('\
'):
            if line.startswith('*'):
                current_branch = line.strip('* ')
                current_branch_data = current_branch.split(' ')
                branches.append({
                    'name': current_branch_data[0],
                    'commit': current_branch_data[1],
                    'status': ' '.join(current_branch_data[2:])
                })
            else:
                branch_data = line.strip().split(' ')
                branches.append({
                    'name': branch_data[0],
                    'commit': branch_data[1],
                    'status': ' '.join(branch_data[2:])
                })
        return branches

    def get_repo_stats(self):
        os.chdir(self.repo_path)
        output = subprocess.check_output(['git', 'status', '--porcelain=v2'], universal_newlines=True)
        repo_stats = {
            'modified': 0,
            'untracked': 0,
            'staged': 0,
            'deleted': 0
        }
        for line in output.strip().split('\
'):
            status, _, filename = line.split(' ', 2)
            if status == '1 modified':
                repo_stats['modified'] += 1
            elif status == '?? untracked':
                repo_stats['untracked'] += 1
            elif status == 'A  added':
                repo_stats['staged'] += 1
            elif status == 'D  deleted':
                repo_stats['deleted'] += 1
        return repo_stats

    def generate_report(self):
        report = {
            'commit_history': self.get_commit_history(),
            'file_changes': self.get_file_changes(),
            'branch_info': self.get_branch_info(),
            'repo_stats': self.get_repo_stats()
        }
        return report
