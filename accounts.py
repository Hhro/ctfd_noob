import json
import os.path
import utils

is_db_exist = lambda : os.path.isfile("accounts.json")

def make_empty_db():
    with open("accounts.json","w") as accounts_json:
        accounts_json.write("{}")
        accounts_json.close()

def cache_account(ctf_name,account):
    accounts = {}

    if not is_db_exist():
        make_empty_db()
    
    with open("accounts.json","r") as accounts_json:
        accounts = json.load(accounts_json)
        accounts_json.close()
    
    accounts.update({ctf_name:account})

    with open("accounts.json","w") as accounts_json:
        json.dump(accounts,accounts_json)
        accounts_json.close()

def is_account_hit(ctf_name):
    accounts = {}
    
    if not is_db_exist():
        make_empty_db()
        return False
    
    with open("accounts.json","r") as accounts_json:
        accounts = json.load(accounts_json)
        accounts_json.close()
    
    return ctf_name in accounts.keys()

def get_account_cache(ctf_name):
    with open("accounts.json","r") as accounts_json:
        accounts = json.load(accounts_json)
        accounts_json.close()
    
    return accounts[ctf_name]