from ..utils import flatten_list, flatten_dict


class OutboundShipment(object):
    """
    Implements outbound shipment client for Amazon MWS

    .. code-block:: python

        client.fulfillment_outbound_shipment.create_fulfillment_order(
            MarketplaceId='A2Q3Y263D00KWC',
            SellerFulfillmentOrderId='SO3421',
            FulfillmentAction='Ship',
            DisplayableOrderId='SO3421',
            DisplayableOrderDateTime=datetime.utcnow(),
            DisplayableOrderComment='Some comment',
            ShippingSpeedCategory='Standard',
            DestinationAddress={
                'Name': 'John Doe',
                'Line1': 'Random street',
                'StateOrProvinceCode': 'CA',
                'CountryCode': 'US',
            },
            Items=[{
                'SellerSKU': 'SKU-1',
                'SellerFulfillmentOrderItemId': 'SO3421-1',
                'Quantity': 1,
            }],
        )

    for other attributes refer to the Amazon MWS documentation.
    """
    VERSION = "2010-10-01"
    URI = "/FulfillmentOutboundShipment/" + VERSION

    def __init__(self, client):
        self.client = client

    def create_fulfillment_order(self, **kwargs):
        """
        Requests that Amazon ship items from the seller's inventory in Amazon's
        fulfillment network to a destination address.

        `Learn more <http://docs.developer.amazonservices.com/en_US/fba_outbound/FBAOutbound_CreateFulfillmentOrder.html>`__
        """  # noqa: E501
        flatten_dict(kwargs, 'DestinationAddress')
        for item in kwargs.get('Items'):
            flatten_dict(item, 'PerUnitDeclaredValue')
        flatten_list(kwargs, 'Items', 'member')
        flatten_list(kwargs, 'NotificationEmailList', 'member')
        return self.client.post(
            'CreateFulfillmentOrder', self.URI, kwargs, self.VERSION
        )

    def get_fulfillment_order(self, SellerFulfillmentOrderId):
        """
        Returns a fulfillment order based on a specified SellerFulfillmentOrderId.

        `Learn more <Learn more: http://docs.developer.amazonservices.com/en_US/fba_outbound/FBAOutbound_GetFulfillmentOrder.html>`__
        """  # noqa: E501
        return self.client.get(
            'GetFulfillmentOrder', self.URI,
            {'SellerFulfillmentOrderId': SellerFulfillmentOrderId},
            self.VERSION
        )
