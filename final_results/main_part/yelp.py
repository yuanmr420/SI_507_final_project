#get data from yelp api
import requests
from urllib.parse import quote
import json
import pandas as pd
import secret as se

API_KEY= se.key
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'

#in this part, I get all cities name. Just for collecting some records into the cache file to meet the requirements
#nothing to do with the whole porjetc
city = pd.read_csv("d:\\2022fall 课程资料\\SI 507\\hw\\final project\\cities\\cities.csv")
city_list = []
for row in city.itertuples():
    city_list.append(getattr(row,'City'))
city_list.sort()

def request(host, path, api_key, url_params=None):
    '''get the restaurant data from the given api

    Parameters
    ----------
    host: str
        the yelp api host:'https://api.yelp.com'

    path: str
        on which path we want to search: '/v3/businesses/search'
    
    api_key: str
        the authentic api key got from yelp api
    
    url_params: dict
        the search condition for the restaurant


    Returns
    -------
    response.json(): dict
        the detail information we got from the given url

    '''
    url_params = url_params or {}
    url = f"{host}{quote(path.encode('utf8'))}"
    headers = {'Authorization': f'Bearer {api_key}',}
    print(f'Querying {url}')
    response = requests.request('GET', url, headers=headers, params=url_params)
    return response.json()

#parse the json string into class yelp
#just for easily handling data when using flask
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
        self.image_url = json_str["image_url"]

#caching the url data
CACHE_FILENAME = 'yelp_cache.json'

def open_cache():
    '''open the file that stored what we scrapped before from yelp api

    Parameters
    ----------
    None


    Returns
    -------
    cache_dict: dict
        A dict stored what we scrapped before from yelp api

    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_content = cache_file.read()
        cache_dict = json.loads(cache_content)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    '''save what we scrapped before from yelp api into the cache file

    Parameters
    ----------
    None


    Returns
    -------
    None

    '''
    dump_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME, 'w')
    fw.write(dump_json_cache)
    fw.close()

def construct_unique_key(baseurl, params):
    '''construct the url based on the search params we provided

    Parameters
    ----------
    baseurl: str
        most time it is '/v3/businesses/search'
    
    params: dict
        the search condition for the restaurant


    Returns
    -------
    unique_key: str
        an url based on the given params

    '''
    param_strings = []
    connector = '_'
    for k in params.keys():
        param_strings.append(f'{k}_{params[k]}')
    param_strings.sort()
    unique_key = baseurl+connector+connector.join(param_strings)
    return unique_key

def request_with_cache(host, path, api_key, url_params,CACHE_DICT):
    '''When we scrap data from yelp api:
    (1) if we scrapped it before, the func just return the result from cache file
    (2) if not: the func will ask for data from the certain yelp api

    Parameters
    ----------
    host: str
        the yelp api host:'https://api.yelp.com'

    path: str
        on which path we want to search: '/v3/businesses/search'
    
    api_key: str
        the authentic api key got from yelp api
    
    url_params: dict
        the search condition for the restaurant
    
    CACHE_DICT: dict
        where we stored the previous results


    Returns
    -------
    CACHE_DICT[request_key]: str
        the detail information about the restaurant got from yelp api

    '''
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
    #in this for loop, it works to get enough records to meet the requirements
    for city in city_list[:30]:
        params = {'location':city,'limit':10,'term':'dinner'}
        results = request_with_cache(host, base_url, key, params,CACHE_DICT)
    #the yelp_list code is just to test whether Yelp() class works well.
    # yelp_list = [Yelp(restaurant) for restaurant in results['businesses']]


if __name__ == '__main__':
    main()
