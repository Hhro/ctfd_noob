import json
import os.path

is_db_exist = lambda : os.path.isfile("accounts.json")

def cache_account(base_url,account):
    accounts = {}

    if not is_db_exist():
        with open("accounts.json","w") as accounts_json:
            accounts_json.write("{}")
            accounts_json.close()
    
    with open("accounts.json","r") as accounts_json:
        accounts = json.load(accounts_json)
        accounts_json.close()
    
    accounts.update({base_url:account})

    with open("accounts.json","w") as accounts_json:
        json.dump(accounts,accounts_json)
        accounts_json.close()