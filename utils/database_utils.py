#an import file for economy manipulation methods

# how inv is stored:


#migrate coolness methods to here

import math, sqlite3, os, json, time

with open(os.getcwd()+"/Recources/json/items.json") as file:
    item_json = json.loads(file.read())
with open(os.getcwd()+"/Recources/json/misc_economy.json") as file:
    misc_economy_json = json.loads(file.read())
with open(os.getcwd()+"/Recources/json/settings_key.json") as file:
    settings_json = json.loads(file.read())
with open(os.getcwd()+"/Recources/json/command_cooldowns.json") as file:
    cooldowns_json = json.loads(file.read())

#init suggstions and bug reports:
def init_main():
    submission_database = sqlite3.connect(f"Databases/misc/submissions.db")
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

    prefix_database = sqlite3.connect(f"Databases/misc/prefixes.db")
    cursor = prefix_database.cursor()
    cursor.execute('''SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = 'prefixes' ''')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''CREATE TABLE prefixes (
            guild_id INTEGER,
            prefix TEXT
        )''')

    #cursor.execute('''SELECT guild_id, prefix FROM prefixes''')
    #data = cursor.fetchall()
    #data = {elm[0]:elm[1] for elm in data}
    #print(data, "test")
    #print(Bot.guilds)
    #for guild in Bot.guilds:
    #    print(guild.id)
    #    if guild.id not in list(data.keys()):
    #        print("tst")
    #        cursor.execute('''INSERT into prefixes values (?,?)''', (guild.id, Bot.default_prefix))

    prefix_database.commit()
    prefix_database.close()

def init_user(user_id):  #inits a user's balance, inventory and preferences. try to make this efficient.
    
    user_database = sqlite3.connect(f"Databases/users/{user_id}.db")
    user_cursor = user_database.cursor()

    #single values, balance, exp etc
    user_cursor.execute('''SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = 'single_values' ''')
    if user_cursor.fetchone()[0] == 0:
        user_cursor.execute('''CREATE TABLE single_values (
            balance INTEGER, 
            coolness INTEGER,
            boops INTEGER
        )''')
        user_cursor.execute('''INSERT into single_values values (
            100,
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
    server_database = sqlite3.connect(f"Databases/servers/{server_id}.db")
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


def fetch_timedelta(user_id:int, entry:str):
    # returns how many seconds in the past that the timestamp represents.
    init_user(user_id)

    if entry not in cooldowns_json.keys():
        raise KeyError("this isnt a valid cooldown")

    user_database = sqlite3.connect(f"Databases/users/{user_id}.db")
    user_cursor = user_database.cursor()

    user_cursor.execute(''' SELECT timestamp FROM cooldowns WHERE name = ?''', (str(entry),))
    data = user_cursor.fetchall()[0][0]

    user_database.commit()
    user_database.close()

    return int(time.time())-data

def fetch_balance(user_id:int):
    init_user(user_id)
    user_database = sqlite3.connect(f"Databases/users/{user_id}.db")
    user_cursor = user_database.cursor()

    user_cursor.execute('''SELECT balance from single_values''')
    balance = user_cursor.fetchall()[0][0]

    user_database.close()

    return balance

def fetch_boops(user_id):
    init_user(user_id)
    user_database = sqlite3.connect(f"Databases/users/{user_id}.db")
    user_cursor = user_database.cursor()

    user_cursor.execute('''SELECT boops from single_values''')
    boops = user_cursor.fetchall()[0][0]

    user_database.close()

    return boops

def fetch_bugreports(mode:str, integer:int):
    if mode not in ["all", "primary_key", "user", "latest"]: #grab all, those with a certain primary id, all from a specific user's id, or the n latest submissions
        raise ValueError("For the \'mode\' argument specify either \'all\' for all entries, \'primary_key\' for search by primary key (given as 'integer'), \'user\' for all entries from a given id (given in the 'integer' arg), or \'latest\' for the <integer> latest entries.")

    submissions_database = sqlite3.connect(f"Databases/misc/submissions.db")
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

    submissions_database = sqlite3.connect(f"Databases/misc/submissions.db")
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
    init_user(user_id)
    user_database = sqlite3.connect(f"Databases/users/{user_id}.db")
    user_cursor = user_database.cursor()

    user_cursor.execute('''SELECT coolness from single_values''')
    coolness = user_cursor.fetchall()[0][0]

    user_database.close()

    #return exp then level
    return (coolness, -(math.floor(((coolness/1.6)-coolness)/130)))

def fetch_inventory(user_id:int, all_items:bool=True, item:str=None):
    init_user(user_id)

    if item == None and all_items == False:
        raise ValueError("No item to lookup despite all_items being False.")

    if item != None and all_items == False:
        if item not in item_json.keys():
            raise KeyError(f"Invalid item for lookup: \"{item}\"")

    user_database = sqlite3.connect(f"Databases/users/{user_id}.db")
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

    database = sqlite3.connect(f"Databases/misc/prefixes.db")
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

    database = sqlite3.connect(f"Databases/{group}/{id}.db")
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

def omit_data(user_id:int, table:str, drop:bool=False, obliterate:bool=False):
    init_user(user_id)

    user_database = sqlite3.connect(f"Databases/users/{user_id}.db")
    user_cursor = user_database.cursor()

    if obliterate == False:
        user_cursor.execute(f'''{'DROP' if drop else 'DELETE from'} ?;''', (str(table),))
    else: #boom!
        os.remove(f'Recources/users/{user_id}.db')

    user_database.commit()
    user_database.close()
    #remove user from balance or inventory databases, or both

def refresh_cooldown(user_id:int, entry:str):
    init_user(user_id)

    if entry not in cooldowns_json.keys():
        raise KeyError("this isnt a valid cooldown")

    user_database = sqlite3.connect(f"Databases/users/{user_id}.db")
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

    user_database = sqlite3.connect(f"Databases/users/{user_id}.db")
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
    #user_database = sqlite3.connect(f"Databases/users/{user_id}.db")
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

def alter_prefix(guild_ids:list, mode:str, prefix:str):

    database = sqlite3.connect(f"Databases/misc/prefixes.db")
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

    database = sqlite3.connect(f"Databases/{group}/{id}.db")
    cursor = database.cursor()

    new_value = value if todefault == False else settings_json[setting]["default"]

    cursor.execute('''SELECT value FROM settings WHERE option = ?''', (setting,))
    if len(cursor.fetchall()) == 0:
        cursor.execute('''INSERT into settings values (?,?)''', (str(setting),int(new_value)))
    else:
        cursor.execute('''UPDATE settings set value = ? WHERE option = ?''', (int(new_value), str(setting)))

    database.commit()
    database.close()

def alter_bugreports(changes:dict):#mode:str,ids:list,contents:str):
    #dict with "delete" and "insert" items, delete having [primary_key,], insert having {user_id:content,}

    submissions_database = sqlite3.connect(f"Databases/misc/submissions.db")
    cursor = submissions_database.cursor()

    for primary_key in changes["delete"]:
        cursor.execute('''DELETE FROM bugreports WHERE ID = ?''',(int(primary_key),))
    for user_id, content in changes["insert"].items():
        cursor.execute('INSERT into bugreports (user_id,content,timestamp) values (?,?,?)', (user_id, content,int(time.time())))

    submissions_database.commit()
    submissions_database.close()

def alter_suggestions(changes:dict):#mode:str,ids:list,contents:str):
    #dict with "delete" and "insert" items, delete having [primary_key,], insert having {user_id:content,}

    submissions_database = sqlite3.connect(f"Databases/misc/submissions.db")
    cursor = submissions_database.cursor()

    for primary_key in changes["delete"]:
        cursor.execute('''DELETE FROM suggestions WHERE ID = ?''',(int(primary_key),))
    for user_id, content in changes["insert"].items():
        cursor.execute('INSERT into suggestions (user_id,content,timestamp) values (?,?,?)', (user_id, content,int(time.time())))

    submissions_database.commit()
    submissions_database.close()

def alter_coolness(user_id:int,value:int,overwrite:bool=False):
    init_user(user_id)

    user_database = sqlite3.connect(f"Databases/users/{user_id}.db")
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

    user_database = sqlite3.connect(f"Databases/users/{user_id}.db")
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

    user_database = sqlite3.connect(f"Databases/users/{user_id}.db")
    user_cursor = user_database.cursor()

    user_cursor.execute('''SELECT balance from single_values''')
    balance = user_cursor.fetchall()[0][0]

    delta = value if overwrite else balance+value

    user_cursor.execute('''UPDATE single_values set balance = ?''', (int(delta),))

    user_database.commit()
    user_database.close()

    return (balance, delta)