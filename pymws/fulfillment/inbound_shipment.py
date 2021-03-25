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

    def list_all_inbound_shipments(self, **kwargs):
        "Gets all the inboud shipments using next token"
        if "NextToken" in kwargs:
            response = self.list_inbound_shipments_by_next_token(
                kwargs["NextToken"]
            )
        else:
            response = self.list_inbound_shipments(**kwargs)

        if not hasattr(response.ShipmentData, "member"):
            # No shipments
            return []

        shipments = list(response.ShipmentData.member)

        next_token = getattr(response, "NextToken")
        if next_token:
            shipments.extend(
                self.list_all_inbound_shipments(NextToken=str(next_token))
            )
        return shipments

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

    def list_all_inbound_shipment_items(self, ShipmentId, NextToken=None):
        "Gets all the inboud shipment items using next token"
        if NextToken:
            response = self.list_inbound_shipment_items_by_next_token(
                NextToken
            )
        else:
            response = self.list_inbound_shipment_items(ShipmentId)

        if not hasattr(response.ItemData, "member"):
            # No items
            return []

        items = list(response.ItemData.member)

        next_token = getattr(response, "NextToken")
        if next_token:
            items.extend(
                self.list_all_inbound_shipment_items(
                    ShipmentId, NextToken=str(next_token)
                )
            )
        return items

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
