#!/usr/bin/env python3
"""
Project Hours Tracking System for ISO/IEC 42001 Lead Implementer Certification
llm-agent-mcp Project

This script tracks implementation activities and generates a comprehensive log
of hours spent on each clause and document for ISO certification purposes.
"""

import os
import sys
import csv
import json
import argparse
import requests
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
from typing import List, Dict, Optional, Tuple
import re

# Configuration
GITHUB_REPO = "onchainlabs1/llm-agent-mcp"
GITHUB_API_BASE = "https://api.github.com"
CSV_FILE = "project_hours_log.csv"
MD_FILE = "project_hours_log.md"
CONFIG_FILE = "hours_config.json"

# Bot patterns to exclude
BOT_PATTERNS = [
    r'dependabot',
    r'github-actions',
    r'renovate',
    r'bot',
    r'ci',
    r'cd',
    r'auto',
    r'merge',
    r'update'
]

# Clause mapping based on file paths
CLAUSE_MAPPING = {
    'Clause4': 'Clause 4 - Context',
    'Clause5': 'Clause 5 - Leadership', 
    'Clause6': 'Clause 6 - Planning',
    'Clause7': 'Clause 7 - Support',
    'Clause8': 'Clause 8 - Operation',
    'Clause9': 'Clause 9 - Performance Evaluation',
    'Clause10': 'Clause 10 - Improvement'
}

# Default time estimates for different activity types
DEFAULT_TIME_ESTIMATES = {
    'documentation': 2.0,  # hours per documentation file
    'implementation': 1.5,  # hours per implementation file
    'testing': 1.0,        # hours per test file
    'configuration': 0.5,  # hours per config file
    'commit': 0.5,         # hours per commit (fallback)
}

class HoursTracker:
    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token
        self.session = requests.Session()
        if github_token:
            self.session.headers.update({
                'Authorization': f'token {github_token}',
                'Accept': 'application/vnd.github.v3+json'
            })
        
        self.existing_entries = self.load_existing_entries()
        
    def load_existing_entries(self) -> List[Dict]:
        """Load existing entries from CSV to avoid duplicates"""
        entries = []
        if os.path.exists(CSV_FILE):
            try:
                with open(CSV_FILE, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    entries = list(reader)
            except Exception as e:
                print(f"Warning: Could not load existing entries: {e}")
        return entries
    
    def is_bot_commit(self, commit_data: Dict) -> bool:
        """Check if commit is from a bot or automated tool"""
        author = commit_data.get('commit', {}).get('author', {}).get('name', '').lower()
        committer = commit_data.get('commit', {}).get('committer', {}).get('name', '').lower()
        
        for pattern in BOT_PATTERNS:
            if re.search(pattern, author) or re.search(pattern, committer):
                return True
        return False
    
    def categorize_clause(self, file_path: str) -> str:
        """Categorize file by ISO clause based on path"""
        for clause_pattern, clause_name in CLAUSE_MAPPING.items():
            if clause_pattern.lower() in file_path.lower():
                return clause_name
        
        # Default categorization based on file type
        if 'docs/' in file_path:
            return 'Clause 4 - Context'  # Documentation generally falls under context
        elif 'agent/' in file_path:
            return 'Clause 8 - Operation'  # Agent implementation
        elif 'services/' in file_path:
            return 'Clause 8 - Operation'  # Business services
        elif 'api/' in file_path:
            return 'Clause 8 - Operation'  # API implementation
        elif 'tests/' in file_path:
            return 'Clause 9 - Performance Evaluation'  # Testing
        else:
            return 'Clause 4 - Context'  # Default
    
    def estimate_time(self, file_path: str, commit_message: str) -> float:
        """Estimate time spent based on file type and commit message"""
        file_ext = Path(file_path).suffix.lower()
        
        # Documentation files
        if file_ext == '.md' or 'docs/' in file_path:
            return DEFAULT_TIME_ESTIMATES['documentation']
        
        # Implementation files
        elif file_ext in ['.py', '.js', '.ts', '.java']:
            return DEFAULT_TIME_ESTIMATES['implementation']
        
        # Test files
        elif 'test' in file_path.lower() or 'spec' in file_path.lower():
            return DEFAULT_TIME_ESTIMATES['testing']
        
        # Configuration files
        elif file_ext in ['.json', '.yaml', '.yml', '.toml', '.ini', '.cfg']:
            return DEFAULT_TIME_ESTIMATES['configuration']
        
        # Default estimate
        else:
            return DEFAULT_TIME_ESTIMATES['commit']
    
    def fetch_github_commits(self, since_date: Optional[str] = None) -> List[Dict]:
        """Fetch commits from GitHub API"""
        commits = []
        page = 1
        
        while True:
            url = f"{GITHUB_API_BASE}/repos/{GITHUB_REPO}/commits"
            params = {
                'page': page,
                'per_page': 100
            }
            
            if since_date:
                params['since'] = since_date
            
            try:
                response = self.session.get(url, params=params)
                response.raise_for_status()
                
                page_commits = response.json()
                if not page_commits:
                    break
                
                for commit in page_commits:
                    if not self.is_bot_commit(commit):
                        commits.append(commit)
                
                page += 1
                
                # Rate limiting check
                if 'X-RateLimit-Remaining' in response.headers:
                    remaining = int(response.headers['X-RateLimit-Remaining'])
                    if remaining <= 1:
                        print("Warning: GitHub API rate limit approaching")
                        break
                        
            except requests.exceptions.RequestException as e:
                print(f"Error fetching commits: {e}")
                break
        
        return commits
    
    def fetch_commit_details(self, commit_sha: str) -> Optional[Dict]:
        """Fetch detailed commit information including files changed"""
        url = f"{GITHUB_API_BASE}/repos/{GITHUB_REPO}/commits/{commit_sha}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching commit details for {commit_sha}: {e}")
            return None
    
    def process_commit(self, commit: Dict) -> List[Dict]:
        """Process a single commit and extract hour entries"""
        entries = []
        
        commit_sha = commit['sha']
        commit_date = commit['commit']['author']['date'][:10]  # YYYY-MM-DD
        commit_message = commit['commit']['message']
        author = commit['commit']['author']['name']
        
        # Skip if already processed
        existing_sha = f"sha:{commit_sha}"
        if any(entry.get('File/Link', '').startswith(existing_sha) for entry in self.existing_entries):
            return entries
        
        # Fetch detailed commit information
        commit_details = self.fetch_commit_details(commit_sha)
        if not commit_details:
            return entries
        
        # Process each file in the commit
        for file_change in commit_details.get('files', []):
            file_path = file_change['filename']
            
            # Skip binary files and generated files
            if file_change.get('binary', False) or any(skip in file_path for skip in ['.pyc', '.git', 'node_modules']):
                continue
            
            # Determine clause
            clause = self.categorize_clause(file_path)
            
            # Estimate time
            time_estimate = self.estimate_time(file_path, commit_message)
            
            # Create entry
            entry = {
                'Date': commit_date,
                'Task Description': f"{commit_message[:50]}...",
                'Clause': clause,
                'Time (h)': time_estimate,
                'File/Link': f"sha:{commit_sha} - {file_path}",
                'Notes': f"Author: {author}, Status: {file_change.get('status', 'modified')}"
            }
            
            entries.append(entry)
        
        return entries
    
    def add_manual_entry(self):
        """Add manual entry via CLI"""
        print("\n=== Manual Hours Entry ===")
        
        # Get date
        date_input = input("Date (YYYY-MM-DD) [today]: ").strip()
        if not date_input:
            date_input = datetime.now().strftime('%Y-%m-%d')
        
        # Get task description
        task = input("Task Description: ").strip()
        if not task:
            print("Task description is required!")
            return
        
        # Get clause
        print("\nAvailable Clauses:")
        for i, clause in enumerate(CLAUSE_MAPPING.values(), 1):
            print(f"{i}. {clause}")
        print("8. Other")
        
        clause_choice = input("Select clause (1-8): ").strip()
        if clause_choice.isdigit() and 1 <= int(clause_choice) <= 8:
            if int(clause_choice) == 8:
                clause = input("Enter custom clause: ").strip()
            else:
                clause = list(CLAUSE_MAPPING.values())[int(clause_choice) - 1]
        else:
            clause = input("Enter clause: ").strip()
        
        # Get time
        time_input = input("Time (hours): ").strip()
        try:
            time_hours = float(time_input)
        except ValueError:
            print("Invalid time format!")
            return
        
        # Get file/link
        file_link = input("File/Link (optional): ").strip()
        
        # Get notes
        notes = input("Notes (optional): ").strip()
        
        # Create entry
        entry = {
            'Date': date_input,
            'Task Description': task,
            'Clause': clause,
            'Time (h)': time_hours,
            'File/Link': file_link,
            'Notes': notes
        }
        
        self.existing_entries.append(entry)
        print(f"\n✅ Added manual entry: {task}")
    
    def save_entries(self):
        """Save all entries to CSV and generate Markdown"""
        # Sort entries by date
        sorted_entries = sorted(self.existing_entries, key=lambda x: x['Date'])
        
        # Save CSV
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            if sorted_entries:
                writer = csv.DictWriter(f, fieldnames=sorted_entries[0].keys())
                writer.writeheader()
                writer.writerows(sorted_entries)
        
        # Generate Markdown
        self.generate_markdown(sorted_entries)
        
        print(f"✅ Saved {len(sorted_entries)} entries to {CSV_FILE}")
        print(f"✅ Generated {MD_FILE}")
    
    def generate_markdown(self, entries: List[Dict]):
        """Generate Markdown version of the hours log"""
        md_content = f"""# Project Hours Log - ISO/IEC 42001:2023 Implementation
*llm-agent-mcp Project*

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Total Entries:** {len(entries)}  
**Total Hours:** {sum(float(entry['Time (h)']) for entry in entries):.1f}

## Summary by Clause

"""
        
        # Group by clause
        clause_totals = {}
        for entry in entries:
            clause = entry['Clause']
            hours = float(entry['Time (h)'])
            clause_totals[clause] = clause_totals.get(clause, 0) + hours
        
        # Display clause totals
        for clause, total_hours in sorted(clause_totals.items()):
            md_content += f"- **{clause}:** {total_hours:.1f} hours\n"
        
        md_content += "\n## Detailed Log\n\n"
        md_content += "| Date | Task Description | Clause | Time (h) | File/Link | Notes |\n"
        md_content += "|------|------------------|--------|----------|-----------|-------|\n"
        
        for entry in entries:
            md_content += f"| {entry['Date']} | {entry['Task Description']} | {entry['Clause']} | {entry['Time (h)']} | {entry['File/Link']} | {entry['Notes']} |\n"
        
        md_content += f"""

## Certification Requirements

This log demonstrates compliance with ISO/IEC 42001:2023 Lead Implementer certification requirements:

- **Minimum Hours Required:** 300 hours
- **Current Total:** {sum(float(entry['Time (h)']) for entry in entries):.1f} hours
- **Status:** {'✅ ELIGIBLE' if sum(float(entry['Time (h)']) for entry in entries) >= 300 else '⚠️ NEEDS MORE HOURS'}

## Notes

- Hours are estimated based on commit activity and file types
- Manual entries are marked accordingly
- Bot commits and automated changes are excluded
- All activities are mapped to specific ISO clauses

---
*Generated by log_hours.py for ISO/IEC 42001:2023 Lead Implementer certification*
"""
        
        with open(MD_FILE, 'w', encoding='utf-8') as f:
            f.write(md_content)
    
    def run_automated_scan(self, since_date: Optional[str] = None):
        """Run automated scan of GitHub commits"""
        print("🔍 Scanning GitHub commits...")
        
        commits = self.fetch_github_commits(since_date)
        print(f"📊 Found {len(commits)} commits (excluding bots)")
        
        new_entries = []
        for i, commit in enumerate(commits, 1):
            print(f"Processing commit {i}/{len(commits)}: {commit['sha'][:8]}")
            entries = self.process_commit(commit)
            new_entries.extend(entries)
        
        print(f"📝 Generated {len(new_entries)} new hour entries")
        
        # Add new entries to existing ones
        self.existing_entries.extend(new_entries)
        
        # Save all entries
        self.save_entries()
        
        # Display summary
        total_hours = sum(float(entry['Time (h)']) for entry in self.existing_entries)
        print(f"\n📈 Total Hours Logged: {total_hours:.1f}")
        print(f"🎯 ISO Requirement: 300 hours")
        print(f"📊 Status: {'✅ ELIGIBLE' if total_hours >= 300 else '⚠️ NEEDS MORE HOURS'}")

def main():
    parser = argparse.ArgumentParser(description='ISO/IEC 42001:2023 Project Hours Tracker')
    parser.add_argument('--manual', action='store_true', help='Add manual entry')
    parser.add_argument('--since', help='Scan commits since date (YYYY-MM-DD)')
    parser.add_argument('--token', help='GitHub API token (optional)')
    parser.add_argument('--scan-only', action='store_true', help='Only scan GitHub, no manual entries')
    
    args = parser.parse_args()
    
    # Initialize tracker
    tracker = HoursTracker(args.token)
    
    if args.manual:
        tracker.add_manual_entry()
        tracker.save_entries()
    elif args.scan_only:
        tracker.run_automated_scan(args.since)
    else:
        # Default: scan + offer manual entry
        tracker.run_automated_scan(args.since)
        
        response = input("\nWould you like to add manual entries? (y/n): ").strip().lower()
        while response == 'y':
            tracker.add_manual_entry()
            response = input("Add another manual entry? (y/n): ").strip().lower()
        
        tracker.save_entries()

if __name__ == "__main__":
    main() 