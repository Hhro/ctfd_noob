import os
import shutil
from pathlib import Path
from urllib.parse import urljoin

class Manager(object):
    def __init__(self,ctfd,user):
        self.ctfd=ctfd
        self.user=user
    
    def download_all_challenges_files(self,loc=''):
        base_url = self.ctfd.base_url
        ssid = self.user.session
        header = "Cookie: session={}".format(ssid)
        challenges = self.ctfd.challenges

        if loc == '':
            base_dir = Path.cwd() / self.ctfd.name
        else:
            base_dir = Path(loc) /self.ctfd.name

        for idx,chall_id in enumerate(challenges.keys()):
            chall = challenges[chall_id]
            chall_path = base_dir / chall['category'] / chall['name']
            chall_path.mkdir(parents=True,exist_ok=True)

            if chall['files'] == ['']:
                continue
            file_links = [urljoin(base_url,link) for link in chall['files']]

            for file_link in file_links:
                print("Download challenge {} [{}/{}]".format(chall['name'],idx+1,len(challenges.keys())))
                os.system("wget --header=\"{}\" --content-disposition -P {} {}".format(header,str(chall_path),file_link))
        
        return True

            

