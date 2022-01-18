# HelperBoiRewrite
A rewrite of Helperboi; put simply a general purpose discord bot.

### Main features (current and upcoming) include:

* Music player w. commands
* Cards against humanities system (cleanish)
* Moderation commands and features including but not limited to:
  - *toggleable* auto censor
  - thats the only one other than base commands but still
* *Many* standalone fun commands
* A full economy system like that in dank memer, including but not limited to:
  - Balances
  - Coolness (exp and levels)
  - Boops (boops)
  - Inventories
  - Gambling
* (toggleable) autoresponses
* geoforecast autoalert
* "and much, much more!"

## How to run this monstrosity:
~~You dont because its a bad idea to try run it~~
### Its fairly simple, after downloading the thing you do the following:

Change the contents of the token.txt file to the token of the bot account you want to run helperboi on.

Then, you do the following shell commands: (its assumed you already have pip and virtualenv)

1. `cd /path/to/directory/of/HelperBoiRewrite/`
  You cd into the project directory,

2. `virtualenv bot_env`
  Create the virtual environment to dump packages into.

3. `source ./bot_env/bin/activate`
  Activate the virtual environment,
  
4. `pip install -r requirements.txt`
  Install the project dependencies into the bot_env virtual environment
  
5. `java -jar ./Lavalink.jar` (in a seperate terminal window also cd'd into the project dir)
  Activate the lavalink server for music streaming,

6. `python3 Helpercode.py`
  Run the actual bot file.
  
All database files should be created automatically, and internal caches should follow suit, even once deleted, provided you restart the bot.

After doing the above, the bot should be online and running.
You know its most probably online and working when you see "I'm Ready!" appear in console

~~I take no responsibility for accidental conversions of computers to the helperboi botnet~~
