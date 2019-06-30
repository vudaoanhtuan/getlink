import re
import requests
import json
from bs4 import BeautifulSoup

def get_link(url):
    # get id from url
    sid = re.search('/([\w]{15})\??', url).groups()
    if len(sid) != 1:
        raise Exception("Invalid url")
    link_id = sid[0]
    
    # init session
    session = requests.Session()
    
    # get csrf value
    html_res = session.get('https://www.fshare.vn/file/'+link_id)
    html = BeautifulSoup(html_res.text)
    csrf_value = html.select_one('#form-signup > input[type=hidden]')['value']
    
    # get link download
    download_data = {
        '_csrf-app': csrf_value,
        'linkcode': link_id,
        'withFcode5': '0',
        'fcode': ''
    }
    
    link_res = session.post('https://www.fshare.vn/download/get', data=download_data)
    try:
        info = link_res.json()
        direct_url = info['url']
        return direct_url
    except:
        raise Exception("Link is dead")
    return ''