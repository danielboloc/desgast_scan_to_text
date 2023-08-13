"""Console script for desgast_scan_to_text."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for desgast_scan_to_text."""
    click.echo("Replace this message by putting your code into "
               "desgast_scan_to_text.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
