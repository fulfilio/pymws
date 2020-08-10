from collections import namedtuple
from .exceptions import MWSException

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