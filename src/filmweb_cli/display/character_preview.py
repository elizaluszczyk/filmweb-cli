from rich.panel import Panel
from rich.table import Table

from filmweb_cli.schemas.info.people_characters_info import CharacterContentResponse, CharacterInfo

from .console import console
from .formatters import prettify_camel_case


def print_character_preview(info: CharacterInfo, content_info: CharacterContentResponse) -> None:
    console.print(
        Panel(
            f"[dim cyan]{_build_metadata_line(info)}[/dim cyan]",
            title=_build_panel_title(info),
            title_align="left",
            expand=False,
            border_style="dim",
        ),
    )

    if content_info.known_for_titles:
        console.print("[bold green]You can see in:[/bold green]")

        for category, titles in content_info.known_for_titles.items():
            console.print(f"\n[dim cyan]{prettify_camel_case(category)}[/dim cyan]")

            table = Table(box=None, show_header=False, padding=(0, 2))
            table.add_column(style="dim", width=3)
            table.add_column()

            for i, title in enumerate(titles, 1):
                table.add_row(str(i), title)

            console.print(table)


def _build_panel_title(info: CharacterInfo) -> str:
    panel_title = f"[bold]{info.name}[/bold]"
    if info.real_name:
        panel_title += f" / [dim]{info.real_name}[/dim]"
    return panel_title


def _join_character_types(char_types: list) -> str:
    return " · ".join(char_type.name.text for char_type in char_types)


def _build_metadata_line(info: CharacterInfo) -> str:
    metadata = [
        _join_character_types(info.types),
        info.world.name if info.world else None,
    ]

    return " · ".join(filter(None, metadata))
