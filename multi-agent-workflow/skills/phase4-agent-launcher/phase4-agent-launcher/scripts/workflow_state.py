#!/usr/bin/env python3
"""
Workflow State Management for Multi-Agent Workflow Skills
Handles reading/writing WORKFLOW_STATE.json in project directories
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

class WorkflowState:
    """Manages workflow state persistence"""
    
    STATE_FILE = "WORKFLOW_STATE.json"
    
    def __init__(self, project_path: str = "."):
        """Initialize with project path"""
        self.project_path = Path(project_path).resolve()
        self.state_file = self.project_path / self.STATE_FILE
        
    def exists(self) -> bool:
        """Check if state file exists"""
        return self.state_file.exists()
    
    def load(self) -> Dict[str, Any]:
        """Load state from file, return empty state if doesn't exist"""
        if not self.exists():
            return self._empty_state()
        
        try:
            with open(self.state_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"⚠️  Corrupt state file, creating fresh state")
            return self._empty_state()
    
    def save(self, state: Dict[str, Any]) -> None:
        """Save state to file"""
        state['last_updated'] = datetime.now().isoformat()
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def _empty_state(self) -> Dict[str, Any]:
        """Return empty state structure"""
        return {
            "project": self.project_path.name,
            "project_path": str(self.project_path),
            "phase": 0,
            "iteration": 0,
            "status": "not_started",
            "tech_stack": None,
            "agents": [],
            "history": [],
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
    
    def update_phase(self, phase: int, status: str = "in_progress") -> Dict[str, Any]:
        """Update current phase and status"""
        state = self.load()
        state['phase'] = phase
        state['status'] = status
        self.save(state)
        return state
    
    def complete_phase(self, phase: int) -> Dict[str, Any]:
        """Mark phase as complete"""
        state = self.load()
        state['history'].append({
            "phase": phase,
            "completed_at": datetime.now().isoformat()
        })
        state['status'] = f"phase_{phase}_complete"
        self.save(state)
        return state
    
    def add_agent(self, agent_id: int, role: str, status: str = "not_started") -> Dict[str, Any]:
        """Add agent to state"""
        state = self.load()
        agent = {
            "id": agent_id,
            "role": role,
            "status": status,
            "started_at": datetime.now().isoformat() if status != "not_started" else None,
            "completed_at": None,
            "pr_number": None
        }
        state['agents'].append(agent)
        self.save(state)
        return state
    
    def update_agent(self, agent_id: int, **kwargs) -> Dict[str, Any]:
        """Update agent status"""
        state = self.load()
        for agent in state['agents']:
            if agent['id'] == agent_id:
                agent.update(kwargs)
                if kwargs.get('status') == 'complete' and not agent.get('completed_at'):
                    agent['completed_at'] = datetime.now().isoformat()
                break
        self.save(state)
        return state
    
    def get_phase(self) -> int:
        """Get current phase number"""
        return self.load().get('phase', 0)
    
    def get_status(self) -> str:
        """Get current status"""
        return self.load().get('status', 'not_started')
    
    def get_agents(self) -> List[Dict[str, Any]]:
        """Get all agents"""
        return self.load().get('agents', [])
    
    def next_phase(self) -> int:
        """Get next phase number based on current state"""
        current_phase = self.get_phase()
        status = self.get_status()
        
        # If phase complete, move to next
        if "complete" in status:
            return current_phase + 1
        else:
            return current_phase
    
    def format_status(self) -> str:
        """Format current status for display"""
        state = self.load()
        phase = state.get('phase', 0)
        iteration = state.get('iteration', 0)
        status = state.get('status', 'not_started')
        
        output = [
            f"📊 {state.get('project', 'Unknown Project')}",
            f"Phase: {phase} | Iteration: {iteration}",
            f"Status: {status}",
            ""
        ]
        
        # Show completed phases
        history = state.get('history', [])
        if history:
            output.append("✅ Completed:")
            for h in history[-5:]:  # Last 5
                output.append(f"   Phase {h['phase']}")
        
        # Show active agents
        agents = state.get('agents', [])
        active = [a for a in agents if a.get('status') in ['in_progress', 'not_started']]
        complete = [a for a in agents if a.get('status') == 'complete']
        
        if complete:
            output.append("")
            output.append(f"✅ Agents Complete: {len(complete)}")
            for a in complete:
                pr = f"PR #{a.get('pr_number')}" if a.get('pr_number') else ""
                output.append(f"   Agent {a['id']}: {a['role']} {pr}")
        
        if active:
            output.append("")
            output.append(f"🔄 Agents Active: {len(active)}")
            for a in active:
                output.append(f"   Agent {a['id']}: {a['role']} - {a.get('status', 'unknown')}")
        
        return "\n".join(output)


def main():
    """CLI for testing"""
    import sys
    if len(sys.argv) < 2:
        print("Usage: workflow_state.py <project_path> [command]")
        sys.exit(1)
    
    ws = WorkflowState(sys.argv[1])
    
    if len(sys.argv) == 2:
        # Just show status
        print(ws.format_status())
    else:
        command = sys.argv[2]
        if command == "init":
            ws.save(ws._empty_state())
            print("✅ Initialized state file")
        elif command == "load":
            print(json.dumps(ws.load(), indent=2))


if __name__ == "__main__":
    main()
