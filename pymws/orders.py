from .utils import flatten_list


class Orders(object):
    """
    Implements an order API client for Amazon MWS

    .. code-block:: python

        response = client.orders.list_orders(CreatedAfter=start_date)
        for order in response.Orders.getchildren():
            print(order.AmazonOrderId)

    for other attributes of the order, refer to the Amazon MWS documentation.

    To fetch the next page of orders:

    .. code-block:: python

        response = client.orders.list_orders(CreatedAfter=start_date)
        page2 = client.orders.list_orders_by_next_token(
            response.NextToken
        )
    """
    VERSION = '2013-09-01'
    URI = '/Orders/' + VERSION

    def __init__(self, client):
        self.client = client

    def list_orders(self, **kwargs):
        """
        Returns orders created or updated during a time frame that you specify.

        `Learn more <http://docs.developer.amazonservices.com/en_US/orders-2013-09-01/Orders_ListOrders.html>`__
        """     # noqa: E501
        if 'MarketplaceId.Id.1' not in kwargs:
            # Not a single marketplace id is specified.
            # fallback to the default marketplace
            kwargs['MarketplaceId.Id.1'] = self.client.marketplace.id

        flatten_list(kwargs, 'FulfillmentChannel', 'Channel')
        return self.client.get(
            'ListOrders', self.URI, kwargs, self.VERSION
        )

    def list_orders_by_next_token(self, NextToken):
        """
        Returns the next page of orders using the NextToken parameter.

        `Learn more <http://docs.developer.amazonservices.com/en_US/orders-2013-09-01/Orders_ListOrdersByNextToken.html>`__

        The `NextToken` argument is not very pythonic, but keeps the
        package user side code consistent with Amazon's documentation
        and avoids a surprise for the user.
        """     # noqa: E501
        return self.client.get(
            'ListOrdersByNextToken', self.URI,
            {'NextToken': NextToken}, self.VERSION
        )

    def get_order(self, AmazonOrderId):
        """
        Returns orders based on the AmazonOrderId values that you specify.

        `Learn more <http://docs.developer.amazonservices.com/en_US/orders-2013-09-01/Orders_GetOrder.html>`__
        """     # noqa: E501
        return self.client.get(
            'GetOrder', self.URI,
            {'AmazonOrderId.Id.1': AmazonOrderId}, self.VERSION
        )

    def list_order_items(self, AmazonOrderId):
        """
        Returns order items based on the AmazonOrderId that you specify.

        `Learn more <http://docs.developer.amazonservices.com/en_US/orders-2013-09-01/Orders_ListOrderItems.html>`__
        """     # noqa: E501
        return self.client.get(
            'ListOrderItems', self.URI,
            {'AmazonOrderId': AmazonOrderId}, self.VERSION
        )

    def list_order_items_by_next_token(self, NextToken):
        """
        Returns the next page of order items using the NextToken parameter.

        `Learn more <http://docs.developer.amazonservices.com/en_US/orders-2013-09-01/Orders_ListOrderItemsByNextToken.html>`__
        """     # noqa: E501
        return self.client.get(
            'ListOrderItemsByNextToken', self.URI,
            {'NextToken': NextToken}, self.VERSION
        )

    def get_service_status(self):
        """
        Returns the operational status of the Orders API section.

        `Learn more <http://docs.developer.amazonservices.com/en_US/orders-2013-09-01/MWS_GetServiceStatus.html>`__
        """     # noqa: E501
        return self.client.get(
            'GetServiceStatus', self.URI,
            {}, self.VERSION
        )
