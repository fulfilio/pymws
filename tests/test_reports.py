from datetime import datetime


def test_request_report(mws_client, mock_adapter, example_response):
    mock_adapter.register_uri(
        'POST',
        mws_client.marketplace.endpoint + '/Reports/2009-01-01',
        status_code=200,
        text=example_response('reports/request_report.xml'),
        headers={'Content-Type': 'text/xml'}
    )
    response = mws_client.reports.request_report(
        ReportType='_GET_MERCHANT_LISTINGS_DATA_',
        StartDate=datetime(2009, 1, 3, 18, 12, 21),
        MarketplaceIdList=['ATVPDKIKX0DER'],
    )
    assert response.ReportRequestInfo.ReportProcessingStatus == '_SUBMITTED_'


def test_report_request_list(mws_client, mock_adapter, example_response):
    mock_adapter.register_uri(
        'GET',
        mws_client.marketplace.endpoint + '/Reports/2009-01-01',
        status_code=200,
        text=example_response('reports/get_report_request_list.xml'),
        headers={'Content-Type': 'text/xml'}
    )
    response = mws_client.reports.get_report_request_list(
        ReportTypeList=[
            '_GET_ORDERS_DATA_',
            '_GET_MERCHANT_LISTINGS_DATA_',
        ],
        ReportProcessingStatusList=[
            '_DONE_',
        ],
        ReportRequestIdList=['2291326454'],
        MarketplaceIdList=['ATVPDKIKX0DER'],
    )

    assert 'ReportTypeList.Type.1=_GET_ORDERS_DATA_' in \
        mock_adapter.request_history[0].url

    assert response.ReportRequestInfo.ReportProcessingStatus == '_DONE_'
    assert response.NextToken


def test_report_request_list_by_next_token(
        mws_client, mock_adapter, example_response):
    mock_adapter.register_uri(
        'GET',
        mws_client.marketplace.endpoint + '/Reports/2009-01-01',
        status_code=200,
        text=example_response(
            'reports/get_report_request_list_by_next_token.xml'
        ),
        headers={'Content-Type': 'text/xml'}
    )
    response = mws_client.reports.get_report_request_list_by_next_token(
        NextToken='2YgYW55IPQhcm5hbCBwbGVhc3VyZS4='
    )
    assert response.ReportRequestInfo.ReportProcessingStatus == '_SUBMITTED_'
    assert response.NextToken


def test_get_report_tsv(
        mws_client, mock_adapter, example_response):
    mock_adapter.register_uri(
        'GET',
        mws_client.marketplace.endpoint + '/Reports/2009-01-01',
        status_code=200,
        text=example_response(
            'reports/get_report_tab_separated.tsv'
        ),
        headers={'Content-Type': 'text/plain;charset=Cp1252'}
    )
    response = mws_client.reports.get_report(123456789)
    assert len(response) == 3
    assert response[0]['listing-id'] == '0305XXNBYUQ'


def test_get_report_csv(
        mws_client, mock_adapter, example_response):
    mock_adapter.register_uri(
        'GET',
        mws_client.marketplace.endpoint + '/Reports/2009-01-01',
        status_code=200,
        text=example_response(
            'reports/get_report_comma_separated.csv'
        ),
        headers={'Content-Type': 'text/plain;charset=Cp1252'}
    )
    response = mws_client.reports.get_report(123456789)
    assert len(response) == 2
    assert response[0]['sku'] == 'test-1'
