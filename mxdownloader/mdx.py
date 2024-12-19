from .cli_click import main as click_cli
from .cli_inq import main as inquirer_cli
import sys


def main():
    if len(sys.argv) == 1:
        inquirer_cli()
    else:
        click_cli()


if __name__ == "__main__":
    main()
