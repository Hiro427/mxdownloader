# mxdownloader
A command line tool, utilizing the mangadex.org api you can download single, list, range or all chapters of a given manga. 

### Compatability 
Windows: Ok 

Linux: Ok

Mac: Error msg may appear during the download process but the download should go through regardless. This is on my list of things to work on going forward. 


# Installation 

You will need to have python installed.


### Clone repo: 

#### Linux/MacOS

`git clone https://github.com/Hiro427/mxdownloader.git /path/to/directory`

#### Windows
`git clone -b windows --single-branch https://github.com/Hiro427/mxdownloader.git` 

#### Navigate to the project directory 

`cd path/to/project` 

#### Install the requirements

`pip or pip3 install -r requirements.txt`

`pip or pip3 install pyinstaller`

#### Create the executable

`pyinstaller --onefile mdx.py`

#### Move the executable to your PATH

`cd dist` #This is where the exe created by pyinstaller should be.

`sudo mv ./mdx /usr/local/bin/` 

#This should add it to your PATH if you are on MacOS or Linux allowing you to use the cli outside of the project folder. I am not sure how this is done for Windows. 


## Main Menu 

Can be accessed by either 
- `python or python3 mdx.py` if not building exe with pyinstaller
- `./mdx` if executing from dist/
- `mdx` if program is in PATH 

The main functionality is the same for the program whether you decide to copy and paste the url from mangadex or to search from the CLI. 

PLEASE NOTE: The URL must be the manga url not the inidividual chapter url. 

![Screenshot from 2024-09-23 16-35-13](https://github.com/user-attachments/assets/043f42e7-6fb9-4634-bdc2-bf1030577f44)

## Using the CLI 
You have two ways to download for every option, either the cli or the interactive cli.

In the interactive version, vim keys can be used to navigate in main menu and the download options menu.

Vim Keys CANNOT be used when selecting multiple in the list view as the keystrokes will register in the fuzzy finder 

#### Downloading All Chapters 
![Screenshot from 2024-09-23 16-35-50](https://github.com/user-attachments/assets/2dfb3f5c-966a-41df-83d1-aa373152534f)
![Screenshot from 2024-09-23 16-41-02](https://github.com/user-attachments/assets/57801c7d-5e43-4fcd-ad08-645831fd2f27)


#### Download Range of Chapters
![Screenshot from 2024-09-23 16-40-39](https://github.com/user-attachments/assets/5432a4ba-a853-4ce2-b2fc-6e2f903f9c4f)
![Screenshot from 2024-09-23 16-36-20](https://github.com/user-attachments/assets/ff8bd836-f83c-4424-9732-8c8374fc644f)

#### Download Selected Chapters

As I said above VIM keys CANNOT be used here as the program will register them as part of the search. In this menu you will need to use up or down arrows to navigate in addition to the fuzzy finder. 

You can type the chapter title or number, pressing enter adds that chapter to the list of the ones you wish to download.

You can then press continue to begin downloading.

![Screenshot from 2024-09-23 16-37-53](https://github.com/user-attachments/assets/2151e85a-55f5-4252-a0d1-e11a97d2078a)

![Screenshot from 2024-09-23 16-37-28](https://github.com/user-attachments/assets/e91765b4-dd03-4c26-b8bb-643455e22268)

![Screenshot from 2024-09-23 16-40-22](https://github.com/user-attachments/assets/f55a88b1-3fbe-4831-b6e6-7bf5aae91f6a)


### Config File 

Usable without config file: Default to ~/Downloads/Manga

The location of the config file is hard coded by default to be ~/config/mxcli/config.ini. I will add functionality in the program so that it can be changed from the cli. But for now if you want to change the default download directory create the config file. 


#### Example Config File:

![Screenshot from 2024-09-03 13-38-51](https://github.com/user-attachments/assets/db71125f-77eb-48e5-9826-18d92bd105c9)

## Acknowledgements
**Scanlation Groups**: https://www.reddit.com/r/mangadex/comments/mafhtl/scanlation_sites_megathread/


_I couldn't find a reliable way to get all of the scanlation groups, since this program allows downloading any chapter(s) I wanted to give credit to as many groups as possible._

**_If a group's name is not in this thread or would like me to post there links in the readme or in the wiki (not active atm, but I would make it for this) more directly please let me know via the Issues section._**

**MangaDex API**: https://api.mangadex.org/docs/

_Credits the devs at MangaDex for their work in making this api available to everyone._
