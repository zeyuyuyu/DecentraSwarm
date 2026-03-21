import subprocess
from typing import Dict, List, Optional
import re
from dataclasses import dataclass

@dataclass
class DiffMetrics:
    file_path: str
    lines_added: int
    lines_removed: int 
    complexity_score: float
    risk_score: float

class GitDiffAnalyzer:
    def __init__(self, repo_path: str = '.'):
        self.repo_path = repo_path

    def get_diff(self, commit_range: Optional[str] = None) -> str:
        """Get git diff output for specified commit range"""
        cmd = ['git', 'diff']
        if commit_range:
            cmd.append(commit_range)
        
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        return result.stdout

    def parse_diff(self, diff_text: str) -> List[DiffMetrics]:
        """Parse git diff output into structured metrics"""
        metrics: List[DiffMetrics] = []
        current_file = ''
        lines_added = 0
        lines_removed = 0

        for line in diff_text.split('\n'):
            if line.startswith('+++'):
                current_file = line[6:]
            elif line.startswith('+') and not line.startswith('+++'):
                lines_added += 1
            elif line.startswith('-') and not line.startswith('---'):
                lines_removed += 1
            elif line.startswith('diff --git') and current_file:
                # Save previous file metrics
                if current_file:
                    metrics.append(self._create_metrics(current_file, lines_added, lines_removed))
                current_file = ''
                lines_added = 0
                lines_removed = 0

        # Add final file metrics
        if current_file:
            metrics.append(self._create_metrics(current_file, lines_added, lines_removed))

        return metrics

    def _create_metrics(self, file_path: str, lines_added: int, lines_removed: int) -> DiffMetrics:
        """Create DiffMetrics with computed scores"""
        complexity_score = self._calculate_complexity(lines_added, lines_removed)
        risk_score = self._calculate_risk_score(file_path, lines_added, lines_removed)
        
        return DiffMetrics(
            file_path=file_path,
            lines_added=lines_added,
            lines_removed=lines_removed,
            complexity_score=complexity_score,
            risk_score=risk_score
        )

    def _calculate_complexity(self, lines_added: int, lines_removed: int) -> float:
        """Calculate complexity score based on changes"""
        base_score = (lines_added + lines_removed) / 10.0
        change_ratio = lines_added / (lines_removed + 1)  # Avoid div by zero
        return min(base_score * change_ratio, 10.0)

    def _calculate_risk_score(self, file_path: str, lines_added: int, lines_removed: int) -> float:
        """Calculate risk score based on file type and changes"""
        risk_factors = {
            r'\.py$': 1.0,  # Python files
            r'\.js$': 1.2,  # JavaScript files
            r'test': 0.5,  # Test files
            r'security': 2.0,  # Security-related files
            r'core': 1.5   # Core functionality
        }

        base_risk = 1.0
        for pattern, factor in risk_factors.items():
            if re.search(pattern, file_path, re.IGNORECASE):
                base_risk *= factor

        change_volume = lines_added + lines_removed
        return min(base_risk * (change_volume / 20.0), 10.0)

    def analyze_commit_range(self, commit_range: str) -> Dict[str, List[DiffMetrics]]:
        """Analyze git diff for a commit range and return metrics"""
        diff_text = self.get_diff(commit_range)
        metrics = self.parse_diff(diff_text)

        # Group metrics by risk level
        risk_groups: Dict[str, List[DiffMetrics]] = {
            'high_risk': [],
            'medium_risk': [],
            'low_risk': []
        }

        for metric in metrics:
            if metric.risk_score >= 7.0:
                risk_groups['high_risk'].append(metric)
            elif metric.risk_score >= 4.0:
                risk_groups['medium_risk'].append(metric)
            else:
                risk_groups['low_risk'].append(metric)

        return risk_groups