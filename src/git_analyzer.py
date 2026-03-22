import git
import datetime
from collections import defaultdict
from typing import Dict, List, Tuple

class GitAnalyzer:
    def __init__(self, repo_path: str):
        self.repo = git.Repo(repo_path)
        self.activity_data = defaultdict(int)
        
    def analyze_contributions(self) -> Dict[str, dict]:
        """Analyze repository contributions by author"""
        contributions = defaultdict(lambda: {
            'commits': 0,
            'insertions': 0,
            'deletions': 0,
            'files_modified': set()
        })
        
        for commit in self.repo.iter_commits():
            author_email = commit.author.email
            contributions[author_email]['commits'] += 1
            
            # Track file changes and line modifications
            if len(commit.parents) > 0:
                diffs = commit.parents[0].diff(commit)
                for diff in diffs:
                    contributions[author_email]['files_modified'].add(diff.a_path)
                    if diff.a_blob and diff.b_blob:
                        contributions[author_email]['insertions'] += diff.stats.get('insertions', 0)
                        contributions[author_email]['deletions'] += diff.stats.get('deletions', 0)
        
        # Convert sets to lengths for JSON serialization
        for author in contributions:
            contributions[author]['files_modified'] = len(contributions[author]['files_modified'])
            
        return dict(contributions)

    def generate_activity_heatmap(self) -> Dict[str, int]:
        """Generate activity heatmap data for the repository"""
        for commit in self.repo.iter_commits():
            date_str = commit.committed_datetime.strftime('%Y-%m-%d')
            self.activity_data[date_str] += 1
        return dict(self.activity_data)
    
    def get_hotspots(self) -> List[Tuple[str, int]]:
        """Identify code hotspots - files with most frequent changes"""
        file_changes = defaultdict(int)
        
        for commit in self.repo.iter_commits():
            if len(commit.parents) > 0:
                diffs = commit.parents[0].diff(commit)
                for diff in diffs:
                    if diff.a_path:
                        file_changes[diff.a_path] += 1
        
        # Sort by number of changes in descending order
        hotspots = sorted(file_changes.items(), key=lambda x: x[1], reverse=True)
        return hotspots
    
    def get_commit_velocity(self, days: int = 30) -> Dict[str, int]:
        """Calculate commit velocity over specified time period"""
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
        velocity_data = defaultdict(int)
        
        for commit in self.repo.iter_commits():
            if commit.committed_datetime > cutoff_date:
                date_str = commit.committed_datetime.strftime('%Y-%m-%d')
                velocity_data[date_str] += 1
                
        return dict(velocity_data)

    def get_summary_stats(self) -> Dict[str, int]:
        """Get summary statistics for the repository"""
        return {
            'total_commits': len(list(self.repo.iter_commits())),
            'total_contributors': len(self.get_unique_contributors()),
            'active_branches': len(list(self.repo.branches)),
            'total_tags': len(list(self.repo.tags))
        }
    
    def get_unique_contributors(self) -> set:
        """Get set of unique contributor emails"""
        return {commit.author.email for commit in self.repo.iter_commits()}
