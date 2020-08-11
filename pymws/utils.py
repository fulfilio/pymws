from collections import namedtuple

import six

from .exceptions import MWSException

if six.PY2:
    import unicodecsv as csv
    from io import BytesIO
else:
    import csv


Marketplace = namedtuple('Marketplace', ['code', 'id', 'endpoint'])

# Updated from
# http://docs.developer.amazonservices.com/en_US/dev_guide/DG_Endpoints.html
MARKETPLACES = [

    # North america region
    Marketplace('BR', 'A2Q3Y263D00KWC', 'https://mws.amazonservices.com'),
    Marketplace('CA', 'A2EUQ1WTGCTBG2', 'https://mws.amazonservices.ca'),
    Marketplace('MX', 'A1AM78C64UM0Y8', 'https://mws.amazonservices.com.mx'),
    Marketplace('US', 'ATVPDKIKX0DER', 'https://mws.amazonservices.com'),

    # Europe region
    # TODO: Add these

    # Far East region
    # TODO: Add these
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
