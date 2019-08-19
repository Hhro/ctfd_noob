import requests
from bs4 import BeautifulSoup

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

        