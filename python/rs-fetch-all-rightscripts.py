import sys
import os
import requests
import json

RS_BASE_URL='https://us-4.rightscale.com'
RS_API_VERSION='1.5'
TOKEN=''

# Get the access token
def get_access_token():
    headers={'accept' : 'application/json', 'cache-control':'no-cache', 'x-api-version':RS_API_VERSION}
    data={'grant_type' : 'refresh_token', 'refresh_token':TOKEN}
    r = requests.post(RS_BASE_URL+'/api/oauth2', data, headers=headers)
    ret_json = json.loads(r.text)
    return ret_json['access_token']

# Get all the rightscripts
def get_all_rightscripts():
    headers={'accept' : 'application/json', 'cache-control': 'no-cache', 'x-api-version': RS_API_VERSION,
             'authorization': 'Bearer '+ get_access_token() }
    r = requests.get(RS_BASE_URL+'/api/right_scripts', headers=headers)
    ret_json=json.loads(r.text)

    script_info = {}
    for elem in ret_json:
        script_info[elem['name']] = elem['links'][1]['href']
    return script_info

def download_all_rightscripts():
    for name, url in get_all_rightscripts().items():
        headers={'cache-control':'no-cache', 'x-api-version':RS_API_VERSION,
                 'authorization' : 'Bearer '+ get_access_token() }
        r = requests.get(RS_BASE_URL+ url, headers=headers)
        escaped_name = name.replace('/', '_slash_')
        with open(os.path.join('/Users/ramz.sivagurunathan/projects/sw/work/iag/repos/devlabs/rightscripts/', escaped_name), 'a+') as fp:
            fp.write(r.text)
        print(r.text)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Insufficient argument")
        print("usage: rs-fetch-all-rightscripts.py TOKEN RIGHTSCALE_URL API_VERSION")
    else:
        TOKEN=sys.argv[1]
        RS_BASE_URL=sys.argv[2]
        RS_API_VERSION=sys.argv[3]
        download_all_rightscripts()
