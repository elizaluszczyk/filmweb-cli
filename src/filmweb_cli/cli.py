import click


@click.command()
def main() -> None:
    click.echo("Hello from filmweb-cli!")


if __name__ == "__main__":
    main()
