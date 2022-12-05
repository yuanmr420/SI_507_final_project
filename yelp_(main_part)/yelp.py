#get data from yelp api
import requests
from urllib.parse import quote
import json

API_KEY= 'bBIGqWedlHoDz9W6dg4krgfHxWTQ54SVKlGGgB3fJyijnbVsrUI2ukIzxFGoXS8Sq4mELh7i26R63Uo4_XgnuOiPS_XJ_q7kdTiDl042OpEzhqirtn_1TTOWDnGIY3Yx'
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'

def request(host, path, api_key, url_params=None):
    url_params = url_params or {}
    url = f"{host}{quote(path.encode('utf8'))}"
    headers = {'Authorization': f'Bearer {api_key}',}
    print(f'Querying {url}')
    response = requests.request('GET', url, headers=headers, params=url_params)
    return response.json()

#parse the json string into class yelp
class Yelp():
    def __init__(self,json_str):
        self.name = json_str['name']
        self.categories = json_str['categories'][0]['alias']
        self.rating = json_str['rating']
        self.location = ' '.join(json_str['location']['display_address'])
        if 'price' not in json_str.keys():
            self.price = None
        else:
            self.price = json_str['price']
        self.url = json_str['url']

#caching the url data
CACHE_FILENAME = 'yelp_cache.json'

def open_cache():
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_content = cache_file.read()
        cache_dict = json.loads(cache_content)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    dump_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME, 'a+')
    fw.write(dump_json_cache)
    fw.close()

def construct_unique_key(baseurl, params):
    param_strings = []
    connector = '_'
    for k in params.keys():
        param_strings.append(f'{k}_{params[k]}')
    param_strings.sort()
    unique_key = baseurl+connector+connector.join(param_strings)
    return unique_key

def request_with_cache(host, path, api_key, url_params,CACHE_DICT):
    request_key = construct_unique_key(path, url_params)
    print(request_key)
    if request_key in CACHE_DICT.keys():
        print('cache hit!', request_key)
        return CACHE_DICT[request_key]
    else:
        print('cache miss!', request_key)
        CACHE_DICT[request_key] = request(host, path, api_key, url_params)
        save_cache(CACHE_DICT)
        return CACHE_DICT[request_key]

def main():
    CACHE_DICT = open_cache()
    base_url = SEARCH_PATH
    key = API_KEY
    host = API_HOST
    params = {'location':'Boston','limit':10,'term':'dinner'}
    results = request_with_cache(host, base_url, key, params,CACHE_DICT)
    yelp_list = [Yelp(restaurant) for restaurant in results['businesses']]


if __name__ == '__main__':
    main()
