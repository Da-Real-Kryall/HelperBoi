# HelperBoi
Put simply, a general purpose Discord bot currently serving as a passion project and sink for ideas.

### Main features (current and upcoming) include:

* Music player w. commands
* Dynamic Cards-Against-Humanities system (w/ clean version)
* Moderation commands and features including but not limited to:
  - *toggleable* auto censor
  - thats the only one other than base commands but still
* *Many* standalone fun commands
* A full economy system like that in dank memer, including but not limited to:
  - Balances
  - Coolness (exp and levels)
  - Slaps (slaps)
  - Inventories
  - Gambling
* (toggleable) autoresponses
* Autoalerts for geomagnetic storms
* Reminders
* Full support for slash commands (recently added)
* "and much, much more!"
## How to run this monstrosity:
~~You dont because its a bad idea to try run it~~
### Requirements:
* Python 3.8 or higher. (download [here](https://www.python.org/downloads/))
* Virtualenv (install with `pip install virtualenv`)
* A Discord bot token. (get one by setting up a discord app [here](https://discord.com/developers/applications).)

### Actual Setup:
1. `git clone https://github.com/Da-Real-Kryall/HelperBoi`
<br> Download the repository.

2. `cd /path/to/directory/of/HelperBoi/`
<br> Cd into the project directory, do this for two windows.

3. Change the contents of `token.txt` to the token of the bot you want to run HelperBoi on.

4. `virtualenv bot_env`
<br> Create the virtual environment to dump packages into and run the bot in.

5. `source ./bot_env/bin/activate`
<br> Activate the virtual environment. (The command might be different on Windows.)
  
6. `pip install -r requirements.txt`
<br> Install the project dependencies into the bot_env virtual environment.
  
5. `java -jar ./Lavalink.jar` 
<br> Activate the lavalink server for music streaming, do this in that second window.

6. `python3 Helpercode.py`
<br> Run the actual bot file. (in the first window)
  
All database files should be created automatically, and internal caches should follow suit, even once deleted, provided you restart the bot.

After doing the above, the bot should be online and running.
You know its most probably online and working when you see "I'm Ready!" appear in console, alongside a slew of cog loading messages.

~~I take no responsibility for accidental conversions of computers to the helperboi botnet.~~

Have fun!
