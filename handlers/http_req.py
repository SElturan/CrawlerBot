import requests

from config import http_api

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

def get_channels_req():
    req = requests.get(f"{http_api}/channels/", headers=HEADERS)
    data = req.json()
    result = []
    channels = [response['channel_id'] for response in data]
    result.append(channels)
    # print(result)
    return result

def get_required_word():
    req = requests.get(f"{http_api}/keyword/", headers=HEADERS)
    data = req.json()
    keyword = [response['keyword'] for response in data]
    # print(keyword)
    return keyword

def get_stop_word():
    req = requests.get(f"{http_api}/spamwords/", headers=HEADERS)
    data = req.json()
    keyword = [response['word'] for response in data]
    return keyword


