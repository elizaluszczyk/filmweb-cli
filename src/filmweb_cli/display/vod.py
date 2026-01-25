from filmweb_cli.schemas.vod.vod_providers import WhereToWatch

from .console import console


def print_where_to_watch(where_to_watch_list: list[WhereToWatch]) -> None:
    if not where_to_watch_list:
        console.print("[dim]No streaming information available.[/dim]")
        return

    console.print()

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
    if not where_to_watch_list:
        console.print("[dim]No streaming information available.[/dim]")
        return

    console.print()

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
