# mxdownloader
A command line tool, utilizing the mangadex.org api you can download single, list, range or all chapters of a given manga. 

### Compatability 
Currently I've only tested on **Linux**, I expect it will work on MacOS aswell, but I will be testing it and updating this readme appropriately. 

As for Windows I've only done  little testing, the main funcionality is there but I still have a few kinks to work out.


## Installation 

#### Note: Creating the virtual environment is not necessary, you can just pip3/pip install -r requirements .txt and make the exe with pyinstaller, I'll leave that up to you. 

#### Similarly you dont need to use pyinstaller, you can just run python/python3 mxdownloader.py followed by the arguments. 

Run: 

`git clone https://github.com/Hiro427/mxdownloader.git /path/to/directory` #Linux/MacOS

`git clone -b windows --single-branch https://github.com/Hiro427/mxdownloader.git` #Windows

Create a Python Virtual Environment 
`python -m venv .venv`

Install the requirements  
`pip install -r requirements.txt`

Create the executable
`pyinstaller --onefile mxdownloader.py`

Move the executable to your PATH
`cd dist`
`sudo mv ./mxdownloader /usr/local/bin/`


## Using the CLI 

### Config File 

The location of the config file is hard coded by default to be ~/config/mxcli/config.ini, you can change this in the .py file is you wish, you can then create the file yourself to change the default download path.

This is not necessary as the script will default to ~/Downloads/Manga 

Example Config File:

![Screenshot from 2024-09-03 13-38-51](https://github.com/user-attachments/assets/db71125f-77eb-48e5-9826-18d92bd105c9)


You need either the manga url or the chapter url,
#### To Download any chapter of any language: 
![Screenshot from 2024-09-01 18-07-07](https://github.com/user-attachments/assets/da1aa90e-9ef2-4ef1-8a01-e8595a845ef7)

#### To download any 2 chapters follow the syntax in the picture below, where we download chapters 2 and 7  
![Screenshot from 2024-09-01 17-47-17](https://github.com/user-attachments/assets/76334fa4-10db-4bfb-b60d-fae3d1484dcd)

#### To download a rnage of chapters follow a syntax like the image below where it will download chapters range 2 to 7
![Screenshot from 2024-09-01 17-46-25](https://github.com/user-attachments/assets/36d5e844-0fac-4f44-8558-8016c9f519ba)

#### To download all chapters of a given manga follow syntax like below. 
![Screenshot from 2024-09-01 17-45-20](https://github.com/user-attachments/assets/bcf7aeca-5c95-4037-86ca-4edbfbe627cd)



## Credits 
**Scanlation Groups**: https://www.reddit.com/r/mangadex/comments/mafhtl/scanlation_sites_megathread/


_I couldn't find a reliable way to get all of the scanlation groups, since this program allows downloading any chapter(s) I wanted to give credit to as many groups as possible._

**_If a group's name is not in this thread or would like me to post there links in the readme or in the wiki (not active atm, but I would make it for this) more directly please let me know via the Issues section._**

**MangaDex API**: https://api.mangadex.org/docs/

_Credits the devs at MangaDex for their work in making this api available to everyone. I did not intend on making this script public as it isn't an extremely complex set up._
