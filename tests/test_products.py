def test_list_orders(mws_client, mock_adapter, example_response):
    mock_adapter.register_uri(
        'GET',
        mws_client.marketplace.endpoint + '/Products/2011-10-01',
        status_code=200,
        text=example_response('products/get_matching_product_for_id.xml'),
        headers={'Content-Type': 'text/xml'}
    )
    response = mws_client.products.get_matching_product_for_id(
        IdList=['9781933988665', '0439708184'],
        IdType='ISBN',
    )
    assert len(response) == 2
