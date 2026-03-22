import git
from typing import Dict, List, Tuple
import re
from dataclasses import dataclass
from enum import Enum

class RiskLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class CommitAnalysis:
    commit_hash: str
    risk_level: RiskLevel
    impact_score: float
    affected_files: List[str]
    risky_patterns: List[str]

class GitAnalyzer:
    def __init__(self, repo_path: str):
        self.repo = git.Repo(repo_path)
        self.risk_patterns = {
            'critical': [
                r'DROP\s+TABLE',
                r'DROP\s+DATABASE',
                r'rm\s+-rf',
                r'TRUNCATE\s+TABLE'
            ],
            'high': [
                r'password',
                r'SECRET',
                r'API_KEY',
                r'\bTODO\b'
            ],
            'medium': [
                r'deprecated',
                r'FIXME',
                r'hack',
                r'workaround'
            ]
        }

    def analyze_commit(self, commit_hash: str) -> CommitAnalysis:
        commit = self.repo.commit(commit_hash)
        affected_files = []
        risky_patterns = []
        impact_score = 0.0

        # Analyze each file in the commit
        for file in commit.stats.files:
            affected_files.append(file)
            try:
                diff = commit.diff(commit.parents[0], paths=file, create_patch=True)
                for d in diff:
                    if d.diff:
                        decoded_diff = d.diff.decode('utf-8')
                        impact_score += self._calculate_diff_impact(decoded_diff)
                        patterns = self._find_risky_patterns(decoded_diff)
                        risky_patterns.extend(patterns)
            except:
                continue

        risk_level = self._determine_risk_level(impact_score, len(risky_patterns))

        return CommitAnalysis(
            commit_hash=commit_hash,
            risk_level=risk_level,
            impact_score=impact_score,
            affected_files=affected_files,
            risky_patterns=risky_patterns
        )

    def _calculate_diff_impact(self, diff_content: str) -> float:
        lines_added = len([l for l in diff_content.split('\n') if l.startswith('+')])
        lines_removed = len([l for l in diff_content.split('\n') if l.startswith('-')])
        
        # Impact formula considers both additions and deletions
        # Deletions are weighted slightly higher as they're generally riskier
        return (lines_added * 1.0) + (lines_removed * 1.2)

    def _find_risky_patterns(self, content: str) -> List[str]:
        found_patterns = []
        
        for severity, patterns in self.risk_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    found_patterns.append(f'{severity}:{pattern}')
        
        return found_patterns

    def _determine_risk_level(self, impact_score: float, risky_pattern_count: int) -> RiskLevel:
        if impact_score > 500 or risky_pattern_count >= 3:
            return RiskLevel.CRITICAL
        elif impact_score > 200 or risky_pattern_count >= 2:
            return RiskLevel.HIGH
        elif impact_score > 50 or risky_pattern_count >= 1:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    def analyze_branch(self, branch_name: str, max_commits: int = 10) -> List[CommitAnalysis]:
        analyses = []
        commits = list(self.repo.iter_commits(branch_name, max_count=max_commits))
        
        for commit in commits:
            analysis = self.analyze_commit(commit.hexsha)
            analyses.append(analysis)
            
        return analyses

    def get_high_risk_commits(self, branch_name: str, max_commits: int = 50) -> List[CommitAnalysis]:
        analyses = self.analyze_branch(branch_name, max_commits)
        return [a for a in analyses if a.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL)]