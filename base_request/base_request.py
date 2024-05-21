import hmac
import time
from hashlib import sha256

import requests

from exeptions import BingxExceptionErrors


class BaseRequest(object):
    def __init__(self, key='', secret='', url='https://open-api.bingx.com'):
        """
        https://bingx-api.github.io/docs
        :param key: bingx-api key for Bingx API (mandatory)
        :param secret: bingx-api secret for Bingx API (mandatory)
        :param url: bingx-api url for Bingx API
        """
        self.key = key
        self.secret = secret
        self.url = url

    def _request(self, method: str, path: str, query_params: dict) -> dict:
        parse_query_params = self.parse_query_params(query_params)
        bingx_sign = self.get_sign(self.secret, parse_query_params)
        url = f'{self.url}{path}?{parse_query_params}&signature={bingx_sign}'
        headers = {'X-BX-APIKEY': self.key}
        response = requests.request(method, url, headers=headers, data={})
        if response.json().get('code') != 0:
            raise BingxExceptionErrors(response.json())
        return response.json()

    @staticmethod
    def parse_query_params(params_map: dict) -> str:
        sorted_keys = sorted(params_map)
        params_str = '&'.join(['%s=%s' % (x, params_map[x]) for x in sorted_keys])
        return params_str + '&timestamp=' + str(int(time.time() * 1000))

    @staticmethod
    def get_sign(api_secret: str, payload) -> str:
        return hmac.new(api_secret.encode('utf-8'), payload.encode('utf-8'), digestmod=sha256).hexdigest()
