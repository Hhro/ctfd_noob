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
        resp2 = requests.post("http://httpbin.org/post",cookies={'session':ssid},data=register_form)
        print(resp2.text)
        
        if "confirmation" in resp.text:
            print("Register success.")
            del(register_form['nonce'])
            accounts.cache_account(self.ctfd.base_url,register_form)
            print("Account caching complete.")
            return True
        else:
            print("Register failed.")
            print(resp.text)
            return False

    def login(self):
        login_url = self.ctfd.base_url + self.ctfd.endpoints['login']

        print("Check registered account...")
        if not accounts.is_account_hit(self.ctfd.base_url):
            print("There is no registered account")
            print("Register now")
            if not self.register():
                return False
        else:
            print("There is registered account")

        account = accounts.get_account_cache(self.ctfd.base_url)
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
        print("Get challenge info")
        challenges = {}

        if self.session == '':
            self.login()

        challenges_endpoint = self.ctfd.base_url + "/api/v1/challenges"

        resp = requests.get(challenges_endpoint,cookies={"session":self.session})

        if resp.status_code==200:
            print("Done.")
            challenges = json.loads(resp.text)
            return challenges
        else:
            print("Something wrong...")
            print(resp.text)
            return False