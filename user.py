import requests
import json
import accounts
import parser
import utils

class User(object):
    def __init__(self,ctfd):
        self.name=''
        self.pw=''
        self.email=''
        self.session=''
        self.ctfd=ctfd
    
    def register(self):
        register_url = self.ctfd.base_url+self.ctfd.endpoints['register']
        register_form, nonce, ssid = parser.prepare_register(register_url)
        
        print("=====[Register]=====")
        for required in register_form.keys():
            register_form[required] = input(required+": ")
        register_form['nonce'] = nonce

        resp = requests.post(register_url,cookies={'session':ssid},data=register_form)
        
        if "confirmation" in resp.text:
            print("Register success.")
            del(register_form['nonce'])
            accounts.cache_account(self.ctfd.name,register_form)
            print("Account caching complete.")
            return True
        else:
            print("Register failed.")
            print(resp.text)
            return False

    def login(self):
        login_url = self.ctfd.base_url + self.ctfd.endpoints['login']

        print("Check registered account...")
        if not accounts.is_account_hit(self.ctfd.name):
            print("There is no registered account")
            print("Register now")
            if not self.register():
                return False
        else:
            print("There is registered account")

        account = accounts.get_account_cache(self.ctfd.name)
        ssid,nonce = utils.get_ssid_nonce(login_url)
        account.update({"nonce":nonce})
        
        resp = requests.post(login_url,cookies={"session":ssid},data=account,allow_redirects=False)

        if resp.status_code == 302:
            self.name = account['name']
            self.pw = account['password']
            self.email = account['email']
            self.session = resp.cookies['session']
            print("Login succeed")
            return True
        else:
            print("Login failed")
            return False

    def get_challenges(self):
        print("Get challenge meta info")
        challenges = {}

        if self.session == '':
            self.login()

        challenges_endpoint = self.ctfd.base_url + "/api/v1/challenges"

        resp = requests.get(challenges_endpoint,cookies={"session":self.session})

        if resp.status_code==200:
            print("Done.")
            challenges = json.loads(resp.text)['data']

            print("Processing...")
            processed = {}
            for chall in challenges:
                chall['name']=chall['name'].replace(' ','_').lower()
                chall['category']=chall['category'].replace(' ','_').lower()
                del(chall['template'])
                del(chall['script'])
                del(chall['type'])
                processed.update({chall['id']: {key: chall[key] for key in filter(lambda x : x!='id',chall)}})
            print("Done")

            print("Get challenge specific info.(You may need to wait)")
            for chall_id in processed.keys():
                resp=requests.get(challenges_endpoint+'/'+str(chall_id),cookies={"session":self.session})
                chall_info = json.loads(resp.text)['data']

                processed[chall_id]['files']=chall_info['files']
                processed[chall_id]['description']=chall_info['description']
                processed[chall_id]['hint']=chall_info['hints']
                processed[chall_id]['solves']=chall_info['solves']

            print("Merge complete")

            return processed
        else:
            print("Something wrong...")
            print(resp.text)
            return False
    
    def create_team(self):
        print("[Create team]")
        create_team_url = self.ctfd.base_url + self.ctfd.endpoints['teams'] + '/new'

        if self.session == '':
            self.login()

        team_name = input("team name: ")
        team_pw = input("team password: ")
        _, nonce = utils.get_ssid_nonce(create_team_url,self.session)
        login_form = {"name":team_name,"password":team_pw,"nonce":nonce}

        resp=requests.post(create_team_url,cookies={"session":self.session},data=login_form)
        
        if resp.status_code == 200:
            print("[Create team]Done")
            return True
        else:
            print("[Create team]Something wrong...")
            return False
