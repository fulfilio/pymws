"""Main module."""
from __future__ import unicode_literals

import base64
import hashlib
import hmac
from builtins import str as text
from datetime import date, datetime

import requests
from lxml import objectify

from .exceptions import MWSError, AccessDenied
from .orders import Orders
from .products import Products
from .reports import Reports
from .utils import get_marketplace, parse_tsv

try:
    from urllib.parse import urlparse, quote
except ImportError:
    # py2
    from urlparse import urlparse
    from urllib import quote


MWS_SAFE = '-_.~'.encode('utf-8')


class MWS(object):
    """
    Primary client class that acts as a gateway to all of the
    functionality offered by this package

    :param marketplace: marketplace to connect to
    """

    def __init__(
                self,
                marketplace, merchant_id=None,
                access_key_id=None, secret_key=None,
                auth_token=None):
        self.marketplace = get_marketplace(marketplace)
        self.merchant_id = merchant_id
        self.access_key_id = access_key_id
        self.secret_key = secret_key
        self.auth_token = auth_token
        self.session = requests.Session()
        self.user_agent = 'pymws/0.1 (Language=Python)'

    @property
    def products(self):
        return Products(self)

    @property
    def orders(self):
        return Orders(self)

    @property
    def reports(self):
        return Reports(self)

    def get(self, action, uri, req_params, version):
        return self._request(
            'GET',
            action, uri, req_params, version
        )

    def post(self, action, uri, req_params, version):
        return self._request(
            'POST',
            action, uri, req_params, version
        )

    def _request(self, http_verb, action, uri, req_params, version):
        """
        Build a request, parse the response and handle errors
        """
        query_string = self.get_query_string(action, req_params, version)
        signature = self.get_signature(http_verb, uri, query_string)
        url = "{endpoint}{uri}".format(
            endpoint=self.marketplace.endpoint,
            uri=uri,
        )
        response = self.session.request(
            http_verb,
            url,
            params="{query_string}&Signature={signature}".format(
                query_string=query_string,
                signature=quote(signature)
            ),
            headers={'User-Agent': self.user_agent}
        )

        if response.status_code == 401:
            raise AccessDenied(response.text)
        elif response.status_code != 200:
            raise MWSError(response.text)

        if response.headers['content-type'].startswith('text/xml'):
            xml = objectify.fromstring(response.content)
            result_el = '{}Result'.format(action)
            if hasattr(xml, result_el):
                return getattr(xml, result_el)
            return xml
        elif response.headers['content-type'].startswith('text/plain'):
            return parse_tsv(response.content.decode(encoding="iso-8859-1"))
        else:
            return response.text

    def get_query_string(self, action, req_params, version):
        params = {
            'AWSAccessKeyId': self.access_key_id,
            'Action': action,
            'MWSAuthToken': self.auth_token,
            'SellerId': self.merchant_id,
            'SignatureMethod': 'HmacSHA256',
            'SignatureVersion': '2',
            'Timestamp': datetime.utcnow().isoformat(),
            'Version': version,
        }
        params.update(req_params)
        query_string = self.build_query_string(params)
        return query_string

    def get_signature(self, http_verb, uri, query_string):
        to_sign = [
            http_verb,
            urlparse(self.marketplace.endpoint).netloc,
            uri,
            query_string
        ]
        return base64.b64encode(
            hmac.new(
                self.secret_key.encode('utf-8'),
                '\n'.join(to_sign).encode('utf-8'),
                hashlib.sha256,
            ).digest()
        ).decode('utf-8')

    def build_query_string(self, params):
        """
        create the query string to be signed

        * Sort the UTF-8 query string components by parameter name
        * URL encode the parameter name and values

        Because of the following issues, this method cannot directly
        call urlencode because urlencode does not support quoting the
        way amazon wants, it always does quote_plus.
        """
        query = []
        for key in sorted(params.keys()):
            value = params[key]

            if isinstance(value, (date, datetime)):
                value = value.isoformat()

            if not isinstance(value, text):
                value = str(value)

            query.append(
                '{}={}'.format(
                    quote(key, safe=MWS_SAFE),
                    quote(value.encode('utf-8'), safe=MWS_SAFE)
                )
            )
        return '&'.join(query)
