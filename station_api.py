import requests
import json

# GET REQUEST
def get_api_request(get_url, get_data):
    url = get_url
    headers = {'Content-Type': 'application/json'}
    data = get_data
    response = requests.get(url, data=json.dumps(data), headers=headers)
    return response.json()

# GET REQUEST (데이터 필드 없음)
def get_api_request2(get_url):
    url = get_url
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    return response.json()

# PUT REQUEST
def put_api_request(put_url, put_data):
    url = put_url
    headers = {'Content-Type': 'application/json'}
    data = put_data
    response = requests.put(url, data=json.dumps(data), headers=headers)
    return response.json()

# POST REQUEST
def post_api_request(post_url, post_data):
    url = post_url
    headers = {'Content-Type': 'application/json'}
    data = post_data
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response.json()

if __name__ == '__main__':

    get_url = "http://192.168.137.10:9200/stations/_search"
    get_data = {
        "query": {
            "match": {
                "station.nori_discard": "입구"
            }
        }
    }
    print(get_api_request(get_url, get_data))

    put_url = "http://192.168.137.10:9200/stations/"
    put_data = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "nori_discard": {
                        "tokenizer": "nori_t_discard",
                        "filter": "shingle"
                    }
                },
            "tokenizer": {
                "nori_t_discard": {
                    "type": "nori_tokenizer",
                    "decompound_mode": "discard"
                }
            },
            "filter": {
                "shingle": {
                    "type": "shingle",
                    "token_separator": "",
                    "max_shingle_size": 3
                }
            }
        }
    },
        "mappings": {
            "properties": {
                "station": {
                    "type": "text",
                    "fields": {
                        "nori_discard": {
                            "type": "text",
                            "analyzer": "nori_discard",
                            "search_analyzer": "standard"
                        }
                    }
                }
            }
        }
    }
    # print(put_api_request(put_url, put_data))
