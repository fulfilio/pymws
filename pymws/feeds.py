from .utils import flatten_list


class Feeds(object):
    """
    The Amazon MWS Feeds API section of the Amazon Marketplace
    Web Service (Amazon MWS) API lets you upload inventory and
    order data to Amazon.

    .. code-block:: python

        response = client.feeds.submit_feed(
            feed_content_xml,
            FeedType='_POST_INVENTORY_AVAILABILITY_DATA_'
        )
        result = client.feeds.get_feed_submission_result(
            response.FeedSubmissionInfo.FeedSubmissionId
        )

    """
    VERSION = '2009-01-01'
    URI = '/Feeds/' + VERSION

    def __init__(self, client):
        self.client = client

    def submit_feed(self, FeedContent, FeedType, ContentType=None, **kwargs):
        """
        Uploads a feed for processing by Amazon MWS.

        :param FeedContent: String or base string content
        :param FeedType: Type of feed
                         (see `MWS docs <https://docs.developer.amazonservices.com/en_US/feeds/Feeds_FeedType.html>`_)
        :param ContentType: Set the content type of feed.
                            (See `Feedtypes <https://docs.developer.amazonservices.com/en_US/feeds/Feeds_SubmitFeed.html>`_).
                            If not set, this will be guessed based on
                            FeedType

        `Learn more <https://docs.developer.amazonservices.com/en_US/feeds/Feeds_SubmitFeed.html>`_
        """    # noqa: E501
        kwargs['FeedType'] = FeedType
        if ContentType is None:
            if '_FLAT_FILE_' in FeedType:
                ContentType = \
                    'text/tab-separated-values; charset=iso-8859-1'
                FeedContent = FeedContent.encode('iso-8859-1')
            else:
                ContentType = 'text/xml'
        return self.client.post(
            'SubmitFeed', self.URI, kwargs, self.VERSION,
            FeedContent, ContentType
        )

    def get_feed_submission_list(self, **kwargs):
        """
        Returns a list of all feed submissions submitted in the previous 90 days.

        `Learn more <https://docs.developer.amazonservices.com/en_US/feeds/Feeds_GetFeedSubmissionList.html>`_
        """    # noqa: E501
        flatten_list(kwargs, 'FeedSubmissionIdList', 'Id')
        flatten_list(kwargs, 'FeedTypeList', 'Type')
        return self.client.get(
            'GetFeedSubmissionList', self.URI, kwargs, self.VERSION
        )

    def get_feed_submission_list_by_next_token(self, NextToken):
        """
        Returns a list of feed submissions using the NextToken parameter.

        `Learn more <https://docs.developer.amazonservices.com/en_US/feeds/Feeds_GetFeedSubmissionListByNextToken.html>`_
        """    # noqa: E501
        return self.client.get(
            'GetFeedSubmissionListByNextToken', self.URI,
            {'NextToken': NextToken}, self.VERSION
        )

    def get_feed_submission_count(self, **kwargs):
        """
        Returns a count of the feeds submitted in the previous 90 days.

        `Learn more <https://docs.developer.amazonservices.com/en_US/feeds/Feeds_GetFeedSubmissionCount.html>`_
        """    # noqa: E501
        return self.client.get(
            'GetFeedSubmissionCount', self.URI, kwargs, self.VERSION
        )

    def cancel_feed_submissions(self, **kwargs):
        """
        Cancels one or more feed submissions and returns a count of the
        feed submissions that were canceled.

        `Learn more <https://docs.developer.amazonservices.com/en_US/feeds/Feeds_CancelFeedSubmissions.html>`_
        """    # noqa: E501
        return self.client.get(
            'CancelFeedSubmissions', self.URI, kwargs, self.VERSION
        )

    def get_feed_submission_result(self, FeedSubmissionId):
        """
        Returns the feed processing report and the Content-MD5 header.

        `Learn more <https://docs.developer.amazonservices.com/en_US/feeds/Feeds_GetFeedSubmissionResult.html>`_
        """    # noqa: E501
        return self.client.get(
            'GetFeedSubmissionResult', self.URI,
            {'FeedSubmissionId': FeedSubmissionId},
            self.VERSION
        )
