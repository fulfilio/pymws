
def test_submit_feed(mws_client, mock_adapter, example_response):
    mock_adapter.register_uri(
        'POST',
        mws_client.marketplace.endpoint + '/Feeds/2009-01-01',
        status_code=200,
        text=example_response('feeds/submit_feed.xml'),
        headers={'Content-Type': 'text/xml'}
    )
    response = mws_client.feeds.submit_feed(
        '<mock></mock>',
        '_POST_ORDER_ACKNOWLEDGEMENT_DATA_'
    )
    assert response.FeedSubmissionInfo.FeedSubmissionId
    assert response.FeedSubmissionInfo.FeedProcessingStatus == '_SUBMITTED_'

    response = mws_client.feeds.submit_feed(
        b'<mock></mock>',
        '_POST_ORDER_ACKNOWLEDGEMENT_DATA_'
    )
    assert response.FeedSubmissionInfo.FeedSubmissionId
    assert response.FeedSubmissionInfo.FeedProcessingStatus == '_SUBMITTED_'


def test_feed_result(mws_client, mock_adapter, example_response):
    mock_adapter.register_uri(
        'GET',
        mws_client.marketplace.endpoint + '/Feeds/2009-01-01',
        status_code=200,
        text=example_response('feeds/result-failed.xml'),
        headers={'Content-Type': 'text/xml'}
    )
    response = mws_client.feeds.get_feed_submission_result('4901340')
    assert response.MessageType == 'ProcessingReport'


def test_feed_submission_count(mws_client, mock_adapter, example_response):
    mock_adapter.register_uri(
        'GET',
        mws_client.marketplace.endpoint + '/Feeds/2009-01-01',
        status_code=200,
        text=example_response('feeds/submission-count.xml'),
        headers={'Content-Type': 'text/xml'}
    )
    response = mws_client.feeds.get_feed_submission_count()
    assert response.Count == 463


def test_feed_submission_cancel(mws_client, mock_adapter, example_response):
    mock_adapter.register_uri(
        'GET',
        mws_client.marketplace.endpoint + '/Feeds/2009-01-01',
        status_code=200,
        text=example_response('feeds/submission-cancel.xml'),
        headers={'Content-Type': 'text/xml'}
    )
    response = mws_client.feeds.cancel_feed_submissions()
    assert response.Count == 1


def test_feed_submission_list(mws_client, mock_adapter, example_response):
    mock_adapter.register_uri(
        'GET',
        mws_client.marketplace.endpoint + '/Feeds/2009-01-01',
        status_code=200,
        text=example_response('feeds/submission-list.xml'),
        headers={'Content-Type': 'text/xml'}
    )
    response = mws_client.feeds.get_feed_submission_list()
    assert response.NextToken
    assert response.FeedSubmissionInfo.FeedType == '_POST_PRODUCT_DATA_'


def test_feed_submission_list_next(mws_client, mock_adapter, example_response):
    mock_adapter.register_uri(
        'GET',
        mws_client.marketplace.endpoint + '/Feeds/2009-01-01',
        status_code=200,
        text=example_response('feeds/submission-list-token.xml'),
        headers={'Content-Type': 'text/xml'}
    )
    response = mws_client.feeds.get_feed_submission_list_by_next_token(
        'next-token'
    )
    assert response.NextToken == 'none'
    assert response.FeedSubmissionInfo.FeedType == '_POST_PRODUCT_DATA_'
