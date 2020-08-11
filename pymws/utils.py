from collections import namedtuple

import six

from .exceptions import MWSException

if six.PY2:
    import unicodecsv as csv
    from io import BytesIO
else:
    import csv


Marketplace = namedtuple('Marketplace', ['code', 'id', 'endpoint', 'name'])

# Updated from
# http://docs.developer.amazonservices.com/en_US/dev_guide/DG_Endpoints.html
MARKETPLACES = [

    # North america region
    Marketplace('BR', 'A2Q3Y263D00KWC', 'https://mws.amazonservices.com', 'Brazil'),
    Marketplace('CA', 'A2EUQ1WTGCTBG2', 'https://mws.amazonservices.ca', 'Canada'),
    Marketplace('MX', 'A1AM78C64UM0Y8', 'https://mws.amazonservices.com.mx', 'Mexico'),
    Marketplace('US', 'ATVPDKIKX0DER', 'https://mws.amazonservices.com', 'US'),

    # Europe region
    Marketplace('AE', 'A2VIGQ35RCS4UG', 'https://mws.amazonservices.ae', 'United Arab Emirates (U.A.E.)'),
    Marketplace('DE', 'A1PA6795UKMFR9', 'https://mws-eu.amazonservices.com', 'Germany'),
    Marketplace('EG', 'ARBP9OOSHTCHU', 'https://mws-eu.amazonservices.com', 'Egypt'),
    Marketplace('ES', 'A1RKKUPIHCS9HS', 'https://mws-eu.amazonservices.com', 'Spain'),
    Marketplace('FR', 'A13V1IB3VIYZZH', 'https://mws-eu.amazonservices.com', 'France'),
    Marketplace('GB', 'A1F83G8C2ARO7P', 'https://mws-eu.amazonservices.com', 'UK'),
    Marketplace('IN', 'A21TJRUUN4KGV', 'https://mws.amazonservices.in', 'India'),
    Marketplace('IT', 'APJ6JRA9NG5V4', 'https://mws-eu.amazonservices.com', 'Italy'),
    Marketplace('NL', 'A1805IZSGTT6HS', 'https://mws-eu.amazonservices.com', 'Netherlands'),
    Marketplace('SA', 'A17E79C6D8DWNP', 'https://mws-eu.amazonservices.com', 'Saudi Arabia'),
    Marketplace('TR', 'A33AVAJ2PDY3EV', 'https://mws-eu.amazonservices.com', 'Turkey'),

    # Far East region
    Marketplace('SG', 'A19VAU5U5O7RUS', 'https://mws-fe.amazonservices.com', 'Singapore'),
    Marketplace('AU', 'A39IBJ37TRP1C6', 'https://mws.amazonservices.com.au', 'Australia'),
    Marketplace('JP', 'A1VC38T7YXB528', 'https://mws.amazonservices.jp', 'Japan'),

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

    Example:

    flatten_list({'ReportTypeList': ['_A_', '_B_']}, 'ReportTypeList', 'Type')

    Becomes:

    ReportTypeList.Type.1=_A_&ReportTypeList.Type.2=_B_
    """
    vals = kwargs.pop(key, [])
    for index, value in enumerate(vals, 1):
        kwargs['{}.{}.{}'.format(key, separator, index)] = value


def parse_tsv(text):
    """
    Python 2 and 3 compatible TSV parser that returns a list of
    dictionary objects.
    """
    if six.PY2:
        text = BytesIO(text.encode('utf-8'))
    else:
        text = text.splitlines()
    return list(
        csv.DictReader(text, dialect='excel-tab')
    )
