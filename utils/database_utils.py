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
    pass
    submission_database = sqlite3.connect(f"Databases/submissions/submissions.db")
    cursor = submission_database.cursor()
    cursor.execute(f'''SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = 'suggestions' ''')
    if cursor.fetchone()[0] == 0:
        cursor.execute(f'''CREATE TABLE suggestions (
            ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
            user_id INTEGER,
            content TEXT
        )''')
    cursor.execute(f'''SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = 'bugreports' ''')
    if cursor.fetchone()[0] == 0:
        cursor.execute(f'''CREATE TABLE bugreports (
            ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
            user_id INTEGER,
            content TEXT
        )''')
    
    submission_database.commit()
    submission_database.close()

def init_user(user_id):  #inits a user's balance, inventory and preferences. try to make this efficient.
    
    user_database = sqlite3.connect(f"Databases/users/{user_id}.db")
    user_cursor = user_database.cursor()

    #single values, balance, exp etc
    user_cursor.execute(f'''SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = 'single_values' ''')
    if user_cursor.fetchone()[0] == 0:
        user_cursor.execute(f'''CREATE TABLE single_values (
            balance INTEGER, 
            coolness INTEGER,
            boops INTEGER
        )''')
        user_cursor.execute(f'''INSERT into single_values values (
            100,
            0,
            0
        )''')

    #inventory
    user_cursor.execute(f'''SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = 'inventory' ''')
    if user_cursor.fetchone()[0] == 0:
        user_cursor.execute(f'''CREATE TABLE inventory (
            item_name TEXT,
            quantity INTEGER
        )''') #perhaps add flags when switching to mode two for storage; item nbt and such
    
    #remove unknown items
    user_cursor.execute(f'''SELECT item_name FROM inventory''')
    data = user_cursor.fetchall()

    if len(data) > 0:
        for item in data:
            if item[0] not in list(item_json.keys()):
                user_cursor.execute(f'''DELETE FROM inventory WHERE item_name = '{item[0]}' ''')

    #add in all items
    for item in item_json.keys():
        user_cursor.execute(f'''SELECT quantity FROM inventory WHERE item_name = '{item}' ''')
        fetched_item = user_cursor.fetchall()
        if len(fetched_item) == 0:
            user_cursor.execute(f'''INSERT into inventory values ('{item}', {"1" if item == "biscuit" else "0"})''')


    #settings
    user_cursor.execute(f'''SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = 'settings' ''')
    if user_cursor.fetchone()[0] == 0:
        user_cursor.execute(f'''CREATE TABLE settings (
            option TEXT,
            value INTEGER
        )''')


    #remove unknown settings
    user_cursor.execute(f'''SELECT option FROM settings''')
    data = user_cursor.fetchall()

    if len(data) > 0:
        for setting in data:
            if setting[0] not in list(settings_json["users"].keys()):
                user_cursor.execute(f'''DELETE FROM settings WHERE option = '{setting[0]}' ''')

    #add in all settings
    for setting in settings_json["users"].keys():
        user_cursor.execute(f'''SELECT value FROM settings WHERE option = '{setting}' ''')
        fetched_setting = user_cursor.fetchall()
        if len(fetched_setting) == 0:
            user_cursor.execute(f'''INSERT into settings values ('{setting}', '{int(settings_json["users"][setting]["default"])}')''')

    #cooldowns
    user_cursor.execute(f'''SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = 'cooldowns' ''')
    if user_cursor.fetchone()[0] == 0:
        user_cursor.execute(f'''CREATE TABLE cooldowns (
            name TEXT,
            timestamp INTEGER
        )''') 
    
    #remove unknown entries
    user_cursor.execute(f'''SELECT name FROM cooldowns''')
    data = user_cursor.fetchall()

    if len(data) > 0:
        for entry in data:
            if entry[0] not in list(cooldowns_json.keys()):
                user_cursor.execute(f'''DELETE FROM cooldowns WHERE name = '{entry[0]}' ''')

    #add in all entries
    for entry in cooldowns_json.keys():
        user_cursor.execute(f'''SELECT timestamp FROM cooldowns WHERE name = '{entry}' ''')
        fetched_timestamp = user_cursor.fetchall()
        if len(fetched_timestamp) == 0:
            user_cursor.execute(f'''INSERT into cooldowns values ('{entry}', {int(time.time())-cooldowns_json[entry]}) ''')

    user_database.commit()

    user_database.close()

def init_server(server_id):
    server_database = sqlite3.connect(f"Databases/servers/{server_id}.db")
    server_cursor = server_database.cursor()

    #settings
    server_cursor.execute(f'''SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = 'settings' ''')
    if server_cursor.fetchone()[0] == 0:
        server_cursor.execute(f'''CREATE TABLE settings (
            option TEXT,
            value INTEGER
        )''')

    #remove unknown settings
    server_cursor.execute(f'''SELECT option FROM settings''')
    data = server_cursor.fetchall()

    if len(data) > 0:
        for setting in data:
            if setting[0] not in list(settings_json["servers"].keys()):
                server_cursor.execute(f'''DELETE FROM settings WHERE option = '{setting[0]}' ''')

    #add in all settings
    for setting in settings_json["servers"].keys():
        server_cursor.execute(f'''SELECT value FROM settings WHERE option = '{setting}' ''')
        fetched_setting = server_cursor.fetchall()
        if len(fetched_setting) == 0:
            server_cursor.execute(f'''INSERT into settings values ('{setting}', '{int(settings_json["servers"][setting]["default"])}')''')
    
    server_database.commit()

    server_database.close()


def fetch_timedelta(user_id:int, entry:str):
    # returns how many seconds in the past that the timestamp represents.
    init_user(user_id)

    if entry not in cooldowns_json.keys():
        raise KeyError("this isnt a valid cooldown")

    user_database = sqlite3.connect(f"Databases/users/{user_id}.db")
    user_cursor = user_database.cursor()

    user_cursor.execute(f''' SELECT timestamp FROM cooldowns WHERE name = '{entry}' ''')
    data = user_cursor.fetchall()[0][0]

    user_database.commit()
    user_database.close()

    return int(time.time())-data

def fetch_balance(user_id:int):
    init_user(user_id)
    user_database = sqlite3.connect(f"Databases/users/{user_id}.db")
    user_cursor = user_database.cursor()

    user_cursor.execute(f'''SELECT balance from single_values''')
    balance = user_cursor.fetchall()[0][0]

    user_database.close()

    return balance

def fetch_boops(user_id):
    init_user(user_id)
    user_database = sqlite3.connect(f"Databases/users/{user_id}.db")
    user_cursor = user_database.cursor()

    user_cursor.execute(f'''SELECT boops from single_values''')
    boops = user_cursor.fetchall()[0][0]

    user_database.close()

    return boops


def fetch_coolness(user_id):
    init_user(user_id)
    user_database = sqlite3.connect(f"Databases/users/{user_id}.db")
    user_cursor = user_database.cursor()

    user_cursor.execute(f'''SELECT coolness from single_values''')
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
        return data
    else:
        user_cursor.execute(f'''SELECT quantity FROM inventory WHERE item_name = '{item}' ''')
        data = user_cursor.fetchall()
        return data[0][0]

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

    cursor.execute(f'''SELECT value FROM settings WHERE option = '{setting}' ''')
    fetched_setting = cursor.fetchall()
    if len(fetched_setting) == 0:
        cursor.execute(f'''INSERT into settings values ('{setting}', '{settings_json[group][setting]["default"]}')''')
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
        user_cursor.execute(f'''{'DROP' if drop else 'DELETE from'} {table};''')
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

    user_cursor.execute(f'''UPDATE cooldowns SET timestamp = {int(time.time())} WHERE name = '{entry}' ''')

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
            user_cursor.execute(f'''SELECT quantity FROM inventory WHERE item_name = '{item}' ''')
            current_quantity = user_cursor.fetchall()[0][0]
            end_quantity = quantity+current_quantity
            user_cursor.execute(f'''UPDATE inventory SET quantity = {end_quantity} WHERE item_name = '{item}' ''')
    
    elif mode == "set": #set the values of the items given
        for item, quantity in items.items(): # lol items.items
            user_cursor.execute(f'''UPDATE inventory SET quantity = {quantity} WHERE item_name = '{item}' ''')
    
    elif mode == "overwrite_all": #replace the current inv with items given, all others not specified are set to zero.
        for item in item_json.keys():
            new_quantity = items[item] if item in items.keys() else 0
            user_cursor.execute(f'''UPDATE inventory SET quantity = {new_quantity} WHERE item_name = '{item}' ''')

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

    cursor.execute(f'''SELECT value FROM settings WHERE option = '{setting}' ''')
    if len(cursor.fetchall()) == 0:
        cursor.execute(f'''INSERT into settings values ('{setting}', {new_value})''')
    else:
        cursor.execute(f'''UPDATE settings set value = {new_value} WHERE option = '{setting}' ''')

    database.commit()
    database.close()


def alter_coolness(user_id:int,value:int,overwrite:bool=False):
    init_user(user_id)

    user_database = sqlite3.connect(f"Databases/users/{user_id}.db")
    user_cursor = user_database.cursor()

    user_cursor.execute(f'''SELECT coolness from single_values''')
    coolness = user_cursor.fetchall()[0][0]

    delta = value if overwrite else coolness+value

    user_cursor.execute(f'''UPDATE single_values set coolness = {delta}''')
    
    user_database.commit()
    user_database.close()

    return (coolness, delta)

def alter_boops(user_id:int,value:int,overwrite:bool=False):
    init_user(user_id)

    user_database = sqlite3.connect(f"Databases/users/{user_id}.db")
    user_cursor = user_database.cursor()

    user_cursor.execute(f'''SELECT boops from single_values''')
    boops = user_cursor.fetchall()[0][0]

    delta = value if overwrite else boops+value

    user_cursor.execute(f'''UPDATE single_values set boops = {delta}''')
    
    user_database.commit()
    user_database.close()

    return (boops, delta)

def alter_balance(user_id:int, value:int, overwrite:bool=False):
    init_user(user_id)

    user_database = sqlite3.connect(f"Databases/users/{user_id}.db")
    user_cursor = user_database.cursor()

    user_cursor.execute(f'''SELECT balance from single_values''')
    balance = user_cursor.fetchall()[0][0]

    delta = value if overwrite else balance+value

    user_cursor.execute(f'''UPDATE single_values set balance = {delta}''')

    user_database.commit()
    user_database.close()

    return (balance, delta)