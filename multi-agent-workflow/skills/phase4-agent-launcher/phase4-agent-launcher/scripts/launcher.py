#!/usr/bin/env python3
"""
Phase 4: Agent Launcher & Progress Management
Launches parallel agents and manages sprint-based progress tracking
"""
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from workflow_state import WorkflowState


class AgentLauncher:
    """Manages agent launch and progress tracking"""

    def __init__(self, project_path: str = "."):
        """Initialize launcher with project path"""
        self.project_path = Path(project_path).resolve()
        self.ws = WorkflowState(project_path)
        self.agent_prompts_dir = self.project_path / "AGENT_PROMPTS"

    def launch_agents(self, sprint_duration: int = 60) -> None:
        """
        Function 1: Initial Launch
        Displays ready-to-copy prompts for each agent from Phase 3

        Args:
            sprint_duration: Sprint duration in minutes (default: 60)
        """
        # Load workflow state
        state = self.ws.load()
        agents = state.get('agents', [])

        if not agents:
            print("❌ No agents found in workflow state")
            print("💡 Run Phase 3 (codex-review) first to generate agent definitions")
            return

        # Get repository URL
        repo_url = state.get('repo_url', self._detect_repo_url())

        # Display launch header
        print(f"\n🚀 Launching {len(agents)} Agents in Parallel\n")
        print("="*70)
        print(f"📍 Project: {state.get('project', 'Unknown')}")
        print(f"🔗 Repository: {repo_url}")
        print(f"⏱️  Sprint Duration: {sprint_duration} minutes")
        print("="*70)

        print("\n📋 Instructions:")
        print("1. Copy each prompt below to a SEPARATE Claude chat window")
        print("2. Let each agent work independently for the sprint duration")
        print("3. After the sprint, ask each agent: 'Give me a progress report'")
        print("4. Paste all reports back here for evaluation\n")

        print("="*70)

        # Generate and display prompts for each agent
        for agent in agents:
            agent_id = agent['id']
            role = agent['role']

            print(f"\n{'='*70}")
            print(f"💬 Agent {agent_id}: {role}")
            print(f"{'='*70}\n")

            # Find agent prompt file
            prompt_file = self._find_agent_prompt(agent_id, role)

            if prompt_file:
                prompt_path = f"AGENT_PROMPTS/{prompt_file.name}"
            else:
                prompt_path = f"AGENT_PROMPTS/{agent_id}_{self._role_to_filename(role)}.md"
                print(f"⚠️  Prompt file not found: {prompt_path}")

            # Generate copy-paste prompt
            launch_prompt = self._generate_launch_prompt(
                agent_id, role, repo_url, prompt_path
            )
            print(launch_prompt)
            print(f"\n{'-'*70}\n")

            # Update agent status to in_progress
            self.ws.update_agent(agent_id, status='in_progress')

        # Display next steps
        print("\n" + "="*70)
        print("✅ All agent prompts generated!")
        print(f"\n⏰ SET TIMER: {sprint_duration} minutes")
        print(f"\n➡️  After {sprint_duration} minutes:")
        print("   1. Ask each agent: 'Give me a progress report'")
        print("   2. Paste all reports here")
        print("   3. Run progress evaluation to adjust next sprint")
        print("="*70 + "\n")

        # Update phase status
        self.ws.update_phase(4, "agents_launched")

    def evaluate_progress(self, reports: str, next_sprint_duration: int = 60) -> None:
        """
        Function 2: Progress Check & Re-Evaluation
        Analyzes agent progress reports and generates updated prompts

        Args:
            reports: Raw text containing all agent progress reports
            next_sprint_duration: Duration for next sprint in minutes
        """
        print("\n📊 Analyzing Agent Progress Reports\n")
        print("="*70)

        # Parse reports
        parsed_reports = self._parse_reports(reports)

        if not parsed_reports:
            print("❌ No valid progress reports found")
            print("\n💡 Progress report should follow this format:")
            self._show_report_template()
            return

        print(f"✅ Found {len(parsed_reports)} agent reports\n")

        # Analyze each agent's progress
        evaluations = []
        for report in parsed_reports:
            evaluation = self._evaluate_agent_progress(report)
            evaluations.append(evaluation)

            # Display analysis
            status_icon = {
                'ahead': '🚀',
                'on_track': '✅',
                'behind': '⚠️',
                'blocked': '🚫'
            }.get(evaluation['status'], '❓')

            print(f"{status_icon} Agent {report['agent_id']}: {report.get('role', 'Unknown')}")
            print(f"   Status: {evaluation['status'].upper()}")
            print(f"   Action: {evaluation['action']}")

            if evaluation.get('note'):
                print(f"   Note: {evaluation['note']}")
            print()

            # Update workflow state
            agent_status = 'blocked' if evaluation['status'] == 'blocked' else 'in_progress'
            self.ws.update_agent(report['agent_id'], status=agent_status)

        # Generate updated prompts for next sprint
        print("\n" + "="*70)
        print(f"🔄 Updated Prompts for Next {next_sprint_duration}-Minute Sprint")
        print("="*70 + "\n")

        for i, (report, evaluation) in enumerate(zip(parsed_reports, evaluations)):
            print(f"\n{'='*70}")
            print(f"💬 Agent {report['agent_id']}: {report.get('role', 'Unknown')} (Updated)")
            print(f"{'='*70}\n")

            updated_prompt = self._generate_updated_prompt(
                report, evaluation, next_sprint_duration
            )
            print(updated_prompt)
            print(f"\n{'-'*70}\n")

        # Check if all agents are complete
        if all(report.get('complete', False) for report in parsed_reports):
            print("\n" + "="*70)
            print("🎉 ALL AGENTS COMPLETE!")
            print("="*70)

            state = self.ws.load()
            for agent in state.get('agents', []):
                pr_num = agent.get('pr_number', 'pending')
                print(f"✅ Agent {agent['id']}: {agent['role']} - PR #{pr_num}")

            self.ws.complete_phase(4)
            print("\n➡️  Next: Run phase5-integration to merge all PRs")
            print("="*70 + "\n")
        else:
            print("\n" + "="*70)
            print(f"⏰ Continue work for {next_sprint_duration} minutes")
            print("\nThen check progress again with another report cycle")
            print("="*70 + "\n")

    def _detect_repo_url(self) -> str:
        """Detect GitHub repository URL from git config"""
        try:
            import subprocess
            result = subprocess.run(
                ['git', 'config', '--get', 'remote.origin.url'],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                url = result.stdout.strip()
                # Convert SSH to HTTPS if needed
                if url.startswith('git@github.com:'):
                    url = url.replace('git@github.com:', 'https://github.com/')
                if url.endswith('.git'):
                    url = url[:-4]
                return url
        except Exception:
            pass
        return "https://github.com/user/repo"

    def _find_agent_prompt(self, agent_id: int, role: str) -> Optional[Path]:
        """Find the agent prompt file in AGENT_PROMPTS directory"""
        if not self.agent_prompts_dir.exists():
            return None

        # Try multiple patterns
        patterns = [
            f"{agent_id}_{self._role_to_filename(role)}.md",
            f"{agent_id}_*.md",
            f"*{role.lower().replace(' ', '_')}*.md"
        ]

        for pattern in patterns:
            matches = list(self.agent_prompts_dir.glob(f"**/{pattern}"))
            if matches:
                return matches[0]

        return None

    def _role_to_filename(self, role: str) -> str:
        """Convert role name to filename format"""
        return role.lower().replace(' ', '_').replace('-', '_')

    def _generate_launch_prompt(self, agent_id: int, role: str,
                                repo_url: str, prompt_path: str) -> str:
        """Generate copy-paste prompt for agent launch"""
        return f"""You are Agent {agent_id}: {role}

Repository: {repo_url}

📋 Instructions:
1. Clone the repository: git clone {repo_url}
2. Read your detailed instructions: {prompt_path}
3. Follow the role definition and complete assigned tasks
4. Create a PR when ready
5. Provide progress reports when asked

START NOW - Work independently and follow your role's guidelines.
"""

    def _parse_reports(self, reports_text: str) -> List[Dict[str, Any]]:
        """Parse progress reports from text"""
        parsed = []
        current_report = {}
        current_section = None

        lines = reports_text.strip().split('\n')

        for line in lines:
            line = line.strip()

            if not line:
                continue

            # Detect agent header
            if line.lower().startswith('agent') and ':' in line:
                if current_report:
                    parsed.append(current_report)

                # Extract agent ID
                try:
                    agent_part = line.split(':')[0]
                    agent_id = int(''.join(filter(str.isdigit, agent_part)))
                    role_part = line.split(':', 1)[1].strip() if ':' in line else ''
                    current_report = {
                        'agent_id': agent_id,
                        'role': role_part,
                        'done': [],
                        'working_on': [],
                        'blocked_by': [],
                        'next': [],
                        'complete': False
                    }
                    current_section = None
                except (ValueError, IndexError):
                    continue
                continue

            # Skip if no active report
            if not current_report:
                continue

            # Detect section headers
            if '✅' in line or line.lower().startswith('done'):
                current_section = 'done'
                # Check if content is on same line
                content = line
                for marker in ['✅', 'Done:', 'done:']:
                    content = content.replace(marker, '')
                content = content.strip('- ').strip()
                if content and content.lower() not in ['done', 'none']:
                    current_report[current_section].append(content)
                continue

            elif '🔄' in line or 'working' in line.lower():
                current_section = 'working_on'
                content = line
                for marker in ['🔄', 'Working on:', 'working on:', 'Working:', 'working:']:
                    content = content.replace(marker, '')
                content = content.strip('- ').strip()
                if content and 'working' not in content.lower():
                    current_report[current_section].append(content)
                continue

            elif '⚠️' in line or 'blocked' in line.lower():
                current_section = 'blocked_by'
                content = line
                for marker in ['⚠️', 'Blocked by:', 'blocked by:', 'Blocked:', 'blocked:']:
                    content = content.replace(marker, '')
                content = content.strip('- ').strip()
                # Only add if not empty and not just "None"
                if content and content.lower() not in ['none', 'blocked', 'blocked by', 'n/a', 'na']:
                    current_report[current_section].append(content)
                continue

            elif '⏭️' in line or 'next' in line.lower():
                current_section = 'next'
                content = line
                for marker in ['⏭️', 'Next:', 'next:']:
                    content = content.replace(marker, '')
                content = content.strip('- ').strip()
                if content and content.lower() not in ['next']:
                    current_report[current_section].append(content)
                continue

            # Check for completion status (but only if line explicitly indicates completion)
            elif line.lower() in ['complete', 'finished', 'done', 'completed', 'all done'] or \
                 line.lower().startswith('status:') and ('complete' in line.lower() or 'finished' in line.lower()):
                current_report['complete'] = True
                current_section = None
                continue

            # Add content to current section if it starts with '-' or is continuation
            elif current_section and (line.startswith('-') or line[0].isalpha() or line[0].isdigit()):
                content = line.strip('- ').strip()
                # Filter out "None" from blocked_by section
                if content:
                    if current_section == 'blocked_by' and content.lower() in ['none', 'n/a', 'na']:
                        continue
                    current_report[current_section].append(content)

        # Add last report
        if current_report:
            parsed.append(current_report)

        return parsed

    def _evaluate_agent_progress(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate agent progress and determine action"""

        # Check if blocked (filter out "None" entries)
        blockers = [b for b in report.get('blocked_by', []) if b and b.lower() not in ['none', 'n/a', 'na']]
        if blockers:
            return {
                'status': 'blocked',
                'action': 'Provide workaround or redirect to different task',
                'note': f"Blocked by: {', '.join(blockers)}"
            }

        # Check if complete
        if report.get('complete'):
            return {
                'status': 'complete',
                'action': 'Agent finished - ready for PR merge',
                'note': 'Well done!'
            }

        # Assess progress
        done_count = len(report.get('done', []))
        working_count = len(report.get('working_on', []))

        if done_count >= 3:
            return {
                'status': 'ahead',
                'action': 'Add stretch goal or bonus task',
                'note': f'{done_count} tasks completed - excellent progress'
            }
        elif done_count >= 1:
            return {
                'status': 'on_track',
                'action': 'Continue current plan',
                'note': 'Good progress, stay on track'
            }
        else:
            return {
                'status': 'behind',
                'action': 'Simplify scope or extend time',
                'note': 'Limited progress - may need support'
            }

    def _generate_updated_prompt(self, report: Dict[str, Any],
                                 evaluation: Dict[str, Any],
                                 duration: int) -> str:
        """Generate updated prompt for next sprint"""
        agent_id = report['agent_id']
        role = report.get('role', 'Unknown')
        status = evaluation['status']

        prompt_parts = [f"Continue your work as {role}\n"]

        # Add progress summary
        if report.get('done'):
            prompt_parts.append("✅ Completed:")
            for item in report['done']:
                prompt_parts.append(f"   - {item}")
            prompt_parts.append("")

        # Add current work status
        if report.get('working_on'):
            prompt_parts.append("🔄 In Progress:")
            for item in report['working_on']:
                prompt_parts.append(f"   - {item}")
            prompt_parts.append("")

        # Add directive based on evaluation
        if status == 'blocked':
            prompt_parts.append("🔄 NEW DIRECTION:")
            prompt_parts.append(f"   Your blocker: {', '.join(report.get('blocked_by', []))}")
            prompt_parts.append("   → Switch to different task while waiting")
            if report.get('next'):
                prompt_parts.append(f"   → Work on: {report['next'][0]}")

        elif status == 'ahead':
            prompt_parts.append("🚀 STRETCH GOAL:")
            prompt_parts.append("   You're ahead of schedule! Add bonus task:")
            if report.get('next'):
                prompt_parts.append(f"   → {report['next'][0]}")
                if len(report['next']) > 1:
                    prompt_parts.append(f"   → {report['next'][1]}")
            else:
                prompt_parts.append("   → Improve code quality, add tests, or refactor")

        elif status == 'behind':
            prompt_parts.append("⚠️ SIMPLIFIED SCOPE:")
            prompt_parts.append("   Focus on core functionality first")
            if report.get('next'):
                prompt_parts.append(f"   → Priority: {report['next'][0]}")
            prompt_parts.append("   → Skip nice-to-haves for now")

        else:  # on_track
            prompt_parts.append("✅ CONTINUE:")
            if report.get('next'):
                prompt_parts.append(f"   → Next task: {report['next'][0]}")
            else:
                prompt_parts.append("   → Continue current work")

        prompt_parts.append(f"\n⏱️  Time: {duration} minutes")
        prompt_parts.append("\n💡 Provide progress report when this sprint ends")

        return '\n'.join(prompt_parts)

    def _show_report_template(self) -> None:
        """Display progress report template"""
        template = """
Agent [N] - [Role Name]

✅ Done:
- Task 1 completed
- Task 2 completed

🔄 Working on:
- Current task (X% complete)

⚠️ Blocked by:
- [Issue description, or "None"]

⏭️ Next:
- Planned next task
"""
        print(template)

    def show_status(self) -> None:
        """Display current workflow status"""
        print(self.ws.format_status())


def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Phase 4: Agent Launcher & Progress Management")
        print("\nUsage:")
        print("  python launcher.py <project_path> launch [sprint_duration]")
        print("  python launcher.py <project_path> evaluate <reports_file> [next_sprint_duration]")
        print("  python launcher.py <project_path> status")
        print("\nExamples:")
        print("  python launcher.py . launch 60")
        print("  python launcher.py . evaluate reports.txt 90")
        print("  python launcher.py . status")
        sys.exit(1)

    project_path = sys.argv[1]
    launcher = AgentLauncher(project_path)

    if len(sys.argv) < 3:
        launcher.show_status()
        return

    command = sys.argv[2].lower()

    if command == 'launch':
        sprint_duration = int(sys.argv[3]) if len(sys.argv) > 3 else 60
        launcher.launch_agents(sprint_duration)

    elif command == 'evaluate':
        if len(sys.argv) < 4:
            print("❌ Error: Please provide reports file or text")
            sys.exit(1)

        reports_input = sys.argv[3]
        next_duration = int(sys.argv[4]) if len(sys.argv) > 4 else 60

        # Check if it's a file
        if os.path.exists(reports_input):
            with open(reports_input, 'r') as f:
                reports_text = f.read()
        else:
            # Treat as direct text
            reports_text = reports_input

        launcher.evaluate_progress(reports_text, next_duration)

    elif command == 'status':
        launcher.show_status()

    else:
        print(f"❌ Unknown command: {command}")
        print("Valid commands: launch, evaluate, status")
        sys.exit(1)


if __name__ == "__main__":
    main()
