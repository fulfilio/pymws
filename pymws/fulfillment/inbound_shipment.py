from ..utils import flatten_list


class InboundShipment(object):
    "Implements inbound shipment client for Amazon MWS"
    VERSION = "2010-10-01"
    URI = "/FulfillmentInboundShipment/" + VERSION

    def __init__(self, client):
        self.client = client

    def list_inbound_shipments(self, **kwargs):
        """
        Learn more: https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_ListInboundShipments.html  # noqa
        """
        flatten_list(kwargs, "ShipmentStatusList", "member")
        flatten_list(kwargs, "ShipmentIdList", "member")
        return self.client.get(
            "ListInboundShipments", self.URI, kwargs, self.VERSION
        )

    def list_inbound_shipments_by_next_token(self, NextToken):
        """
        Returns the next page of inbound shipments using the NextToken parameter.

        `Learn more https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_ListInboundShipmentsByNextToken.html`__

        The `NextToken` argument is not very pythonic, but keeps the
        package user side code consistent with Amazon's documentation
        and avoids a surprise for the user.
        """     # noqa: E501
        return self.client.get(
            "ListInboundShipmentsByNextToken", self.URI,
            {"NextToken": NextToken}, self.VERSION
        )

    def list_inbound_shipment_items(self, ShipmentId):
        """
        Returns shipment items based on the ShipmentId that you specify.

        `Learn more <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_ListInboundShipmentItems.html`__
        """     # noqa: E501
        return self.client.get(
            "ListInboundShipmentItems", self.URI,
            {"ShipmentId": ShipmentId}, self.VERSION
        )

    def list_inbound_shipment_items_by_next_token(self, NextToken):
        """
        Returns the next page of inbound shipment items using the NextToken parameter.

        `Learn more <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_ListInboundShipmentItemsByNextToken.html`__

        The `NextToken` argument is not very pythonic, but keeps the
        package user side code consistent with Amazon's documentation
        and avoids a surprise for the user.
        """     # noqa: E501
        return self.client.get(
            "ListInboundShipmentItemsByNextToken", self.URI,
            {"NextToken": NextToken}, self.VERSION
        )
