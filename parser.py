import ctfd
import requests
from bs4 import BeautifulSoup
from utils import get_html

def parse_CTFd_sitemap(CTFd):
    home = CTFd.base_url
    urls = set()
    other_sites = set()

    home_html = get_html(home)
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

def prepare_register(CTFd):
    register_url = CTFd.base_url+CTFd.endpoints['register']
    form={}
    nonce=''
    session=''

    resp = requests.get(register_url)
    session = resp.cookies['session']

    soup = BeautifulSoup(resp.text,'html.parser')

    for required in soup.findAll('input'):
        if required.attrs['name'] == 'nonce':
            nonce = required.attrs['value']
        else:
            form.update({required.attrs['name']:''})
    
    return form, nonce, session




