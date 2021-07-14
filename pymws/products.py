from .utils import flatten_list


class Products(object):

    VERSION = '2011-10-01'
    URI = '/Products/' + VERSION

    def __init__(self, client):
        self.client = client

    def list_matching_products(self, query, query_context_id):
        """
        Returns a list of products and their attributes, based on a
        search query.

        Learn more: http://docs.developer.amazonservices.com/en_US/products/Products_ListMatchingProducts.html
        """  # noqa: E501
        pass

    def get_matching_product_for_id(self, **kwargs):
        """Returns a list of products and their attributes, based on a list of
        ASIN, GCID, SellerSKU, UPC, EAN, ISBN, and JAN values.

        `Learn more <https://docs.developer.amazonservices.com/en_US/products/Products_GetMatchingProductForId.html>`_
        """  # noqa: E501
        if 'MarketplaceId' not in kwargs:
            # marketplace id is not specified.
            # fallback to the default marketplace
            kwargs['MarketplaceId'] = self.client.marketplace.id

        flatten_list(kwargs, 'IdList', 'Id')
        return self.client.get(
            'GetMatchingProductForId', self.URI, kwargs, self.VERSION
        )
