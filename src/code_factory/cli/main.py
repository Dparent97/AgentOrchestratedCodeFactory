"""
Main CLI entry point for the Code Factory

Provides commands to initialize, check status, and run the factory.
"""

import sys
import time
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from code_factory import __version__
from code_factory.core.agent_runtime import AgentRuntime
from code_factory.core.config import get_config, load_config
from code_factory.core.models import Idea
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
    
    # Configuration
    config = get_config()
    console.print(f"  Projects Directory: {config.projects_dir}")
    console.print(f"  Checkpoint Directory: {config.checkpoint_dir}")
    console.print(f"  Agent Timeout: {config.default_agent_timeout}s")
    
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


@app.command()
def generate(
    description: str = typer.Argument(..., help="Project description - what to build"),
    output_dir: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output directory for the generated project"
    ),
    features: Optional[List[str]] = typer.Option(
        None, "--feature", "-f", help="Features to include (can be repeated)"
    ),
    target_users: Optional[List[str]] = typer.Option(
        None, "--target-user", "-t", help="Target user roles (can be repeated)"
    ),
    environment: Optional[str] = typer.Option(
        None, "--env", "-e", help="Target environment (e.g., 'offline', 'low-bandwidth')"
    ),
):
    """
    Generate a project from a description
    
    Transform your idea into a complete project with code, tests, and documentation.
    
    Examples:
        code-factory generate "CLI tool to manage docker containers"
        code-factory generate "REST API for inventory" -f "authentication" -f "pagination"
        code-factory generate "mobile checklist app" -t "field engineer" -e "offline"
    """
    console.print()
    console.print(
        Panel(
            f"[bold]{description}[/bold]",
            title="🏭 Code Factory",
            subtitle="Transforming idea into project",
        )
    )
    console.print()

    # Create the Idea from CLI arguments
    idea = Idea(
        description=description,
        features=features or [],
        target_users=target_users or [],
        environment=environment,
    )

    # Initialize runtime and orchestrator
    runtime = get_runtime()
    config = get_config()
    
    # Override output directory if specified
    if output_dir:
        config.projects_dir = output_dir
    
    orchestrator = Orchestrator(runtime=runtime, config=config)

    # Run the factory with progress display
    start_time = time.time()
    
    with console.status("[bold blue]Generating project...[/bold blue]", spinner="dots"):
        try:
            result = orchestrator.run_factory(idea)
        except Exception as e:
            console.print(f"\n[bold red]✗ Error:[/bold red] {e}")
            raise typer.Exit(1)

    elapsed = time.time() - start_time

    # Display results
    console.print()
    if result.success:
        console.print("[bold green]✓ Project generated successfully![/bold green]\n")
        
        # Summary table
        table = Table(title="Generation Summary", show_header=False, box=None)
        table.add_column("Property", style="cyan")
        table.add_column("Value")
        
        table.add_row("Project Name", result.project_name)
        if result.project_path:
            table.add_row("Location", result.project_path)
        table.add_row("Time", f"{elapsed:.1f}s")
        table.add_row("Agents Run", str(len(result.agent_runs)))
        if result.git_repo_url:
            table.add_row("Repository", result.git_repo_url)
        
        console.print(table)
        console.print()
        
        # Show agent execution summary if any
        if result.agent_runs:
            console.print("[bold cyan]Pipeline Stages:[/bold cyan]")
            for run in result.agent_runs:
                status_icon = "✓" if run.status == "success" else "✗" if run.status == "failed" else "○"
                status_color = "green" if run.status == "success" else "red" if run.status == "failed" else "yellow"
                duration = f" ({run.duration_seconds:.1f}s)" if run.duration_seconds else ""
                console.print(f"  [{status_color}]{status_icon}[/{status_color}] {run.agent_name}{duration}")
            console.print()
        
        # Next steps
        if result.project_path:
            console.print("[bold]Next steps:[/bold]")
            console.print(f"  cd {result.project_path}")
            console.print("  # Review generated code and tests")
            console.print()
    else:
        console.print("[bold red]✗ Project generation failed[/bold red]\n")
        
        if result.errors:
            console.print("[bold red]Errors:[/bold red]")
            for error in result.errors:
                console.print(f"  • {error}")
            console.print()
        
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
