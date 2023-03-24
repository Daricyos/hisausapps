import requests


class HisaAPI:
    def __init__(self, key=''):
        self.key = key
        self.link = 'https://dbapi.dev.hisausapps.org/'

    def request(self, method, url, params=None):
        headers = {'X-API-KEY': self.key, 'accept': 'text/json'}
        response = requests.request(
            method=method, url=url, params=params, headers=headers)
        print(response.status_code)
        if 200 <= response.status_code < 300:
            res = response.json()

            return res
        return False

    def get_ruling_all(self, params=None, ):
        if params:
            url = f"{self.link}ruling/all"
            res = self.request(method='GET', url=url, params=params, )
            return res
        return False
