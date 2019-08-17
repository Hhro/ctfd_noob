import json
import os.path

is_db_exist = lambda : os.path.isfile("accounts.json")

def make_empty_db():
    with open("accounts.json","w") as accounts_json:
        accounts_json.write("{}")
        accounts_json.close()

def cache_account(base_url,account):
    accounts = {}

    if not is_db_exist():
        make_empty_db()
    
    with open("accounts.json","r") as accounts_json:
        accounts = json.load(accounts_json)
        accounts_json.close()
    
    accounts.update({base_url:account})

    with open("accounts.json","w") as accounts_json:
        json.dump(accounts,accounts_json)
        accounts_json.close()

def is_account_hit(base_url):
    accounts = {}
    
    if not is_db_exist():
        make_empty_db()
        return False
    
    with open("accounts.json","r") as accounts_json:
        accounts = json.load(accounts_json)
        accounts_json.close()
    
    return base_url in accounts.keys()

def get_account_cache(base_url):
    with open("accounts.json","r") as accounts_json:
        accounts = json.load(accounts_json)
        accounts_json.close()
    
    return accounts[base_url]