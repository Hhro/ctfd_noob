import ctfd
import requests
import utils
from bs4 import BeautifulSoup

def parse_CTFd_sitemap(base_url):
    home = base_url
    urls = set()
    other_sites = set()

    home_html = utils.get_html(home)
    soup = BeautifulSoup(home_html, 'html.parser')

    for link in soup.findAll("a"):
        if 'href' in link.attrs:
            url = link.attrs['href']
            if url.startswith('#'):
                continue
            if not url.startswith('/'):
                other_sites.add(link.attrs['href'])
                continue
            urls.add(link.attrs['href'])
    
    return urls,other_sites

def prepare_register(register_url):
    form={}
    ssid, nonce = utils.get_ssid_nonce(register_url)

    resp = requests.get(register_url)
    soup = BeautifulSoup(resp.text,'html.parser')

    for required in soup.findAll('input'):
        if required.attrs['name'] != 'nonce':
            form.update({required.attrs['name']:''})
    
    return form, nonce, ssid
