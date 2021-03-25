# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def test_list_inbound_shipments(mws_client, mock_adapter, example_response):
    mock_adapter.register_uri(
        "GET",
        "/FulfillmentInboundShipment/2010-10-01?Action=ListInboundShipments",
        status_code=200,
        text=example_response("inbound_shipment/list_shipments.xml"),
        headers={"Content-Type": "text/xml"}
    )
    response = mws_client.fulfillment_inbound_shipment.list_inbound_shipments(
        ShipmentStatusList=["WORKING"]
    )
    assert len(response.ShipmentData.member) == 2


def test_list_inbound_shipment_items(
    mws_client, mock_adapter, example_response
):
    mock_adapter.register_uri(
        "GET",
        "/FulfillmentInboundShipment/2010-10-01?Action=ListInboundShipmentItems",  # noqa
        status_code=200,
        text=example_response("inbound_shipment/list_shipment_items.xml"),
        headers={"Content-Type": "text/xml"}
    )
    res = mws_client.fulfillment_inbound_shipment.list_inbound_shipment_items(
        ShipmentId="FBA161HWJF4X"
    )
    assert len(res.ItemData.member) == 2


def test_list_all_inbound_shipments(
    mws_client, mock_adapter, example_response
):
    mock_adapter.register_uri(
        "GET",
        "/FulfillmentInboundShipment/2010-10-01?Action=ListInboundShipments",
        status_code=200,
        text=example_response("inbound_shipment/list_shipments.xml"),
        headers={"Content-Type": "text/xml"}
    )
    mock_adapter.register_uri(
        "GET",
        "/FulfillmentInboundShipment/2010-10-01?Action=ListInboundShipmentsByNextToken",  # noqa
        status_code=200,
        text=example_response(
            "inbound_shipment/list_shipments_by_next_token.xml"
        ),
        headers={"Content-Type": "text/xml"}
    )
    inbound_shipment_api = mws_client.fulfillment_inbound_shipment
    shipments = inbound_shipment_api.list_all_inbound_shipments(
        ShipmentStatusList=["WORKING"]
    )
    assert len(shipments) == 2


def test_list_all_inbound_shipment_items(
    mws_client, mock_adapter, example_response
):
    mock_adapter.register_uri(
        "GET",
        "/FulfillmentInboundShipment/2010-10-01?Action=ListInboundShipmentItems",  # noqa
        status_code=200,
        text=example_response("inbound_shipment/list_shipment_items.xml"),
        headers={"Content-Type": "text/xml"}
    )
    mock_adapter.register_uri(
        "GET",
        "/FulfillmentInboundShipment/2010-10-01?Action=ListInboundShipmentItemsByNextToken",  # noqa
        status_code=200,
        text=example_response(
            "inbound_shipment/list_shipment_items_by_next_token.xml"
        ),
        headers={"Content-Type": "text/xml"}
    )
    inbound_shipment_api = mws_client.fulfillment_inbound_shipment
    items = inbound_shipment_api.list_all_inbound_shipment_items(
        ShipmentId="FBA161HWJF4X"
    )
    assert len(items) == 2
