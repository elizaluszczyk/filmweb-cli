from collections.abc import Sequence
from typing import Protocol

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from filmweb_cli.schemas.info.info import ContentInfo, FullDescription
from filmweb_cli.schemas.info.rating import ContentRating, Rating
from filmweb_cli.schemas.vod.vod_providers import WhereToWatch

console = Console(width=85, highlight=False)

THOUSAND_THRESHOLD = 1000


class Displayable(Protocol):
    def display_name(self) -> str: ...
    def get_id(self) -> str: ...


def print_search_results(categories: list[tuple[str, Sequence[Displayable]]]) -> None:
    has_results = False
    for name, items in categories:
        if not items:
            continue
        has_results = True

        console.print(f"[bold cyan]{name}[/bold cyan]")
        table = Table(box=None, show_header=False, padding=(0, 2))
        table.add_column(style="dim", width=3)
        table.add_column()

        for i, item in enumerate(items, 1):
            table.add_row(str(i), item.display_name(), item.get_id())

        console.print(table)
        console.print()

    if not has_results:
        console.print("[dim]No results found.[/dim]")


def print_preview(
    info: ContentInfo, rating: ContentRating, critics_rating: Rating, description: FullDescription, *, full_desc: bool,
) -> None:
    title = info.title.title if info.title else info.original_title.title
    original = info.original_title.title

    console.print(
        Panel(
            f"[dim cyan]{_build_metadata_line(info)}[/dim cyan]",
            title=_build_panel_title(title, original),
            title_align="left",
            expand=False,
            border_style="dim",
        ),
    )

    if rating:
        console.print(
            f"[bold magenta]★ {rating.rate:.1f}[/bold magenta][dim] · {_format_count(rating.count)}[/dim]",
        )

    if critics_rating:
        console.print(
            f"[bold green]☆ {critics_rating.rate:.1f}[/bold green][dim] · {critics_rating.count} critics[/dim]",
        )
        console.print()

    if info.directors:
        console.print(f"[bold]Directors:[/bold] {_join_names(info.directors)}")

    if info.main_cast:
        console.print(f"[bold]Main cast:[/bold] {_join_names(info.main_cast)}")

    if full_desc:
        console.print()

        clean_full_description = " ".join(description.text.split())
        console.print(clean_full_description)
    elif info.description:
        console.print()

        clean_description = " ".join(info.description.split())
        console.print(clean_description)


def _format_count(count: int) -> str:
    return f"{count / 1000:.0f}k ratings" if count >= THOUSAND_THRESHOLD else str(count)


def _join_names(items: list) -> str:
    return ", ".join(item.name for item in items)


def _build_panel_title(title: str, original: str) -> str:
    panel_title = f"[bold]{title}[/bold]"
    if title != original:
        panel_title += f" / [dim]{original}[/dim]"
    return panel_title


def _build_metadata_line(info: ContentInfo) -> str:
    metadata = [
        str(info.year) if info.year else None,
        f"{info.duration} min" if info.duration else None,
        _join_names(info.genres) if info.genres else None,
    ]
    return " · ".join(filter(None, metadata))


def print_where_to_watch(where_to_watch_list: list[WhereToWatch]) -> None:
    console.print()

    if not where_to_watch_list:
        console.print("[dim]No streaming information available.[/dim]")
        return

    subscription, rent, buy, free = _group_providers(where_to_watch_list)

    def print_category_with_price(title: str, style: str, items: dict[str, list[int]]) -> None:
        if not items:
            return

        console.print(f"[bold {style}]● {title}[/bold {style}]")

        sorted_items = sorted(
            items.items(),
            key=lambda x: min(x[1]) if x[1] else float("inf"),
        )
        for name, prices in sorted_items:
            if prices:
                best_price = min(prices) / 100
                console.print(f"  {name} [dim]· {best_price:.2f} PLN[/dim]")
            else:
                console.print(f"  {name}")
        console.print()

    def print_category(title: str, style: str, items: set[str]) -> None:
        if not items:
            return

        console.print(f"[bold {style}]● {title}[/bold {style}]")
        for name in sorted(items):
            console.print(f"  {name}")
        console.print()

    print_category_with_price("Subscription", "green", subscription)
    print_category_with_price("Rent", "yellow", rent)
    print_category_with_price("Buy", "magenta", buy)
    print_category("Free", "blue", free)

    if not any([subscription, free, rent, buy]):
        console.print("[dim]No streaming options found.[/dim]")


def print_where_to_watch_compact(where_to_watch_list: list[WhereToWatch]) -> None:
    console.print()

    if not where_to_watch_list:
        console.print("[dim]No streaming information available.[/dim]")
        return

    subscription, rent, buy, free = _group_providers(where_to_watch_list)

    def print_category(title: str, style: str, items: dict[str, list[int]] | set[str]) -> None:
        if not items:
            return

        category_title = f"[bold {style}]● {title}[/bold {style}]: "
        names = ", ".join(sorted(items))

        console.print(category_title + names)

    print_category("Subscription", "green", subscription)
    print_category("Rent", "yellow", rent)
    print_category("Buy", "magenta", buy)
    print_category("Free", "blue", free)
    console.print()

    if not any([subscription, free, rent, buy]):
        console.print("[dim]No streaming options found.[/dim]")


def _group_providers(
    where_to_watch_list: list[WhereToWatch],
) -> tuple[dict[str, list[int]], dict[str, list[int]], dict[str, list[int]], set[str]]:
    subscription: dict[str, list[int]] = {}
    rent: dict[str, list[int]] = {}
    buy: dict[str, list[int]] = {}
    free: set[str] = set()

    for vod in where_to_watch_list:
        if not vod.provider:
            continue

        name = vod.provider.display_name

        if not vod.content.payments:
            subscription.setdefault(name, [])
            continue

        for payment in vod.content.payments:
            if payment.subscription:
                subscription.setdefault(name, []).append(payment.price)
            elif payment.rent:
                rent.setdefault(name, []).append(payment.price)
            elif payment.buy:
                buy.setdefault(name, []).append(payment.price)
            elif payment.free:
                free.add(name)

    return subscription, rent, buy, free
