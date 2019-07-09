import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-id", type=str)
parser.add_argument("-o", "-output", type=str)


args = parser.parse_args()


lid = args.id
output = args.o



def download_file(lid, filename=None):
    url = 'https://drive.google.com/uc?export=download&id=' + lid

    r = requests.get(url)

    cookies = r.cookies
    ck_key = cookies.keys()

    warning_key = None

    for k in ck_key:
        if 'warning' in k.lower():
            warning_key = k
            break

    if warning_key is not None:
        url = url + '&confirm=' + cookies[warning_key]

    if filename is None:
        filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, cookies=cookies, stream=True) as r:
        r.raise_for_status()

        downloaded_size = 0
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush()
                    downloaded_size += len(chunk)
                    print("Downloading: %f MB" % (downloaded_size*1.0/1024/1024), end='\r')
            f.flush()
    print(" "*100, end='\r')        
    print("Done! File save to %s" % filename)



download_file(lid, output)