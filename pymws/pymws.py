"""Main module."""
from __future__ import unicode_literals

import base64
import hashlib
import hmac
from builtins import str as text
from datetime import date, datetime

import requests
from lxml import objectify

from .exceptions import MWSError, AccessDenied, QuotaExceeded, RequestThrottled
from .feeds import Feeds
from .orders import Orders
from .products import Products
from .reports import Reports
from .fulfillment.outbound_shipment import OutboundShipment
from .fulfillment.inbound_shipment import InboundShipment
from .utils import get_marketplace, parse_xsv, get_md5_hash

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
    functionality offered by this package.

    Example usage::

        client = MWS(
            marketplace="US", merchant_id="1234",
            access_key_id="key", secret_key="secret",
            auth_token="token"
        )
        client.reports.get_reports_list()

    :param marketplace: marketplace to connect to.
    :param merchant_id: Amazon merchant it.
    :param access_key_id: Access key of your app
    :param secret_key: Secret key of your app
    :param auth_token: Token obtained by the merchant after
                       installing your app.
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
        """
        Fetch the products API client.
        Returns an instance of :class:`pymws.products.Products`
        """
        return Products(self)

    @property
    def orders(self):
        """
        Fetch the order API client
        Returns an instance of :class:`pymws.orders.Orders`
        """
        return Orders(self)

    @property
    def reports(self):
        """
        Fetch the reports API client
        Returns an instance of :class:`pymws.reports.Reports`
        """
        return Reports(self)

    @property
    def feeds(self):
        """
        Fetch the feeds API client
        Returns an instance of :class:`pymws.feeds.Feeds`
        """
        return Feeds(self)

    @property
    def fulfillment_outbound_shipment(self):
        """
        Fetch the Fulfillment outbound shipment API client
        Returns an instance of
        :class:`pymws.fulfillment.outbound_shipment.OutboundShipment`
        """
        return OutboundShipment(self)

    @property
    def fulfillment_inbound_shipment(self):
        """
        Fetch the Fulfillment inbound shipment API client
        Returns an instance of
        :class:`pymws.fulfillment.inbound_shipment.InboundShipment`
        """
        return InboundShipment(self)

    def get(self, action, uri, req_params, version):
        return self._request(
            'GET',
            action, uri, req_params, version
        )

    def post(self, action, uri, req_params, version,
             body=None, content_type=None):
        return self._request(
            'POST',
            action, uri, req_params, version, body, content_type
        )

    def _request(self, http_verb, action, uri, req_params, version,
                 body=None, content_type=None):
        """
        Build a request, parse the response and handle errors
        """
        if body is not None:
            req_params['ContentMD5Value'] = get_md5_hash(body)

        query_string = self.get_query_string(action, req_params, version)
        signature = self.get_signature(http_verb, uri, query_string)
        url = "{endpoint}{uri}".format(
            endpoint=self.marketplace.endpoint,
            uri=uri,
        )
        headers = {
            'User-Agent': self.user_agent,
        }

        if content_type:
            headers['Content-Type'] = content_type

        response = self.session.request(
            http_verb,
            url,
            data=body,
            params="{query_string}&Signature={signature}".format(
                query_string=query_string,
                signature=quote(signature)
            ),
            headers=headers
        )

        if response.status_code == 401:
            raise AccessDenied(response.text)
        elif response.status_code == 503:
            error_code = objectify.fromstring(response.text).Error.Code
            if error_code == 'RequestThrottled':
                raise RequestThrottled(response.text)
            elif error_code == 'QuotaExceeded':
                raise QuotaExceeded(response.text)
        elif response.status_code != 200:
            raise MWSError(response.text)

        if response.headers['content-type'].startswith('text/xml'):
            xml = objectify.fromstring(response.content)
            result_el = '{}Result'.format(action)
            if hasattr(xml, result_el):
                return getattr(xml, result_el)
            return xml
        elif response.headers['content-type'].startswith('text/plain'):
            return parse_xsv(response.content.decode(encoding="iso-8859-1"))
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
