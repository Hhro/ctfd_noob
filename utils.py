import requests
import json
import sys
from pathlib import Path
from bs4 import BeautifulSoup

is_file_exists = lambda f : Path(f).exists()

def get_html(url):
    _html = ''
    resp = requests.get(url)
    if resp.status_code == 200:
        _html = resp.text
        return _html

def get_cookies(url):
    resp = requests.get(url)
    return resp.cookies

def get_ssid_nonce(url,ssid=''):
    if ssid == '':
        resp = requests.get(url)
        ssid = resp.cookies['session']

    resp = requests.get(url,cookies={"session":ssid})
    soup = BeautifulSoup(resp.text,'html.parser')
    for x in soup.findAll('input'):
        if x.attrs['name'] == 'nonce':
            nonce = x.attrs['value']
    
    return ssid,nonce

def save_json_into_file(json_dict,save_dir,file_name,opt='new'):
        save_dir.mkdir(parents=True,exist_ok=True)
        
        if opt == 'new':
                with open(str(save_dir / file_name), "w") as json_out:
                        json.dump(json_dict,json_out)
                        json_out.close()
        if opt =='modify':
                with open(str(save_dir / file_name), "r") as json_in:
                        json_data = json.load(json_in)
                        json_in.close()
                json_data.update(json_dict)

                with open(str(save_dir / file_name), "w") as json_out:
                        json.dump(json_data,json_out)
                        json_out.close()
                
        return True

def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()