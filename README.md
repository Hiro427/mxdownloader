# mxdownloader
A command line tool, utilizing the mangadex.org api you can download single, list, range or all chapters of a given manga. 



## About 
This is a a python cli tool that can dowload single, list, range or all chapters. **_The config file as of writing this (9/1/2024) can only set the path_** but I will add the ability to change langauge from default (en/english) to any supported langauge on mangadex via the cli.

### Compatability 
Currently I've only tested on **Linux**, I expect it will work on MacOS aswell, but I will be testing it and updating this readme appropriately. 

As for Windows I've only done  little testing, the main funcionality is there but I still have a few kinks to work out.

This is my first _published_ project albeit a small one, if any of the more experienced devs who may come across this have any suggestions feel free to add it to the issues discussion. 

Thank you in advance for your advice!

## Installation 
Run: 
`git clone https://github.com/JacobAR1/mxdownloader.git /path/to/directory`

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




## Credits 
**Scanlation Groups**: https://www.reddit.com/r/mangadex/comments/mafhtl/scanlation_sites_megathread/


_I couldn't find a reliable way to get all of the scanlation groups especially since this program allows downloading any chapter(s)._

**_If a group's name is not in this thread or would like me to post there links in the readme or in the wiki (not active atm, but I would make it for this) more directly please let me know via the Issues section._**

**MangaDex API**: https://api.mangadex.org/docs/

_Credits the devs at MangaDex for their work in making this api available to everyone. I did not intend on making this script public as it isn't an extremely complex set up._
