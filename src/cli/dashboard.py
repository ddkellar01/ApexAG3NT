from rich.console import Console
from rich.table import Table
from rich.panel import Panel

class ApexDashboard:
    """Renders a live, status-rich terminal dashboard for tracking multi-agent tasks."""

    def __init__(self):
        self.console = Console()

    def render_status(self, active_tasks: list, system_health: str = "OPTIMAL"):
        """Draws the live terminal dashboard UI."""
        table = Table(title="ApexAgent Execution Grid", show_header=True, header_style="bold magenta")
        table.add_column("Node ID", style="cyan")
        table.add_column("Model Assigned", style="green")
        table.add_column("Status", style="yellow")

        for task in active_tasks:
            table.add_row(task.get("id"), task.get("model"), task.get("status"))

        self.console.clear()
        self.console.print(Panel(f"System Health: [bold green]{system_health}[/bold green]", title="Apex Core Status"))
        self.console.print(table)
