# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime


def test_create_fulfillment_order(mws_client, mock_adapter, example_response):
    mock_adapter.register_uri(
        'POST', (
            mws_client.marketplace.endpoint +
            '/FulfillmentOutboundShipment/2010-10-01'
        ),
        status_code=200,
        text=example_response(
            'outbound_shipment/create_fulfillment_order.xml'
        ),
        headers={'Content-Type': 'text/xml'}
    )
    fulfillment_outbound_shipment = mws_client.fulfillment_outbound_shipment
    response = fulfillment_outbound_shipment.create_fulfillment_order(
        MarketplaceId='A2Q3Y263D00KWC',
        SellerFulfillmentOrderId='SO3421',
        FulfillmentAction='Ship',
        DisplayableOrderId='SO3421',
        DisplayableOrderDateTime=datetime.utcnow(),
        DisplayableOrderComment='Some comment',
        ShippingSpeedCategory='Standard',
        DestinationAddress={
            'Name': 'René Magritte',
            'Line1': 'Random street',
            'StateOrProvinceCode': 'CA',
            'CountryCode': 'US',
        },
        Items=[{
            'SellerSKU': 'SKU-1',
            'SellerFulfillmentOrderItemId': 'SO3421-1',
            'Quantity': 1,
        }, {
            'SellerSKU': 'SKU-2',
            'SellerFulfillmentOrderItemId': 'SO3421-2',
            'Quantity': 10.0,
            'PerUnitDeclaredValue': {
                'CurrencyCode': 'USD',
                'Value': "32",
            }
        }],
    )
    assert response.ResponseMetadata.RequestId
    url = mock_adapter.request_history[0].url
    assert 'DestinationAddress.Name=Ren%C3%A9%20Magritte' in url
    assert 'Items.member.1.SellerSKU=SKU-1' in url
    assert 'Items.member.1.Quantity=1' in url
    assert 'Items.member.2.SellerSKU=SKU-2' in url
    assert 'Items.member.2.Quantity=10.0' in url
    assert 'Items.member.2.PerUnitDeclaredValue.CurrencyCode=USD' in url
    assert 'Items.member.2.PerUnitDeclaredValue.Value=32' in url


def test_get_fulfillment_order(mws_client, mock_adapter, example_response):
    mock_adapter.register_uri(
        'GET', (
            mws_client.marketplace.endpoint +
            '/FulfillmentOutboundShipment/2010-10-01'
        ),
        status_code=200,
        text=example_response('outbound_shipment/get_fulfillment_order.xml'),
        headers={'Content-Type': 'text/xml'}
    )
    fulfillment_outbound_shipment = mws_client.fulfillment_outbound_shipment
    response = fulfillment_outbound_shipment.get_fulfillment_order(
        SellerFulfillmentOrderId='extern_id_1154539615776'
    )
    shipment_1, shipment_2 = response.FulfillmentShipment.member
    assert shipment_1.FulfillmentShipmentStatus == 'PENDING'
    assert len(shipment_1.FulfillmentShipmentItem.member) == 1
    assert shipment_1.FulfillmentShipmentItem.member[0].SellerSKU == 'SKU100'
    assert shipment_1.FulfillmentShipmentItem.member[0].Quantity == 2

    assert shipment_2.FulfillmentShipmentStatus == 'SHIPPED'
    assert len(shipment_2.FulfillmentShipmentItem.member) == 1
    assert shipment_2.FulfillmentShipmentItem.member[0].SellerSKU == 'SKU101'
    assert shipment_2.FulfillmentShipmentItem.member[0].Quantity == 1
    shipment_2_package, = shipment_2.FulfillmentShipmentPackage.member
    assert shipment_2_package.TrackingNumber == '93ZZ00'
    assert shipment_2_package.CarrierCode == 'UPS'
