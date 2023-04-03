import requests


class HisaAPI:
    def __init__(self, key=''):
        self.key = key
        self.link = 'https://dbapi.dev.hisausapps.org/'

    def request(self, method, url, params=None, is_files=False, ):
        headers = {'X-API-KEY': self.key, 'accept': 'text/json'}
        print(url)
        response = requests.request(
            method=method, url=url, params=params, headers=headers)
        if 200 <= response.status_code < 300:
            res = response.json()
            if is_files:
                return response
            return res
        return False

    def get_ruling_all(self, params=None, ):
        if params:
            url = f"{self.link}ruling/all"
            res = self.request(method='GET', url=url, params=params, )
            return res
        return False

    def get_file_from_ruling(self, file_url='', ):
        if file_url:
            url = f'{self.link}{file_url}'
            response = self.request(method='GET', url=url, params=None, is_files=True, )
            return response
        return False

