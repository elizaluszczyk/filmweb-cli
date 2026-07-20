from rich.table import Table

from filmweb_cli.schemas.info.ranking import TopRole

from .console import console


def print_top_roles_preview(top_roles: list[TopRole], *, max_value: int) -> None:
    if not top_roles:
        console.print("[dim]No top roles available[/dim]")
        console.print()
        return

    console.print("[bold green]TOP ROLES[/bold green]")

    table = Table(box=None, show_header=True, header_style="bold", padding=(0, 2))
    table.add_column("Rank", style="dim", width=4)
    table.add_column("Person", no_wrap=True)
    table.add_column("ID", style="dim", width=8)
    table.add_column("Rate", justify="right")
    table.add_column("Votes", justify="right")

    for rank, role in enumerate(top_roles[:max_value], 1):
        table.add_row(
            str(rank),
            role.person_name,
            str(role.person_id),
            f"[bold magenta]{role.rate:.1f}[/bold magenta]",
            str(role.count),
        )

    console.print(table)
    console.print()
