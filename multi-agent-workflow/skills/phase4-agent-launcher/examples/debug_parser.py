#!/usr/bin/env python3
import sys
import json
sys.path.insert(0, '../phase4-agent-launcher/scripts')
from launcher import AgentLauncher

# Test parsing
with open('example_progress_reports.txt', 'r') as f:
    reports = f.read()

launcher = AgentLauncher('.')
parsed = launcher._parse_reports(reports)

print("Parsed Reports:")
print(json.dumps(parsed, indent=2))
