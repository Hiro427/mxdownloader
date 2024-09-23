import requests
from InquirerPy import inquirer
import os 
import re 
from urllib.parse import urlparse
from tqdm import tqdm
from ratelimit import limits, sleep_and_retry
from configparser import ConfigParser
from InquirerPy.base.control import Choice
from InquirerPy.prompts.fuzzy import FuzzyPrompt 
import click 

ONE_SECOND = 1


config = ConfigParser()
config_file = os.path.expanduser("~/.config/mxcli/config.ini")
config.read(config_file)


def search_manga(title):
    url = f"https://api.mangadex.org/manga?title={title}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = []
        for manga in data['data']:
            # Add manga title and ID as choices for the prompt
            results.append({
                'name': manga['attributes']['title']['en'],  # Manga title (you can format this as needed)
                'value': manga['id']  # The ID will be stored for retrieval after selection
            })
        return results
    else:
        return []

def extract_id_from_url(url):
    parsed = urlparse(url)
    path_parts = parsed.path.rstrip('/').split('/')
    if "title" in path_parts:
        return path_parts[-2]  # Extract and return the manga ID
    return None



def normalize_chapter_number(chapter_str):
    match = re.match(r'^(\d+\.?\d*)', chapter_str)
    return float(match.group(1)) if match else None


def download_chapter_range(manga_id):
    start_chapter = click.prompt("Enter the starting chapter number")
    end_chapter = click.prompt("Enter the ending chapter number")

    # Convert input to float to handle decimal chapter numbers correctly
    start_chapter_num = float(start_chapter)
    end_chapter_num = float(end_chapter)

    # Fetch all the chapters
    chapters = get_all_chapters(manga_id)

    # Filter chapters that fall within the specified range
    chapters_in_range = [
        chap for chap in chapters
        if chap['attributes']['chapter'] is not None  # Ensure the chapter number exists
        and start_chapter_num <= float(chap['attributes']['chapter']) <= end_chapter_num
    ]

    # Download each chapter in the range
    for chap in chapters_in_range:
        # print(f"Downloading Chapter {chap['attributes']['chapter']} - {chap['attributes']['title']}")
        download_single_chapter(chap['id'])


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
    # chapter_title = chapter_data['attributes']['title']

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
    chapter_dir = os.path.join(manga_dir, f"Chapter_{chapter_no}")
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
    # chapter_title = chapter_data['attributes']['title']

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
    chapter_dir = os.path.join(manga_dir, f"Chapter_{chapter_no}")
    if not os.path.exists(chapter_dir):
        os.makedirs(chapter_dir)

    for i, image in enumerate(images):
        image_url = f"{base_url}/data/{chapter_hash}/{image}"
        image_path = os.path.join(chapter_dir, f"Page {i + 1}.jpg")
        img_response = requests.get(image_url)
        with open(image_path, 'wb') as file:
            file.write(img_response.content)


def download_all_chapters(manga_id):
    all_chapters = get_all_chapters(manga_id)
    for chapter in (tqdm(all_chapters, desc="Downloading Chapter(s)")):
        download_multiple_chapter(chapter['id'])

def download_specific_chapters(manga_id, chapter_numbers):
    all_chapters = get_all_chapters(manga_id)
    for chapter in all_chapters:
        if chapter['attributes']['chapter'] in chapter_numbers and chapter['attributes']['translatedLanguage'] == 'en':
            download_single_chapter(chapter['id'])




def download_specific_range(manga_id):
    # Prompt the user to enter start and end chapter numbers
    start_chapter = inquirer.text(message="Enter the starting chapter number:").execute()
    end_chapter = inquirer.text(message="Enter the ending chapter number:").execute()

    # Convert input to float to handle decimal chapter numbers correctly
    start_chapter_num = float(start_chapter)
    end_chapter_num = float(end_chapter)

    # Fetch all the chapters
    chapters = get_all_chapters(manga_id)

    # Filter chapters that fall within the specified range
    chapters_in_range = [
        chap for chap in chapters
        if chap['attributes']['chapter'] is not None  # Ensure the chapter number exists
        and start_chapter_num <= float(chap['attributes']['chapter']) <= end_chapter_num
    ]

    # Download each chapter in the range
    for chap in chapters_in_range:
        # print(f"Downloading Chapter {chap['attributes']['chapter']} - {chap['attributes']['title']}")
        download_single_chapter(chap['id'])


def list_available_chapters(manga_id):
    # Fetch all the chapters using your existing `get_all_chapters` function
    chapters = get_all_chapters(manga_id)

    # Extract the chapter number and title from the chapter data, and store both ID and chapter number
    chapter_choices = [
        {
            "name": f"Chapter {chap['attributes']['chapter']} - {chap['attributes']['title']}",
            "value": chap['id'],
            "chapter_number": chap['attributes']['chapter']  # Add chapter number for easier tracking
        }
        for chap in chapters
    ]

    selected_chapters = []

    while True:
        # Ensure that each iteration starts with a fresh list of options
        choices_to_display = [chap for chap in chapter_choices if chap['value'] not in selected_chapters]

        # Add "Go Back" and "Continue" options at the top of the list
        choices_to_display.insert(0, {'name': 'Continue to download selected chapters', 'value': 'continue'})
        choices_to_display.insert(0, {'name': 'Go Back', 'value': 'go_back'})

        prompt = FuzzyPrompt(
            message="Search or select chapters to add (type to search):",
            choices=choices_to_display,
            multiselect=False  # Only allow single chapter selection at a time
        )
        chosen_chapter = prompt.execute()

        # If the user selects "Continue"
        if chosen_chapter == 'continue':
            if selected_chapters:
                print("Continuing to download...")
                break
            else:
                print("No chapters selected! Please select some chapters before continuing.")
                continue

        # If the user selects "Go Back"
        if chosen_chapter == 'go_back':
            print("Going back to the previous menu...")
            return  # Go back to the previous menu

        selected_chapters.append(chosen_chapter)

        display_selected_chapters(selected_chapters, chapter_choices)

    for chapter_id in selected_chapters:
        download_single_chapter(chapter_id)

def display_selected_chapters(selected_chapters, chapter_choices):
    """Display the selected chapters by their chapter numbers instead of their IDs."""
    selected_numbers = [
        next((chap['chapter_number'] for chap in chapter_choices if chap['value'] == chapter_id), chapter_id)
        for chapter_id in selected_chapters
    ]
    print(f"Selected chapters so far: {selected_numbers}")

def handle_download_options(manga_id):
    while True:
        options = inquirer.select(
            message="Select download option:",
            choices=[
                "Download All Chapters",
                "Download Range of Chapters",
                "Download Selected Chapters",
                "Go Back"
            ],
            vi_mode=True, 
        ).execute()

        if options == "Download All Chapters":
            download_all_chapters(manga_id)
            break
        elif options == "Download Range of Chapters":
            download_specific_range(manga_id)
            break
        elif options == "Download Selected Chapters":
            list_available_chapters(manga_id)
            break
        elif options == "Go Back":
            return  # Go back to the main menu
