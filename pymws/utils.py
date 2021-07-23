import base64
from collections import namedtuple
import hashlib

from io import BytesIO
from builtins import str
import six

from .exceptions import MWSException

if six.PY2:
    import unicodecsv as csv
else:
    import csv


Marketplace = namedtuple(
    'Marketplace', ['code', 'currency', 'id', 'endpoint', 'name']
)

#: A list of `Marketplaces
#: <http://docs.developer.amazonservices.com/en_US/dev_guide/DG_Endpoints.html>`_
MARKETPLACES = [

    # North america region
    Marketplace(
        'BR', 'BRL', 'A2Q3Y263D00KWC',
        'https://mws.amazonservices.com', 'Amazon.com.br'),
    Marketplace(
        'CA', 'CAD', 'A2EUQ1WTGCTBG2',
        'https://mws.amazonservices.ca', 'Amazon.ca'),
    Marketplace(
        'MX', 'MXN', 'A1AM78C64UM0Y8',
        'https://mws.amazonservices.com.mx', 'Amazon.com.mx'),
    Marketplace(
        'US', 'USD', 'ATVPDKIKX0DER',
        'https://mws.amazonservices.com', 'Amazon.com'),

    # Europe region
    Marketplace(
        'AE', 'AED', 'A2VIGQ35RCS4UG',
        'https://mws.amazonservices.ae', 'United Arab Emirates (U.A.E.)'),
    Marketplace(
        'DE', 'EUR', 'A1PA6795UKMFR9',
        'https://mws-eu.amazonservices.com', 'Amazon.de'),
    Marketplace(
        'EG', 'EGP', 'ARBP9OOSHTCHU',
        'https://mws-eu.amazonservices.com', 'Egypt'),
    Marketplace(
        'ES', 'EUR', 'A1RKKUPIHCS9HS',
        'https://mws-eu.amazonservices.com', 'Amazon.es'),
    Marketplace(
        'FR', 'EUR', 'A13V1IB3VIYZZH',
        'https://mws-eu.amazonservices.com', 'Amazon.fr'),
    Marketplace(
        'GB', 'GBP', 'A1F83G8C2ARO7P',
        'https://mws-eu.amazonservices.com', 'Amazon.co.uk'),
    Marketplace(
        'IN', 'INR', 'A21TJRUUN4KGV',
        'https://mws.amazonservices.in', 'Amazon.in'),
    Marketplace(
        'IT', 'EUR', 'APJ6JRA9NG5V4',
        'https://mws-eu.amazonservices.com', 'Amazon.it'),
    Marketplace(
        'NL', 'EUR', 'A1805IZSGTT6HS',
        'https://mws-eu.amazonservices.com', 'Amazon.nl'),
    Marketplace(
        'SA', 'SAR', 'A17E79C6D8DWNP',
        'https://mws-eu.amazonservices.com', 'Saudi Arabia'),
    Marketplace(
        'TR', 'EUR', 'A33AVAJ2PDY3EV',
        'https://mws-eu.amazonservices.com', 'Turkey'),

    # Far East region
    Marketplace(
        'SG', 'SGD', 'A19VAU5U5O7RUS',
        'https://mws-fe.amazonservices.com', 'Amazon.sg'),
    Marketplace(
        'AU', 'AUD', 'A39IBJ37TRP1C6',
        'https://mws.amazonservices.com.au', 'Amazon.com.au'),
    Marketplace(
        'JP', 'JPY', 'A1VC38T7YXB528',
        'https://mws.amazonservices.jp', 'Amazon.jp'),

]


def get_marketplace(id_or_code):
    """
    Given a code, get the marketplace
    """
    id_or_code = id_or_code.upper()

    for marketplace in MARKETPLACES:
        if marketplace.code == id_or_code or \
                marketplace.id == id_or_code:
            return marketplace

    raise MWSException(
        '{} is not a valid marketplace id or code'.format(id_or_code)
    )


def flatten_list(kwargs, key, separator):
    """
    Convert a list into URL parameters the way amazon like it.

    Example::

        flatten_list(
            {'ReportTypeList': ['_A_', '_B_']},
            'ReportTypeList',
            'Type'
        )

    Becomes::

        ReportTypeList.Type.1=_A_&ReportTypeList.Type.2=_B_
    """
    vals = kwargs.pop(key, [])
    for index, value in enumerate(vals, 1):
        subkey = '{}.{}.{}'.format(key, separator, index)
        kwargs[subkey] = value
        if isinstance(value, dict):
            flatten_dict(kwargs, subkey)


def flatten_dict(kwargs, key):
    """
    Convert a dict into URL parameters the way amazon like it.

    Example::

        flatten_dict(
            {'DestinationAddress': {'Name': 'John', 'Country': 'US'}},
            'DestinationAddress',
        )

    Becomes::

        DestinationAddress.Name=John&DestinationAddress.Country=US
    """
    vals = kwargs.pop(key, {})
    for subkey, value in vals.items():
        kwargs['{}.{}'.format(key, subkey)] = value


def parse_xsv(text):
    """
    Python 2 and 3 compatible (X)SV - CSV/TSV parser that returns a list of
    dictionary objects.
    """
    header = BytesIO(text.encode("utf-8")).readline().decode("utf-8")
    dialect = csv.Sniffer().sniff(header)
    if six.PY2:
        text = BytesIO(text.encode('utf-8'))
    else:
        text = text.split("\n")

    return list(
        csv.DictReader(
            text,
            delimiter=(
                dialect.delimiter.encode() if six.PY2 else dialect.delimiter
            )
        )
    )


def get_md5_hash(string):
    hasher = hashlib.md5()
    if isinstance(string, str):
        hasher.update(string.encode('utf-8'))
    else:
        hasher.update(string)
    return base64.b64encode(
        hasher.digest()
    ).decode('utf-8')
