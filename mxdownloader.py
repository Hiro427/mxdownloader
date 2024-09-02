import os
import sys
import requests
import argparse
from urllib.parse import urlparse
from tqdm import tqdm
import re
from ratelimit import limits, sleep_and_retry
from configparser import ConfigParser

ONE_SECOND = 1

config = ConfigParser()
config_file = os.path.expanduser("~/.config/mxcli/config.ini")
config.read(config_file)


def extract_id_from_url(url):
    parsed = urlparse(url)
    path_parts = parsed.path.rstrip('/').split('/')
    if "chapter" in path_parts:
        return path_parts[-1], 'chapter'
    elif "title" in path_parts:
        return path_parts[-2], 'manga'
    return None, None


@sleep_and_retry
@limits(calls=5, period=ONE_SECOND)
def get_manga_title_from_url(url):
    parsed = urlparse(url)
    path_parts = parsed.path.strip('/').split('/')

    if 'chapter' in path_parts:
        chapter_id = path_parts[-1]
        chapter_data = requests.get(f"https://api.mangadex.org/chapter/{chapter_id}").json()['data']

        manga_id = next((rel['id'] for rel in chapter_data['relationships'] if rel['type'] == 'manga'), None)
        manga_data = requests.get(f"https://api.mangadex.org/manga/{manga_id}").json()['data']
        manga_title = manga_data['attributes']['title'].get('en', 'Unknown Manga')

        return manga_title

    elif 'title' in path_parts:
        manga_id = path_parts[-2]
        manga_data = requests.get(f"https://api.mangadex.org/manga/{manga_id}").json()['data']
        manga_title = manga_data['attributes']['title'].get('en', 'Unknown Manga')

        return manga_title

    return "Invalid URL"

@sleep_and_retry
@limits(calls=5, period=ONE_SECOND)
def get_all_chapters(manga_id):
    limit = 100
    offset = 0
    all_chapters = []
    processed_chapter_ids = set()

    print("Processing Request")
    while True:
        url = f"https://api.mangadex.org/manga/{manga_id}/feed?translatedLanguage[]=en&limit={limit}&offset={offset}&order[chapter]=asc"
        response = requests.get(url)
        data = response.json()
        chapters = data.get('data', [])

        if not chapters:
            print(f"No more chapters found. Breaking loop at offset {offset}")
            break

        for chapter in chapters:
            chapter_id = chapter['id']
            if chapter_id in processed_chapter_ids:
                print(f"Duplicate chapter ID {chapter_id} detected and skipped.")
                continue
            processed_chapter_ids.add(chapter_id)
            all_chapters.append(chapter)

        offset += limit

        if len(chapters) < limit:
            break
    print("Request Accepted")
    return all_chapters

@sleep_and_retry
@limits(calls=5, period=ONE_SECOND)
def download_single_chapter(chapter_id):
    chapter_url = f"https://api.mangadex.org/chapter/{chapter_id}"
    chapter_data = requests.get(chapter_url).json()['data']
    chapter_no = chapter_data['attributes']['chapter']
    chapter_title = chapter_data['attributes']['title']

    at_home_url = f"https://api.mangadex.org/at-home/server/{chapter_id}"
    image_data = requests.get(at_home_url).json()
    base_url = image_data['baseUrl']
    chapter_hash = image_data['chapter']['hash']
    images = image_data['chapter']['data']

    manga_title = "Unknown Manga"
    for relation in chapter_data['relationships']:
        if relation['type'] == 'manga':
            manga_id = relation['id']
            manga_data = requests.get(f"https://api.mangadex.org/manga/{manga_id}").json()['data']
            manga_title = manga_data['attributes']['title'].get('en', manga_title)
            break

    config_dir = config.get("settings", "path", fallback="~/Downloads/Manga")
    base_dir = os.path.expanduser(config_dir)
    manga_dir = os.path.join(base_dir, manga_title)
    chapter_dir = os.path.join(manga_dir, f"Chapter {chapter_no} - {chapter_title}")
    if not os.path.exists(chapter_dir):
        os.makedirs(chapter_dir)

    for i, image in enumerate(tqdm(images, desc=f"Downloading Chapter {chapter_no}")):
        image_url = f"{base_url}/data/{chapter_hash}/{image}"
        image_path = os.path.join(chapter_dir, f"Page {i + 1}.jpg")
        img_response = requests.get(image_url)
        with open(image_path, 'wb') as file:
            file.write(img_response.content)


@sleep_and_retry
@limits(calls=5, period=ONE_SECOND)
def download_multiple_chapter(chapter_id):
    chapter_url = f"https://api.mangadex.org/chapter/{chapter_id}"
    chapter_data = requests.get(chapter_url).json()['data']
    chapter_no = chapter_data['attributes']['chapter']
    chapter_title = chapter_data['attributes']['title']

    at_home_url = f"https://api.mangadex.org/at-home/server/{chapter_id}"
    image_data = requests.get(at_home_url).json()
    base_url = image_data['baseUrl']
    chapter_hash = image_data['chapter']['hash']
    images = image_data['chapter']['data']

    manga_title = "Unknown Manga"  # Fallback title
    for relation in chapter_data['relationships']:
        if relation['type'] == 'manga':
            manga_id = relation['id']
            manga_data = requests.get(f"https://api.mangadex.org/manga/{manga_id}").json()['data']
            manga_title = manga_data['attributes']['title'].get('en', manga_title)
            break


    config_dir = config.get("settings", "path", fallback="~/Downloads/Manga")
    base_dir = os.path.expanduser(config_dir)
    manga_dir = os.path.join(base_dir, manga_title)
    chapter_dir = os.path.join(manga_dir, f"Chapter {chapter_no} - {chapter_title}")
    if not os.path.exists(chapter_dir):
        os.makedirs(chapter_dir)

    for i, image in enumerate(images):
        image_url = f"{base_url}/data/{chapter_hash}/{image}"
        image_path = os.path.join(chapter_dir, f"Page {i + 1}.jpg")
        img_response = requests.get(image_url)
        with open(image_path, 'wb') as file:
            file.write(img_response.content)



def normalize_chapter_number(chapter_str):
    match = re.match(r'^(\d+\.?\d*)', chapter_str)
    return float(match.group(1)) if match else None

def download_chapter_range(manga_id, start, end):
    all_chapters = get_all_chapters(manga_id)
    filtered_chapters = [
        chap for chap in all_chapters
        if normalize_chapter_number(chap['attributes']['chapter']) is not None and
           start <= normalize_chapter_number(chap['attributes']['chapter']) <= end and
           chap['attributes']['translatedLanguage'] == 'en'
    ]

    for chapter in (tqdm(filtered_chapters, desc="Downloading Chapter(s)")):
        download_multiple_chapter(chapter['id'])


def download_specific_chapters(manga_id, chapter_numbers):
    all_chapters = get_all_chapters(manga_id)
    for chapter in all_chapters:
        if chapter['attributes']['chapter'] in chapter_numbers and chapter['attributes']['translatedLanguage'] == 'en':
            download_single_chapter(chapter['id'])

def download_all_chapters(manga_id):
    all_chapters = get_all_chapters(manga_id)
    for chapter in (tqdm(all_chapters, desc="Downloading Chapter(s)")):
        download_multiple_chapter(chapter['id'])

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Download chapters from MangaDex.")
    parser.add_argument("--url", "-u", help="Full URL to the MangaDex manga or chapter page.")
    parser.add_argument("--chapters", "-c", nargs='*', type=str, help="Specify chapter numbers to download, separated by space")
    parser.add_argument("--download-all", "-da", action='store_true', help="Download all available chapters")
    parser.add_argument("--range", "-r", nargs=2, metavar=("START", "END"), type=int, help="Enter a range of chapters. e.g. --range 20 30")
    parser.add_argument("--set_path", "-sp")

    args = parser.parse_args()

    if args.set_path:
        updated_path = args.set_path
        config.set("settings", "path", updated_path)
        read_path = config["settings"]["path"]
        with open(config_file, 'w') as configFile:
            config.write(configFile)
        print(f"Path set to: {read_path}")
        sys.exit(0)

    if not args.url:
        print("url is required")
        sys.exit(0)

    id_from_url, url_type = extract_id_from_url(args.url)
    manga_title = get_manga_title_from_url(args.url)


    if url_type == 'chapter':
        print(f"Downloading chapter for {manga_title}")
        download_single_chapter(id_from_url)
        print(f"Download Complete: Chapter for {manga_title}")
    elif url_type == 'manga':
        if args.download_all:
            print(f"Downloading all chapters for {manga_title}")
            download_all_chapters(id_from_url)
            print(f"Download complete: All chapters for {manga_title}")
        elif args.chapters:
            print(f"Downloading chapters: {args.chapters}, for {manga_title}")
            download_specific_chapters(id_from_url, args.chapters)
            print(f"Download complete: Chapters {args.chapters} for {manga_title}")
        elif args.range:
            start_chapter, end_chapter = args.range
            print(f"Downloading chapters {start_chapter} to {end_chapter} for {manga_title}")
            download_chapter_range(id_from_url, start_chapter, end_chapter)
            print(f"Download complete: Chapter {start_chapter} to {end_chapter} of {manga_title}")
        else:
            print("No chapters specified. Please use --chapters to specify chapter numbers or --download-all to download all chapters.")


    else:
        print("Invalid URL. Please provide a valid MangaDex chapter or manga URL.")
