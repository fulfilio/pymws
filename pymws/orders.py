class Orders(object):
    VERSION = '2013-09-01'
    URI = '/Orders/' + VERSION

    def __init__(self, client):
        self.client = client

    def list_orders(self, **kwargs):
        """
        Returns orders created or updated during a time frame that you specify.

        Learn more: http://docs.developer.amazonservices.com/en_US/orders-2013-09-01/Orders_ListOrders.html
        """     # noqa: E501
        if 'MarketplaceId.Id.1' not in kwargs:
            # Not a single marketplace id is specified.
            # fallback to the default marketplace
            kwargs['MarketplaceId.Id.1'] = self.client.marketplace.id

        return self.client.get(
            'ListOrders', self.URI, kwargs, self.VERSION
        )
