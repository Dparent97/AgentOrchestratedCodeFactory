"""
Main CLI entry point for the Code Factory

Provides commands to initialize, check status, and run the factory.
"""

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from code_factory import __version__
from code_factory.core.agent_runtime import AgentRuntime
from code_factory.core.orchestrator import Orchestrator
from code_factory.agents.planner import PlannerAgent
from code_factory.agents.architect import ArchitectAgent
from code_factory.agents.implementer import ImplementerAgent
from code_factory.agents.tester import TesterAgent
from code_factory.agents.doc_writer import DocWriterAgent
from code_factory.agents.git_ops import GitOpsAgent
from code_factory.agents.blue_collar_advisor import BlueCollarAdvisor
from code_factory.agents.safety_guard import SafetyGuard

app = typer.Typer(
    name="code-factory",
    help="Agent-Orchestrated Code Factory - Transform ideas into software",
    add_completion=False
)
console = Console()


def get_runtime() -> AgentRuntime:
    """Initialize and return runtime with all agents registered"""
    runtime = AgentRuntime()
    
    # Register all agents
    runtime.register_agent(SafetyGuard())
    runtime.register_agent(PlannerAgent())
    runtime.register_agent(ArchitectAgent())
    runtime.register_agent(ImplementerAgent())
    runtime.register_agent(TesterAgent())
    runtime.register_agent(DocWriterAgent())
    runtime.register_agent(GitOpsAgent())
    runtime.register_agent(BlueCollarAdvisor())
    
    return runtime


@app.command()
def init():
    """
    Initialize or verify the factory environment
    
    Checks that Python version, directories, and configuration are correct.
    Creates any missing directories or files.
    """
    console.print("\n[bold blue]Initializing Code Factory...[/bold blue]\n")
    
    # Check Python version
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    if sys.version_info < (3, 11):
        console.print(f"[red]✗[/red] Python {py_version} (requires 3.11+)")
        raise typer.Exit(1)
    else:
        console.print(f"[green]✓[/green] Python {py_version}")
    
    # Check project structure
    project_root = Path(__file__).parent.parent.parent.parent
    required_dirs = [
        "src/code_factory/core",
        "src/code_factory/agents",
        "src/code_factory/cli",
        "docs",
        "tests/unit",
        "tests/integration",
        "tests/e2e"
    ]
    
    all_present = True
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        if full_path.exists():
            console.print(f"[green]✓[/green] {dir_path}")
        else:
            console.print(f"[red]✗[/red] {dir_path} (missing)")
            all_present = False
    
    # Check Git
    git_dir = project_root / ".git"
    if git_dir.exists():
        console.print(f"[green]✓[/green] Git repository initialized")
    else:
        console.print(f"[yellow]![/yellow] Git not initialized")
    
    # Summary
    console.print()
    if all_present:
        console.print("[bold green]🎉 Factory is ready to use![/bold green]")
    else:
        console.print("[bold yellow]⚠️  Some components are missing[/bold yellow]")
        console.print("Please ensure all directories are present.")


@app.command()
def status():
    """
    Display current factory status and environment info
    
    Shows Python version, Git status, available agents, and system information.
    """
    console.print(f"\n[bold]Agent-Orchestrated Code Factory v{__version__}[/bold]")
    console.print("=" * 60 + "\n")
    
    # Environment section
    console.print("[bold cyan]Environment:[/bold cyan]")
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    py_path = sys.executable
    console.print(f"  Python: {py_version} ({py_path})")
    
    project_root = Path(__file__).parent.parent.parent.parent
    console.print(f"  Working Directory: {project_root}")
    
    # Git status
    git_dir = project_root / ".git"
    if git_dir.exists():
        console.print(f"  Git: Initialized ✓")
    else:
        console.print(f"  Git: Not initialized")
    
    # Projects directory
    projects_dir = Path("/Users/dp/Projects")
    if projects_dir.exists():
        console.print(f"  Projects Directory: {projects_dir} ✓")
    else:
        console.print(f"  Projects Directory: {projects_dir} (not found)")
    
    console.print()
    
    # Agents section
    console.print("[bold cyan]Available Agents:[/bold cyan]")
    runtime = get_runtime()
    agents = runtime.list_agents()
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Agent", style="cyan", no_wrap=True)
    table.add_column("Description")
    
    for agent_name, description in agents.items():
        table.add_row(agent_name, description)
    
    console.print(table)
    console.print()
    
    # Execution history
    history = runtime.get_execution_history()
    console.print(f"[bold cyan]Execution History:[/bold cyan] {len(history)} runs")
    
    console.print()
    console.print("[bold green]Status: Ready ✅[/bold green]\n")


@app.command()
def version():
    """Show version information"""
    console.print(f"Code Factory version {__version__}")


if __name__ == "__main__":
    app()
