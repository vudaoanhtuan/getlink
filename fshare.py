import re
import requests
import json
import argparse
import time
from bs4 import BeautifulSoup

def get_link_from_id(link_id):
def get_link(url):
    # get id from url
    sid = re.search('/([\w]{10,})\??', url).groups()
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
        redirect_url = info['url']
        wait_time = info['wait_time']
        for i in range(wait_time):
            print("Wait for %ds" % (wait_time-i), end='\r')
            time.sleep(1)
            print(" "*20, end='\r')
        print("Done!")
        response = session.get(info['url'], allow_redirects=False)
        direct_url = response.headers['Location']
        return direct_url
    except:
        raise Exception("Link is dead")


def get_link_from_url(url):
    # get id from url
    sid = re.search('/([\w]{15})\??', url).groups()
    if len(sid) != 1:
        raise Exception("Invalid url")
    link_id = sid[0]
    return get_link_from_id(link_id)


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url')
    parser.add_argument('-i', '--id')

    args = parser.parse_args()
    if args.id is not None:
        print(get_link_from_id(args.id))
    elif args.url is not None:
        print(get_link_from_url(args.url))
    else:
        print(parser.print_help())