import requests
import time
import json


class TinSoft:

    def __init__(self, api_key):
        self.api_key = api_key
        self.location = 0
        self.check_proxy_url = "http://proxy.tinsoftsv.com/api/getProxy.php?key=" + api_key
        self.check_api_url = "http://proxy.tinsoftsv.com/api/getKeyInfo.php?key=" + api_key
        self.get_new_proxy_url = f"http://proxy.tinsoftsv.com/api/changeProxy.php?key={api_key}&location={self.location}"

    def CheckProxy(self):
        rq = requests.get(self.check_proxy_url)
        data = rq.json()

        return data

    def CheckApiKey(self):
        rq = requests.get(self.check_api_url)
        data = rq.json()

        return data

    def GetNewProxy(self):
        rq = requests.get(self.get_new_proxy_url)
        data = rq.json()

        return data
