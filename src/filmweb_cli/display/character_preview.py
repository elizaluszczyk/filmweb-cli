from rich.panel import Panel

from filmweb_cli.display.console import console
from filmweb_cli.schemas.info.people_characters_info import CharacterInfo


def print_character_preview(info: CharacterInfo) -> None:
    console.print(
        Panel(
            f"[dim cyan]{_build_metadata_line(info)}[/dim cyan]",
            title=_build_panel_title(info),
            title_align="left",
            expand=False,
            border_style="dim",
        ),
    )


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
