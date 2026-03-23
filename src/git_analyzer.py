import os
import git
import datetime

class GitAnalyzer:
    def __init__(self, repo_path):
        self.repo = git.Repo(repo_path)

    def get_commit_history(self):
        commit_history = []
        for commit in self.repo.iter_commits():
            commit_history.append({
                'hash': commit.hexsha,
                'author': commit.author.name,
                'email': commit.author.email,
                'date': commit.committed_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                'message': commit.message
            })
        return commit_history

    def get_file_changes(self, file_path):
        changes = []
        for commit in self.repo.iter_commits(paths=file_path):
            for file_change in commit.diff(commit.parents[0] if commit.parents else None):
                if file_change.a_path == file_path:
                    changes.append({
                        'commit_hash': commit.hexsha,
                        'author': commit.author.name,
                        'email': commit.author.email,
                        'date': commit.committed_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                        'lines_added': file_change.additions,
                        'lines_deleted': file_change.deletions
                    })
        return changes

    def get_repository_stats(self):
        commit_count = len(list(self.repo.iter_commits()))
        branch_count = len(self.repo.branches)
        return {
            'commit_count': commit_count,
            'branch_count': branch_count
        }
