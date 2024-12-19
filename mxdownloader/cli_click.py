import click
from .functions import *


@click.command()
@click.option('--all', '-a')
@click.option('--range', '-r')
@click.option('--chapters', '-c')
def main(all, range, chapters):
    if all:
        url = extract_id_from_url(all)
        download_all_chapters(url)
    elif range:
        url = extract_id_from_url(range)
        download_chapter_range(url)
    elif chapters:
        url = extract_id_from_url(chapters)
        chapter_input = click.prompt("Enter chapters")
        c = [num for num in chapter_input.split()]
        download_specific_chapters(url, c)


if __name__ == "__main__":
    main()
