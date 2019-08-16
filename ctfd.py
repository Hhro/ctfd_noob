import json
import urllib
import requests
import parser
import accounts
from bs4 import BeautifulSoup
from utils import get_html

class CTFd(object):
    def __init__(self,base_url):
        self.base_url = base_url
        self.urls=set('/')
        self.other_sites=set()
        self.session=''
        self.cfduid=''
        self.endpoints={}
    
    def set_CTFd_sitemap(self):
        urls, other_sites = parser.parse_CTFd_sitemap(self)
        self.urls=self.urls.union(urls)
        self.other_sites=self.other_sites.union(other_sites)
    
    def set_CTFd_endpoints(self):
        for url in self.urls:
            if 'register' in url or 'join' in url:
                self.endpoints.update({"register":url})
            elif 'login' in url:
                self.endpoints.update({"login":url})
            elif 'chall' in url:
                self.endpoints.update({"challenges":url})
            elif 'notifications' in url:
                self.endpoints.update({"notifications":url})
            elif 'teams' in url:
                self.endpoints.update({"teams":url})
            elif 'scoreboard' in url:
                self.endpoints.update({"scoreboard":url})
            elif 'users' in url:
                self.endpoints.update({"users":url})
    
    def register(self):
        register_url = self.base_url+self.endpoints['register']
        register_form, nonce, session = parser.prepare_register(self)
        
        print("=====[Register]=====")
        for required in register_form.keys():
            register_form[required] = input(required+": ")
        register_form['nonce'] = nonce
        
        resp = requests.post(register_url,cookies={'session':session},data=register_form)
        print(resp.text)
        
        if "confirmation" in resp.text:
            print("Register success.")
            del(register_form['nonce'])
            accounts.cache_account(self.base_url,register_form)
            print("Account caching complete.")
        else:
            print("Register failed.")
            print(resp.text)
        