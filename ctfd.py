import requests
import parser
from user import User

class CTFd(object):
    def __init__(self,base_url):
        self.base_url = base_url
        self.urls=set('/')
        self.other_sites=set()
        self.endpoints={}
        self.challenges={}
    
    def get_CTFd_sitemap(self):
        urls, other_sites = parser.parse_CTFd_sitemap(self.base_url)
        self.urls=self.urls.union(urls)
        self.other_sites=self.other_sites.union(other_sites)
    
    def get_CTFd_endpoints(self):
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
    
    





        