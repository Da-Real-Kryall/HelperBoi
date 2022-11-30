

import math, sqlite3, os, json, time

with open(os.getcwd()+"/Resources/json/items.json") as file:
    item_json = json.loads(file.read())
with open(os.getcwd()+"/Resources/json/misc_economy.json") as file:
    misc_economy_json = json.loads(file.read())
with open(os.getcwd()+"/Resources/json/settings_key.json") as file:
    settings_json = json.loads(file.read())
with open(os.getcwd()+"/Resources/json/command_cooldowns.json") as file:
    cooldowns_json = json.loads(file.read())

def init_everything():
    # runs the init.sql file to create the databases that don't already exist
    main_connection = sqlite3.connect("Resources/everything.db")
    main_cursor = main_connection.cursor()
    main_cursor.executescript(open("utils/init.sql", "r").read())

def initialize_user(user_id):
    everything = sqlite3.connect("Resources/everything.db")
    cursor = everything.cursor()

    cursor.execute('''SELECT count(discord_id) FROM users WHERE discord_id = ?''', (user_id,))
    count = cursor.fetchone()[0]

    if count == 0:
        # insert (user_id, 100, 0, 0, 1, 0)
        cursor.execute('''
        INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, 100, 0, 0, 1, 0))

        cursor.execute('''
        INSERT INTO inventory VALUES (?, ?, ?)
        ''', (user_id, "biscuit", 1))

        for setting in settings_json["users"].keys():
            cursor.execute('''
            INSERT INTO user_settings VALUES (?, ?, ?)
            ''', (user_id, setting, settings_json["users"][setting]["default"])
            )

        everything.commit()
    everything.close()

def initialize_server(server_id:int):
    everything = sqlite3.connect("Resources/everything.db")
    cursor = everything.cursor()

    cursor.execute('''
    SELECT count(guild_id) FROM guild_settings WHERE guild_id = ?
    ''', (server_id,))

    if cursor.fetchone()[0] == 0:
        for setting in settings_json["servers"].keys():
            cursor.execute('''
            INSERT INTO guild_settings VALUES (?, ?, ?)
            ''', (server_id, setting, settings_json["servers"][setting]["default"])
            )

    #if count < len(settings_json["servers"]):
    #    cursor.execute('''
    #    SELECT * FROM server_settings WHERE server_id = ?
    #    ''', (server_id,))
    #    data = cursor.fetchall()
    #    for setting in settings_json["servers"].keys():
    #        if setting not in [x[1] for x in data]:
    #            cursor.execute('''
    #            INSERT INTO server_settings (?, ?, ?)
    #            ''', (server_id, setting, settings_json["servers"][setting]["default"]))
    
        everything.commit()
    everything.close()

def fetch_user_data(user_id: int, data_type: str):
    everything = sqlite3.connect("Resources/everything.db")
    cursor = everything.cursor()

    initialize_user(user_id)

    if data_type == "balance":
        cursor.execute('''SELECT balance FROM users WHERE discord_id = ?''', (user_id,))
        return cursor.fetchone()[0]
    
    elif data_type == "coolness":
        cursor.execute('''SELECT coolness FROM users WHERE discord_id = ?''', (user_id,))
        return cursor.fetchone()[0]

    elif data_type == "slaps":
        cursor.execute('''SELECT slaps FROM users WHERE discord_id = ?''', (user_id,))
        return cursor.fetchone()[0]

    elif data_type == "permission_level":
        cursor.execute('''SELECT permission_level FROM users WHERE discord_id = ?''', (user_id,))
        return cursor.fetchone()[0]

    elif data_type == "blocked":
        cursor.execute('''SELECT blocked FROM users WHERE discord_id = ?''', (user_id,))
        return cursor.fetchone()[0]

    elif data_type == "inventory":
        cursor.execute('''SELECT item_name, quantity FROM inventory WHERE user_id = ?''', (user_id,))
        return dict(cursor.fetchall())

    elif data_type == "settings":
        cursor.execute('''SELECT option, value FROM user_settings WHERE user_id = ?''', (user_id,))
        return dict(cursor.fetchall())

    else:
        raise ValueError("invalid data type")

def fetch_guild_settings(server_id: int):
    initialize_server(server_id)

    everything = sqlite3.connect("Resources/everything.db")
    cursor = everything.cursor()

    cursor.execute('''SELECT option, value FROM guild_settings WHERE guild_id = ?''', (server_id,))
    
    return dict(cursor.fetchall())

def set_user_data(user_id: int, data_type: str, value):
    initialize_user(user_id)

    everything = sqlite3.connect("Resources/everything.db")
    cursor = everything.cursor()

    if data_type == "balance":
        cursor.execute('''UPDATE users SET balance = ? WHERE discord_id = ?''', (value, user_id))
    
    elif data_type == "coolness":
        cursor.execute('''UPDATE users SET coolness = ? WHERE discord_id = ?''', (value, user_id))

    elif data_type == "slaps":
        cursor.execute('''UPDATE users SET slaps = ? WHERE discord_id = ?''', (value, user_id))

    elif data_type == "permission_level":
        cursor.execute('''UPDATE users SET permission_level = ? WHERE discord_id = ?''', (value, user_id))

    elif data_type == "blocked":
        cursor.execute('''UPDATE users SET blocked = ? WHERE discord_id = ?''', (value, user_id))

    elif data_type == "settings":
        for setting in value.keys():
            cursor.execute('''UPDATE user_settings SET value = ? WHERE user_id = ? AND option = ?''', (value[setting], user_id, setting))

    elif data_type == "inventory":
        for item in value.keys():
            cursor.execute('''SELECT count(user_id) FROM inventory WHERE user_id = ? AND item_name = ?''', (user_id, item))
            if cursor.fetchone()[0] == 0:
                cursor.execute('''INSERT INTO inventory VALUES (?, ?, ?)''', (user_id, item, value[item]))
            else:
                cursor.execute('''UPDATE inventory SET quantity = ? WHERE user_id = ? AND item_name = ?''', (value[item], user_id, item))
    else:
        raise ValueError("invalid data type")

    everything.commit()
    everything.close()

def set_guild_settings(server_id: int, value):
    initialize_server(server_id)

    everything = sqlite3.connect("Resources/everything.db")
    cursor = everything.cursor()

    for setting in value.keys():
        cursor.execute('''UPDATE guild_settings SET value = ? WHERE guild_id = ? AND option = ?''', (value[setting], server_id, setting))

    everything.commit()
    everything.close()

def fetch_reminders(user_id: int=None):
    everything = sqlite3.connect("Resources/everything.db")
    cursor = everything.cursor()

    if user_id is None:
        cursor.execute('''SELECT * FROM reminders''')
        return cursor.fetchall()
    else:
        cursor.execute('''SELECT * FROM reminders WHERE user_id = ?''', (user_id,))
        return cursor.fetchall()

#adds a reminder and returns it's id
def add_reminder(user_id: int, time: int, message: str, channel_id: int):
    everything = sqlite3.connect("Resources/everything.db")
    cursor = everything.cursor()
    
    cursor.execute('''INSERT INTO reminders (user_id, timestamp, content, channel_id) VALUES (?, ?, ?, ?)''', (user_id, time, message, channel_id))

    everything.commit()

    cursor.execute('''SELECT id FROM reminders WHERE user_id = ? AND timestamp = ? AND content = ? AND channel_id = ?''', (user_id, time, message, channel_id))
    res = cursor.fetchone()[0]
    everything.close()
    return res
    

def remove_reminders(reminder_ids: list):
    everything = sqlite3.connect("Resources/everything.db")
    cursor = everything.cursor()
    for reminder_id in reminder_ids:
        cursor.execute('''DELETE FROM reminders WHERE id = ?''', (reminder_id,))

    everything.commit()
    everything.close()
# there is no guild data

def fetch_users_by_setting(setting: str, value):
    everything = sqlite3.connect("Resources/everything.db")
    cursor = everything.cursor()

    cursor.execute('''SELECT user_id FROM user_settings WHERE option = ? AND value = ?''', (setting, value))

    return [user[0] for user in cursor.fetchall()]


"""





#an import file for economy manipulation methods

# how inv is stored:
#migrate coolness methods to here



# This will initialize any database tables that don't exist already.
def init_main():
    submission_database = sqlite3.connect(f"Databases_old/misc/submissions.db")
    cursor = submission_database.cursor()
    cursor.execute('''SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = 'suggestions' ''')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''CREATE TABLE suggestions (
            ID INTEGER PRIMARY KEY, 
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            timestamp INTEGER
        )''')
    cursor.execute('''SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = 'bugreports' ''')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''CREATE TABLE bugreports (
            ID INTEGER PRIMARY KEY, 
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            timestamp INTEGER
        )''')
    
    submission_database.commit()
    submission_database.close()

    prefix_database = sqlite3.connect(f"Databases_old/misc/prefixes.db")
    cursor = prefix_database.cursor()
    cursor.execute('''SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = 'prefixes' ''')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''CREATE TABLE prefixes (
            guild_id INTEGER,
            prefix TEXT
        )''')

    prefix_database.commit()
    prefix_database.close()

    reminder_database = sqlite3.connect(f"Databases_old/misc/reminders.db")
    cursor = reminder_database.cursor()
    cursor.execute('''SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = 'reminders' ''')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''CREATE TABLE reminders (
            ID INTEGER PRIMARY KEY, 
            content TEXT,
            timestamp INTEGER,
            author_id INTEGER,
            guild_id INTEGER,
            channel_id INTEGER
        )''')

    reminder_database.commit()
    reminder_database.close()

    created_cah_db = False #if this is true then i populate the database with the default cards

    cah_database = sqlite3.connect(f"Databases_old/misc/cards_against_humanity.db")
    cursor = cah_database.cursor()
    cursor.execute('''SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = 'white' ''')
    if cursor.fetchone()[0] == 0:
        created_cah_db = True
        cursor.execute('''CREATE TABLE white (
            ID INTEGER PRIMARY KEY, 
            content TEXT,
            author_id INTEGER
        )''')
    cursor.execute('''SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = 'black' ''')
    if cursor.fetchone()[0] == 0:
        created_cah_db = True
        cursor.execute('''CREATE TABLE black (
            ID INTEGER PRIMARY KEY, 
            content TEXT,
            author_id INTEGER
        )''')

    if created_cah_db:
        with open("Resources/plaintext/cards_data.txt") as file:
            file_data = file.read()
        file_data = file_data.split("\n")
        mode = "black"
        for line in file_data:
            if line == "<WHITE>":
                mode = "white"
                continue
            if mode == 'white':
                cursor.execute('''INSERT into white values (?,?)''', (line, 849543878059098144))
            elif mode == "black":
                cursor.execute('''INSERT into black values (?,?)''', (line, 849543878059098144))

    cah_database.commit()
    cah_database.close()

def init_user(user_id):  #inits a user's balance, inventory and preferences. try to make this efficient.
    
    user_database = sqlite3.connect(f"Databases_old/users/{user_id}.db")
    user_cursor = user_database.cursor()

    #single values, balance, exp etc
    user_cursor.execute('''SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = 'single_values' ''')
    if user_cursor.fetchone()[0] == 0:
        user_cursor.execute('''CREATE TABLE single_values (
            balance INTEGER, 
            coolness INTEGER,
            boops INTEGER,
            permission_level INTEGER,
            blocked INTEGER
        )''')
        user_cursor.execute('''INSERT into single_values values (
            100,
            0,
            0,
            0,
            0
        )''')

    #inventory
    user_cursor.execute('''SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = 'inventory' ''')
    if user_cursor.fetchone()[0] == 0:
        user_cursor.execute('''CREATE TABLE inventory (
            item_name TEXT,
            quantity INTEGER
        )''') #perhaps add flags when switching to mode two for storage; item nbt and such
    
    #remove unknown items
    user_cursor.execute('''SELECT item_name FROM inventory''')
    data = user_cursor.fetchall()

    if len(data) > 0:
        for item in data:
            if item[0] not in list(item_json.keys()):
                user_cursor.execute('''DELETE FROM inventory WHERE item_name = ? ''', (str(item[0]),))

    #add in all items
    for item in item_json.keys():
        user_cursor.execute('''SELECT quantity FROM inventory WHERE item_name = ? ''', (str(item),))
        fetched_item = user_cursor.fetchall()
        if len(fetched_item) == 0:
            user_cursor.execute('''INSERT into inventory values (?,?)''', (item, "1" if item == "biscuit" else "0"))


    #settings
    user_cursor.execute('''SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = 'settings' ''')
    if user_cursor.fetchone()[0] == 0:
        user_cursor.execute('''CREATE TABLE settings (
            option TEXT,
            value INTEGER
        )''')


    #remove unknown settings
    user_cursor.execute('''SELECT option FROM settings''')
    data = user_cursor.fetchall()

    if len(data) > 0:
        for setting in data:
            if setting[0] not in list(settings_json["users"].keys()):
                user_cursor.execute('''DELETE FROM settings WHERE option = ? ''', (str(setting[0]),))

    #add in all settings
    for setting in settings_json["users"].keys():
        user_cursor.execute('''SELECT value FROM settings WHERE option = ? ''', (setting,))
        fetched_setting = user_cursor.fetchall()
        if len(fetched_setting) == 0:
            user_cursor.execute('''INSERT into settings values (?,?)''', (setting, int(settings_json["users"][setting]["default"])))

    #cooldowns
    user_cursor.execute('''SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = 'cooldowns' ''')
    if user_cursor.fetchone()[0] == 0:
        user_cursor.execute('''CREATE TABLE cooldowns (
            name TEXT,
            timestamp INTEGER
        )''') 
    
    #remove unknown entries
    user_cursor.execute('''SELECT name FROM cooldowns''')
    data = user_cursor.fetchall()

    if len(data) > 0:
        for entry in data:
            if entry[0] not in list(cooldowns_json.keys()):
                user_cursor.execute('''DELETE FROM cooldowns WHERE name = ?''', (entry[0],))

    #add in all entries
    for entry in cooldowns_json.keys():
        user_cursor.execute('''SELECT timestamp FROM cooldowns WHERE name = ?''', (entry,))
        fetched_timestamp = user_cursor.fetchall()
        if len(fetched_timestamp) == 0:
            user_cursor.execute('''INSERT into cooldowns values (?,?)''', (str(entry), int(time.time())-cooldowns_json[entry]))

    user_database.commit()

    user_database.close()

def init_server(server_id):
    server_database = sqlite3.connect(f"Databases_old/servers/{server_id}.db")
    server_cursor = server_database.cursor()

    #settings
    server_cursor.execute('''SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = 'settings' ''')
    if server_cursor.fetchone()[0] == 0:
        server_cursor.execute('''CREATE TABLE settings (
            option TEXT,
            value INTEGER
        )''')

    #remove unknown settings
    server_cursor.execute('''SELECT option FROM settings''')
    data = server_cursor.fetchall()

    if len(data) > 0:
        for setting in data:
            if setting[0] not in list(settings_json["servers"].keys()):
                server_cursor.execute('''DELETE FROM settings WHERE option = ?''', (str(setting[0]),))

    #add in all settings
    for setting in settings_json["servers"].keys():
        server_cursor.execute('''SELECT value FROM settings WHERE option = ?''', (str(setting),))
        fetched_setting = server_cursor.fetchall()
        if len(fetched_setting) == 0:
            server_cursor.execute('''INSERT into settings values (?,?)''', (str(setting), int(settings_json["servers"][setting]["default"])))
    
    server_database.commit()

    server_database.close()

def fetch_reminders(user:int=0):#returns the reminders that will occur within the hour, or all from the user if given
    reminder_database = sqlite3.connect(f"Databases_old/misc/reminders.db")
    cursor = reminder_database.cursor()
    if user == 0:
        cursor.execute('''SELECT ID, content, timestamp, author_id, guild_id, channel_id FROM reminders WHERE timestamp < ?''', (int(time.time()+3600),))
        return cursor.fetchall()
    else:
        init_user(user)
        cursor.execute('''SELECT ID, content, timestamp, author_id, guild_id, channel_id FROM reminders WHERE author_id = ?''', (user,))
        return cursor.fetchall()

def fetch_timedelta(user_id:int, entry:str):
    # returns how many seconds in the past that the timestamp represents.
    init_user(user_id)

    if entry not in cooldowns_json.keys():
        raise KeyError("this isnt a valid cooldown")

    user_database = sqlite3.connect(f"Databases_old/users/{user_id}.db")
    user_cursor = user_database.cursor()

    user_cursor.execute(''' SELECT timestamp FROM cooldowns WHERE name = ?''', (str(entry),))
    data = user_cursor.fetchall()[0][0]

    user_database.commit()
    user_database.close()

    return int(time.time())-data

def fetch_cards(mode, amount:int): #SELECT * FROM table WHERE id IN (SELECT id FROM table ORDER BY RANDOM() LIMIT x)
    if mode not in ["white", "black"]:
        raise ValueError("please pick either white or black as the mode argument for fetch_cards")

    cah_database = sqlite3.connect(f"Databases_old/misc/cards_against_humanity.db")
    cursor = cah_database.cursor()
    
    cursor.execute(f'''SELECT * FROM {mode} WHERE ID IN (SELECT ID FROM {mode} ORDER BY RANDOM() LIMIT ?)''', (amount,))
    return_id = cursor.fetchall()
    cah_database.close()
    
    return return_id
    

def fetch_balance(user_id:int):
    init_user(user_id)
    user_database = sqlite3.connect(f"Databases_old/users/{user_id}.db")
    user_cursor = user_database.cursor()

    user_cursor.execute('''SELECT balance from single_values''')
    balance = user_cursor.fetchall()[0][0]

    user_database.close()

    return balance

def fetch_boops(user_id):
    init_user(user_id)
    user_database = sqlite3.connect(f"Databases_old/users/{user_id}.db")
    user_cursor = user_database.cursor()

    user_cursor.execute('''SELECT boops from single_values''')
    boops = user_cursor.fetchall()[0][0]

    user_database.close()

    return boops

def fetch_bugreports(mode:str, integer:int):
    if mode not in ["all", "primary_key", "user", "latest"]: #grab all, those with a certain primary id, all from a specific user's id, or the n latest submissions
        raise ValueError("For the \'mode\' argument specify either \'all\' for all entries, \'primary_key\' for search by primary key (given as 'integer'), \'user\' for all entries from a given id (given in the 'integer' arg), or \'latest\' for the <integer> latest entries.")

    submissions_database = sqlite3.connect(f"Databases_old/misc/submissions.db")
    cursor = submissions_database.cursor()

    if mode == "all":
        cursor.execute('''SELECT ID, user_id, content, timestamp FROM bugreports''')
        data = cursor.fetchall()
        submissions_database.close()
        return data
    elif mode == "primary_key":
        cursor.execute('''SELECT user_id, content, timestamp FROM bugreports WHERE ID = ? ''', (integer,))
        data = cursor.fetchall()
        submissions_database.close()
        return data
    elif mode == "user":
        init_user(integer)
        cursor.execute('''SELECT ID, content, timestamp FROM bugreports WHERE user_id = ? ''', (integer,))
        data = cursor.fetchall()
        submissions_database.close()
        return data
    elif mode == "latest":
        cursor.execute('''SELECT ID, user_id, content, timestamp FROM bugreports ORDER BY timestamp''')
        data = cursor.fetchall()[-integer:]
        submissions_database.close()
        return data

def fetch_suggestions(mode:str, integer:int):
    if mode not in ["all", "primary_key", "user", "latest"]: #grab all, those with a certain primary id, all from a specific user's id, or the n latest submissions
        raise ValueError("For the \'mode\' argument specify either \'all\' for all entries, \'primary_key\' for search by primary key (given as 'integer'), \'user\' for all entries from a given id (given in the 'integer' arg), or \'latest\' for the <integer> latest entries.")

    submissions_database = sqlite3.connect(f"Databases_old/misc/submissions.db")
    cursor = submissions_database.cursor()

    if mode == "all":
        cursor.execute('''SELECT ID, user_id, content, timestamp FROM suggestions''')
        data = cursor.fetchall()
        submissions_database.close()
        return data
    elif mode == "primary_key":
        cursor.execute('''SELECT user_id, content, timestamp FROM suggestions WHERE ID = ? ''', (integer,))
        data = cursor.fetchall()
        submissions_database.close()
        return data
    elif mode == "user":
        init_user(integer)
        cursor.execute('''SELECT ID, content, timestamp FROM suggestions WHERE user_id = ? ''', (integer,))
        data = cursor.fetchall()
        submissions_database.close()
        return data
    elif mode == "latest":
        cursor.execute('''SELECT ID, user_id, content, timestamp FROM suggestions ORDER BY timestamp''')
        data = cursor.fetchall()[-integer:]
        submissions_database.close()
        return data
        

def fetch_coolness(user_id):
    #if type(user_id) == int: #assume user id is a user id
    init_user(user_id)
    user_database = sqlite3.connect(f"Databases_old/users/{user_id}.db")
    user_cursor = user_database.cursor()

    user_cursor.execute('''SELECT coolness from single_values''')
    coolness = user_cursor.fetchall()[0][0]

    user_database.close()
    
    #return exp then level
    return (coolness, -(math.floor(((coolness/1.6)-coolness)/130)))
    #elif type(user_id) == str and user_id == 'all': #person has given the string 'all', thus all user levels will be given.
    #    userlist = 
    #    print(userlist)
    #    return userlist
    #    print([filename.name[:-3] for filename in os.scandir("")])


def fetch_inventory(user_id:int, all_items:bool=True, item:str=None):
    init_user(user_id)

    if item == None and all_items == False:
        raise ValueError("No item to lookup despite all_items being False.")

    if item != None and all_items == False:
        if item not in item_json.keys():
            raise KeyError(f"Invalid item for lookup: \"{item}\"")

    user_database = sqlite3.connect(f"Databases_old/users/{user_id}.db")
    user_cursor = user_database.cursor()

    if all_items:
        user_cursor.execute('''SELECT item_name, quantity FROM inventory''')
        data = user_cursor.fetchall()
        data = {elm[0]:elm[1] for elm in data}
        user_database.close()
        return data
    else:
        user_cursor.execute('''SELECT quantity FROM inventory WHERE item_name = ? ''', (str(item),))
        data = user_cursor.fetchall()
        user_database.close()
        return data[0][0]

def fetch_prefixes():

    database = sqlite3.connect(f"Databases_old/misc/prefixes.db")
    cursor = database.cursor()

    cursor.execute('''SELECT guild_id, prefix FROM prefixes''')
    data = cursor.fetchall()
    database.close()

    data = {elm[0]:elm[1] for elm in data}
    return data

def fetch_setting(group:str, id:int,setting:str):
    if group not in ["servers", "users"]:
        raise KeyError

    #check if setting even exists
    if setting not in list(settings_json[group].keys()):
        raise KeyError

    if group == "users":
        init_user(id)
    else:
        init_server(id)

    database = sqlite3.connect(f"Databases_old/{group}/{id}.db")
    cursor = database.cursor()

    cursor.execute('''SELECT value FROM settings WHERE option = ? ''', (str(setting),))
    fetched_setting = cursor.fetchall()
    if len(fetched_setting) == 0:
        cursor.execute('''INSERT into settings values (?,?)''', (str(setting), str(settings_json[group][setting]["default"])))
        database.commit()
        database.close()
        return int(settings_json[group][setting]["default"])
    else:
        database.close()
        return int(fetched_setting[0][0])

def omit_data(user_id:int=0, table:str="none", drop:bool=False, obliterate:bool=False):
    init_user(user_id)

    user_database = sqlite3.connect(f"Databases_old/users/{user_id}.db")
    user_cursor = user_database.cursor()

    if obliterate == False:
        user_cursor.execute(f'''{'DROP' if drop else 'DELETE from'} ?;''', (str(table),))
        user_database.commit()
        user_database.close()
    else: #boom!
        user_database.commit()
        user_database.close()
        os.remove(f'Databases_old/users/{user_id}.db')

    #remove user from balance or inventory databases, or both

def refresh_cooldown(user_id:int, entry:str):
    init_user(user_id)

    if entry not in cooldowns_json.keys():
        raise KeyError("this isnt a valid cooldown")

    user_database = sqlite3.connect(f"Databases_old/users/{user_id}.db")
    user_cursor = user_database.cursor()

    user_cursor.execute('''UPDATE cooldowns SET timestamp = ? WHERE name = ? ''', (int(time.time()), str(entry)))

    user_database.commit()
    user_database.close()

def alter_items(user_id:int, mode:str, items:dict): #set, take, or overwrite to. takes dict and mode
    init_user(user_id)
    #mode can be (add, take is delta), set or overwrite_all
    #items = {
    #    "stick":1,
    #    "rock" :3
    # }
    if mode not in ["delta", "set", "overwrite_all"]: #make sure mode is valid
        raise ValueError("invalid input for 'mode'; please input a choice between delta, set or overwrite_all.")

    for item in items.keys(): #make sure items are valid.
        if item not in item_json.keys():
            raise ValueError(f"{item} is not a valid item.")

    user_database = sqlite3.connect(f"Databases_old/users/{user_id}.db")
    user_cursor = user_database.cursor()

    if mode == "delta": #change existing values of items given
        for item, quantity in items.items(): # lol items.items
            user_cursor.execute('''SELECT quantity FROM inventory WHERE item_name = ?''', (item,))
            current_quantity = user_cursor.fetchall()[0][0]
            end_quantity = quantity+current_quantity
            user_cursor.execute('''UPDATE inventory SET quantity = ? WHERE item_name = ?''', (int(end_quantity), str(item)))
    
    elif mode == "set": #set the values of the items given
        for item, quantity in items.items(): # lol items.items
            user_cursor.execute('''UPDATE inventory SET quantity = ? WHERE item_name = ?''', (int(quantity), str(item)))
    
    elif mode == "overwrite_all": #replace the current inv with items given, all others not specified are set to zero.
        for item in item_json.keys():
            new_quantity = items[item] if item in items.keys() else 0
            user_cursor.execute('''UPDATE inventory SET quantity = ? WHERE item_name = ?''', (int(new_quantity), str(item)))

    user_database.commit()
    user_database.close()
    #if item == None and all_items == False:
    #    raise ValueError("No item to lookup despite all_items being False.")
    #
    #if item != None and all_items == False:
    #    if item not in item_json.keys():
    #        raise KeyError(f"Invalid item for lookup: \"{item}\"")
    #
    #user_database = sqlite3.connect(f"Databases_old/users/{user_id}.db")
    #user_cursor = user_database.cursor()
    #
    #if all_items:
    #    user_cursor.execute('''SELECT item_name, quantity FROM inventory''')
    #    data = user_cursor.fetchall()
    #    data = {elm[0]:elm[1] for elm in data}
    #    return data
    #else:
    #    user_cursor.execute(f'''SELECT quantity FROM inventory WHERE item_name = '{item}' ''')
    #    data = user_cursor.fetchall()
    #    return data[0][0]
    pass

def remove_reminders(ids:list):#removes the reminders with the ids in the list
    reminder_database = sqlite3.connect(f"Databases_old/misc/reminders.db")
    cursor = reminder_database.cursor()
    for primary_key in ids:
        cursor.execute('''DELETE FROM reminders WHERE ID = ?''',(int(primary_key),))
    reminder_database.commit()
    reminder_database.close()

def add_reminder(content:str, timestamp:int, author_id:int, guild_id:int, channel_id:int):
    reminder_database = sqlite3.connect(f"Databases_old/misc/reminders.db")
    cursor = reminder_database.cursor()
    cursor.execute('''INSERT INTO reminders (content, timestamp, author_id, guild_id, channel_id) values (?,?,?,?,?)''',(content, timestamp, author_id, guild_id, channel_id))
    reminder_database.commit()
    reminder_database.close()
    return cursor.lastrowid
    #database_utils.insert_reminder(content, delta, message.author.id, message.guild.id, message.channel.id)

def alter_prefix(guild_ids:list, mode:str, prefix:str):

    database = sqlite3.connect(f"Databases_old/misc/prefixes.db")
    cursor = database.cursor()

    if mode not in ["insert", "update", "remove"]:
        raise KeyError("mode argument must be update or remove or insert, their meaning is self explanatory.") #il probably change the message here

    if mode == "insert": #yes this is larger but i think is probably faster than the method with less code
        for guild_id in guild_ids:
            init_server(guild_id)
            cursor.execute('''SELECT prefix FROM prefixes WHERE guild_id = ?''', (guild_id,))
            if len(cursor.fetchall()) == 0:
                cursor.execute('''INSERT into prefixes values (?,?)''', (guild_id,prefix))
            else:
                cursor.execute('''UPDATE prefixes set prefix = ? WHERE guild_id = ?''', (prefix, guild_id))

    elif mode == "update":
        for guild_id in guild_ids:
            init_server(guild_id)
            cursor.execute('''SELECT prefix FROM prefixes WHERE guild_id = ?''', (guild_id,))
            if len(cursor.fetchall()) == 0:
                cursor.execute('''INSERT into prefixes values (?,?)''', (guild_id,prefix))
            else:
                cursor.execute('''UPDATE prefixes set prefix = ? WHERE guild_id = ?''', (prefix, guild_id))

    elif mode == "remove":
        for guild_id in guild_ids:
            init_server(guild_id)
            cursor.execute('''SELECT prefix FROM prefixes WHERE guild_id = ?''', (guild_id,))
            if len(cursor.fetchall()) != 0:
                cursor.execute('''DELETE FROM prefixes WHERE guild_id = ?''', (guild_id,))

    database.commit()
    database.close()

def alter_setting(group:str,id:int,setting:str,value:int=0,todefault:bool=False):
    if group not in ["servers", "users"]:
        raise KeyError

    if group == "users":
        init_user(id)
    else:
        init_server(id)

    #check if setting even exists
    if setting not in list(settings_json[group].keys()):
        raise KeyError

    database = sqlite3.connect(f"Databases_old/{group}/{id}.db")
    cursor = database.cursor()

    new_value = value if todefault == False else settings_json[setting]["default"]

    cursor.execute('''SELECT value FROM settings WHERE option = ?''', (setting,))
    if len(cursor.fetchall()) == 0:
        cursor.execute('''INSERT into settings values (?,?)''', (str(setting),int(new_value)))
    else:
        cursor.execute('''UPDATE settings set value = ? WHERE option = ?''', (int(new_value), str(setting)))

    database.commit()
    database.close()

def alter_cards(mode, changes:dict): #SELECT * FROM table WHERE id IN (SELECT id FROM table ORDER BY RANDOM() LIMIT x)
    if mode not in ["white", "black"]:
        raise ValueError("please pick either white or black as the mode argument for fetch_cards")

    cah_database = sqlite3.connect(f"Databases_old/misc/cards_against_humanity.db")
    cursor = cah_database.cursor()
    insert_ids = {}
    for primary_key in changes["delete"]:
        cursor.execute(f'''DELETE FROM {mode} WHERE ID = ?''',(int(primary_key),))
    for value in changes["insert"]: #(content, author_id)
        cursor.execute(f'''INSERT into {mode} (content, author_id) values (?,?)''', (value[0], value[1]))
        insert_ids.update({cursor.lastrowid: value[0]})
    #cursor.execute('''SELECT * FROM ? WHERE ID IN (SELECT ID FROM ? ORDER BY RANDOM() LIMIT ?)''', (mode, mode, amount))
    cah_database.commit()
    cah_database.close()
    return insert_ids

def alter_bugreports(changes:dict):#mode:str,ids:list,contents:str):
    #dict with "delete" and "insert" items, delete having [primary_key,], insert having {user_id:content,}

    submissions_database = sqlite3.connect(f"Databases_old/misc/submissions.db")
    cursor = submissions_database.cursor()

    for primary_key in changes["delete"]:
        cursor.execute('''DELETE FROM bugreports WHERE ID = ?''',(int(primary_key),))
    for user_id, content in changes["insert"].items():
        cursor.execute('INSERT into bugreports (user_id,content,timestamp) values (?,?,?)', (user_id, content,int(time.time())))

    submissions_database.commit()
    submissions_database.close()

def alter_suggestions(changes:dict):#mode:str,ids:list,contents:str):
    #dict with "delete" and "insert" items, delete having [primary_key,], insert having {user_id:content,}

    submissions_database = sqlite3.connect(f"Databases_old/misc/submissions.db")
    cursor = submissions_database.cursor()

    for primary_key in changes["delete"]:
        cursor.execute('''DELETE FROM suggestions WHERE ID = ?''',(int(primary_key),))
    for user_id, content in changes["insert"].items():
        cursor.execute('INSERT into suggestions (user_id,content,timestamp) values (?,?,?)', (user_id, content,int(time.time())))

    submissions_database.commit()
    submissions_database.close()

def alter_coolness(user_id:int,value:int,overwrite:bool=False):
    init_user(user_id)

    user_database = sqlite3.connect(f"Databases_old/users/{user_id}.db")
    user_cursor = user_database.cursor()

    user_cursor.execute('''SELECT coolness from single_values''')
    coolness = user_cursor.fetchall()[0][0]

    delta = value if overwrite else coolness+value

    user_cursor.execute('''UPDATE single_values set coolness = ?''', (int(delta),))
    
    user_database.commit()
    user_database.close()

    return (coolness, delta)

def alter_boops(user_id:int,value:int,overwrite:bool=False):
    init_user(user_id)

    user_database = sqlite3.connect(f"Databases_old/users/{user_id}.db")
    user_cursor = user_database.cursor()

    user_cursor.execute('''SELECT boops from single_values''')
    boops = user_cursor.fetchall()[0][0]

    delta = value if overwrite else boops+value

    user_cursor.execute('''UPDATE single_values set boops = ?''', (int(delta),))
    
    user_database.commit()
    user_database.close()

    return (boops, delta)

def alter_balance(user_id:int, value:int, overwrite:bool=False):
    init_user(user_id)

    user_database = sqlite3.connect(f"Databases_old/users/{user_id}.db")
    user_cursor = user_database.cursor()

    user_cursor.execute('''SELECT balance from single_values''')
    balance = user_cursor.fetchall()[0][0]

    delta = value if overwrite else balance+value

    user_cursor.execute('''UPDATE single_values set balance = ?''', (int(delta),))

    user_database.commit()
    user_database.close()

    return (balance, delta)

# transfers all user data from old database to new database
def transfer_all_data():

    # get all user ids
    user_ids = []
    for file in os.listdir("Databases_old/users"):
        if file.endswith(".db"):
            user_ids.append(int(file[:-3]))

    # transfer data for each user
    for user_id in user_ids:
        initialize_user(user_id)
        everything = sqlite3.connect("Resources/everything.db")
        cursor = everything.cursor()
        
        # transfer balance
        balance = fetch_balance(user_id)
        cursor.execute('''UPDATE users set balance = ? WHERE discord_id = ?''', (balance, user_id))

        # transfer coolness 
        coolness = fetch_coolness(user_id)[0]
        cursor.execute('''UPDATE users set coolness = ? WHERE discord_id = ?''', (coolness, user_id))

        # (don't transfer boops)

        # transfer settings
        settings = []
        for setting in settings_json["users"].keys():
            if setting != "ghost_command_output":
                settings.append([setting, fetch_setting("users", user_id, setting)])

        for setting in settings:
            cursor.execute('''UPDATE user_settings set value = ? WHERE (user_id = ? AND option = ?)''', (setting[1], user_id, setting[0]))
        #cursor.executemany('''UPDATE users set "{}" = ? WHERE discord_id = ?'''.format(settings[0]), settings)

        # transfer inventory
        inventory = fetch_inventory(user_id)

        for key, value in inventory.items():
            cursor.execute('''
            INSERT INTO inventory VALUES (?,?,?)
            ''', (user_id, key, value))

        # transfer cah cards
        cah_database = sqlite3.connect(f"Databases_old/misc/cards_against_humanity.db")
        cah_cursor = cah_database.cursor()

        cah_cursor.execute('''SELECT content FROM white WHERE author_id = ?''', (user_id,))
        white_cards = cah_cursor.fetchall()
        cah_cursor.execute('''SELECT content FROM black WHERE author_id = ?''', (user_id,))
        black_cards = cah_cursor.fetchall()

        cah_database.close()

        cursor.executemany('''
        INSERT INTO cards_against_humanity (user_id, content, type) VALUES (?, ?, ?)
        ''', [(user_id, card[0], "white") for card in white_cards] + [(user_id, card[0], "black") for card in black_cards])
        
        everything.commit()
        everything.close()

    print("users done, doing guilds")
    # transfer all guild settings

    guild_ids = []
    for file in os.listdir("Databases_old/servers"):
        if file.endswith(".db"):
            guild_ids.append(int(file[:-3]))


    for guild_id in guild_ids:
        initialize_server(guild_id)
        everything = sqlite3.connect("Resources/everything.db")
        cursor = everything.cursor()

        # transfer settings
        settings = []
        for setting in settings_json["servers"].keys():
            settings.append([setting, fetch_setting("servers", guild_id, setting)])

        for setting in settings:
            cursor.execute('''UPDATE guild_settings set value = ? WHERE (guild_id = ? AND option = ?)''', (setting[1], guild_id, setting[0]))

        #settings = []
        #for setting in settings_json["servers"].keys():
        #    settings.append([setting, fetch_setting("servers", guild_id, setting)])
        #
        #cursor.executemany('''UPDATE guilds set ? = ? WHERE guild_id = ?''', settings)

        everything.commit()
        everything.close()

    # transfer all misc data
    everything = sqlite3.connect("Resources/everything.db")
    cursor = everything.cursor()

    # transfer all suggestions
    submissions_database = sqlite3.connect(f"Databases_old/misc/submissions.db")
    submissions_cursor = submissions_database.cursor()

    submissions_cursor.execute('''SELECT user_id, content, timestamp FROM suggestions''')
    suggestions = submissions_cursor.fetchall()

    submissions_cursor.execute('''SELECT user_id, content, timestamp FROM bugreports''')
    bugreports = submissions_cursor.fetchall()

    submissions_database.close()

    cursor.executemany('''
    INSERT INTO suggestions (user_id, content, timestamp) VALUES (?, ?, ?)
    ''', tuple(suggestions))
    
    cursor.executemany('''
    INSERT INTO bugreports (user_id, content, timestamp) VALUES (?,?,?)
    ''', tuple(bugreports))
"""