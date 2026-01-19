import datetime

from rich.panel import Panel
from rich.table import Table

from filmweb_cli.display.console import console
from filmweb_cli.schemas.info.people_characters_info import PersonInfo


def print_person_preview(info: PersonInfo) -> None:
    console.print(
        Panel(
            f"[dim cyan]{_build_metadata_line(info)}[/dim cyan]",
            title=_build_panel_title(info),
            title_align="left",
            expand=False,
            border_style="dim",
        ),
    )

    has_details = False

    if info.birthplace:
        place = _format_birthplace(info)
        if place:
            console.print(f"[bold]Birthplace:[/bold] {place}")
            has_details = True

    if info.details and info.details.height:
        console.print(f"[bold]Height:[/bold] {info.details.height} cm")
        has_details = True

    if info.known_for_titles:
        if has_details:
            console.print()

        console.print("[bold green]Known for:[/bold green]")
        table = Table(box=None, show_header=False, padding=(0, 2))
        table.add_column(style="dim", width=3)
        table.add_column()

        for i, title in enumerate(info.known_for_titles, 1):
            table.add_row(str(i), title)

        console.print(table)


def _build_panel_title(info: PersonInfo) -> str:
    panel_title = f"[bold]{info.name}[/bold]"
    if info.details and info.details.real_name:
        panel_title += f" / [dim]{info.details.real_name}[/dim]"
    return panel_title


def _build_metadata_line(info: PersonInfo) -> str:
    birth = info.details.birth_date_int if info.details else None
    death = info.details.death_date_int if info.details else None

    age = _calculate_person_age(birth, death) if birth else None

    age_str = None
    if age is not None:
        age_str = f"✝ {age}" if death else f"{age} years old"

    date_str = _format_date_range(birth, death) if birth else None

    metadata = [
        info.main_profession or None,
        age_str,
        date_str,
    ]

    return " · ".join(filter(None, metadata))


def _format_date_range(birth_date_int: int, death_date_int: int | None) -> str:
    birth_str = _format_date_part(birth_date_int)

    if death_date_int:
        death_str = _format_date_part(death_date_int)
        return f"{birth_str} - {death_str}"

    return birth_str


def _format_date_part(date_int: int) -> str:
    date_str = str(date_int)

    year = date_str[:4]
    month = date_str[4:6]
    day = date_str[6:8]

    return f"{day}.{month}.{year}"


def _calculate_person_age(birth_date_int: int, death_date_int: int | None) -> int:
    birth_date_str = str(birth_date_int)
    birth_year = int(birth_date_str[:4])
    birth_month = int(birth_date_str[4:6])
    birth_day = int(birth_date_str[6:8])

    if death_date_int:
        death_date_str = str(death_date_int)
        end_year = int(death_date_str[:4])
        end_month = int(death_date_str[4:6])
        end_day = int(death_date_str[6:8])
    else:
        today = datetime.datetime.now(datetime.UTC).date()
        end_year = today.year
        end_month = today.month
        end_day = today.day

    age = end_year - birth_year

    if (end_month, end_day) < (birth_month, birth_day):
        age -= 1

    return age


def _format_birthplace(info: PersonInfo) -> str | None:
    if not info.birthplace:
        return None

    parts = [
        info.birthplace.city_name or None,
        info.birthplace.region_name or None,
    ]

    valid_parts = list(filter(None, parts))

    return ", ".join(valid_parts) if valid_parts else None
