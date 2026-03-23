import os
import subprocess

class GitAnalyzer:
    def __init__(self, repo_path):
        self.repo_path = repo_path

    def get_commit_history(self):
        """Retrieves the commit history of the Git repository."""
        os.chdir(self.repo_path)
        try:
            commit_history = subprocess.check_output(['git', 'log', '--pretty=format:"%h %an %ad %s"'], universal_newlines=True)
            return commit_history.split('\n')
        except subprocess.CalledProcessError as e:
            print(f"Error retrieving commit history: {e}")
            return []

    def get_branch_info(self):
        """Retrieves the branch information of the Git repository."""
        os.chdir(self.repo_path)
        try:
            branch_info = subprocess.check_output(['git', 'branch', '-a'], universal_newlines=True)
            return branch_info.split('\n')
        except subprocess.CalledProcessError as e:
            print(f"Error retrieving branch information: {e}")
            return []

    def get_repo_stats(self):
        """Retrieves various statistics about the Git repository."""
        os.chdir(self.repo_path)
        try:
            num_commits = len(self.get_commit_history())
            num_branches = len(self.get_branch_info()) - 1  # Exclude the 'master' branch
            return {
                'num_commits': num_commits,
                'num_branches': num_branches
            }
        except Exception as e:
            print(f"Error retrieving repository statistics: {e}")
            return {}
