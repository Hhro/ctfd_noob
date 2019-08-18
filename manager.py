import os
import pathlib
import shutil
from urllib.parse import urljoin

class Manager(object):
    def __init__(self,ctfd):
        self.ctfd=ctfd
    
    def download_challenges(self):
        base_url = self.ctfd.base_url
        challenges = self.ctfd.challenges

        #TODO
        for idx,chall_id in enumerate(challenges.keys()):
            chall = challenges[chall_id]
            link = urljoin(base_url,chall['file'])
            print("Download challenge {} [{}/{}]".format(chall['name'],idx+1,len(challenges.keys())))
            
            os.mkdir()


