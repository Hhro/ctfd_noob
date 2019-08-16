import requests

def get_html(url):
    _html = ''
    resp = requests.get(url)
    if resp.status_code == 200:
        _html = resp.text
        return _html

def get_cookies(url):
        resp = requests.get(url)
        return resp.cookies
    