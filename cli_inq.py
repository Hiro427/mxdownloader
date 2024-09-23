from InquirerPy import inquirer
from functions import handle_download_options, search_manga, extract_id_from_url






def main():
    # Display the ASCII art logo when the CLI starts
    print(r"""
   _____                              ________
  /     \ _____    ____    _________  \______ \   ____ ___  ___
 /  \ /  \\__  \  /    \  / ___\__  \  |    |  \_/ __ \\  \/  /
/    Y    \/ __ \|   |  \/ /_/  > __ \_|    `   \  ___/ >    <
\____|__  (____  /___|  /\___  (____  /_______  /\___  >__/\_ \
        \/     \/     \//_____/     \/        \/     \/      \/
 ________                      .__                    .___
 \______ \   ______  _  ______ |  |   _________     __| _/___________
  |    |  \ /  _ \ \/ \/ /    \|  |  /  _ \__  \   / __ |/ __ \_  __ \
  |    `   (  <_> )     /   |  \  |_(  <_> ) __ \_/ /_/ \  ___/|  | \/
 /_______  /\____/ \/\_/|___|  /____/\____(____  /\____ |\___  >__|
         \/                  \/                \/      \/    \/
    """)

    while True:
        # Main menu with URL, Search, and Exit
        main_action = inquirer.select(
            message="Main menu:",
            choices=[
                "Enter URL",
                "Search for manga",
                "Exit"
            ],
            vi_mode=True, 
        ).execute()

        if main_action == "Exit":
            print("Exiting...")
            break

        elif main_action == "Enter URL":
            url = inquirer.text(message="Enter the manga URL:").execute()
            manga_id = extract_id_from_url(url)
            if manga_id:
                handle_download_options(manga_id)
            else:
                print("Invalid URL or ID not found.")

        elif main_action == "Search for manga":
            title = inquirer.text(message="Enter the manga title to search:").execute()
            manga_choices = search_manga(title)

            if manga_choices:
                manga_choices.append({'name': 'Go Back', 'value': 'go_back'})
                selected_manga_id = inquirer.select(
                    message="Select the manga:",
                    choices=manga_choices, 
                    vi_mode=True, 
                ).execute()

                if selected_manga_id != 'go_back':
                    handle_download_options(selected_manga_id)
            else:
                print("No results found for that title.")
if __name__ == "__main__":
    main()
