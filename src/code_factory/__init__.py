"""
Agent-Orchestrated Code Factory

A meta-agent system that transforms plain-language ideas into
complete, tested, and documented software projects.

Focus: Building practical tools for blue-collar and technical workers
(marine engineers, plant operators, mechanics, HVAC technicians, etc.)
"""

__version__ = "0.1.0"
__author__ = "Agent Code Factory Team"

from code_factory.core.models import Idea, ProjectSpec, Task, AgentRun

__all__ = ["Idea", "ProjectSpec", "Task", "AgentRun"]
