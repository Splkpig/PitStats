import requests
import json


def getKey():
    API_FILE = open("../PitStats/tokens_and_keys/API_KEY.json", "r")
    API_KEY = json.loads(API_FILE.read())["API_KEY"]
    return API_KEY


def getInfo(call):
    r = requests.get(call)
    return r.json()
