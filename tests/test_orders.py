from decimal import Decimal


def test_list_orders(mws_client, mock_adapter, example_response):
    mock_adapter.register_uri(
        'GET',
        mws_client.marketplace.endpoint + '/Orders/2013-09-01',
        status_code=200,
        text=example_response('orders/list_orders.xml'),
        headers={'Content-Type': 'text/xml'}
    )
    response = mws_client.orders.list_orders()
    assert len(response.Orders.getchildren()) == 3
    assert response.Orders.Order[0].AmazonOrderId == '111-1234567-0000001'
    assert response.NextToken


def test_list_orders_by_next_token(mws_client, mock_adapter, example_response):
    mock_adapter.register_uri(
        'GET',
        mws_client.marketplace.endpoint + '/Orders/2013-09-01',
        status_code=200,
        text=example_response('orders/list_orders_by_next_token.xml'),
        headers={'Content-Type': 'text/xml'}
    )
    response = mws_client.orders.list_orders_by_next_token('TOKEN')
    assert len(response.Orders.getchildren()) == 2
    assert response.Orders.Order[0].AmazonOrderId == '111-1234567-0000002'
    assert response.NextToken


def test_list_order_items(mws_client, mock_adapter, example_response):
    mock_adapter.register_uri(
        'GET',
        mws_client.marketplace.endpoint + '/Orders/2013-09-01',
        status_code=200,
        text=example_response('orders/list_order_items.xml'),
        headers={'Content-Type': 'text/xml'}
    )
    response = mws_client.orders.list_order_items('111-1234567-0000001')
    assert len(response.OrderItems.getchildren()) == 1
    assert response.AmazonOrderId == '111-1234567-0000001'
    item1 = response.OrderItems.OrderItem[0]
    assert item1.ASIN == 'B0X1X2X3X4X5'
    assert Decimal(item1.ItemPrice.Amount.text) == Decimal('139.00')


def test_get_service_status(mws_client, mock_adapter, example_response):
    mock_adapter.register_uri(
        'GET',
        mws_client.marketplace.endpoint + '/Orders/2013-09-01',
        status_code=200,
        text=example_response('orders/get_service_status.xml'),
        headers={'Content-Type': 'text/xml'}
    )
    response = mws_client.orders.get_service_status()
    assert response.Status == 'GREEN'
