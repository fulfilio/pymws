from .utils import flatten_list


class Reports(object):
    """
    Implements a report client for Amazon MWS.

    The report API works differently from other APIs and
    it is important to have a good understanding of
    how this API works from `MWS reports overview
    <http://docs.developer.amazonservices.com/en_US/reports/Reports_Overview.html>`__
    """    # noqa: E501
    VERSION = '2009-01-01'
    URI = '/Reports/' + VERSION

    def __init__(self, client):
        self.client = client

    def request_report(self, **kwargs):
        """
        Creates a report request and submits the request to Amazon MWS.

        Amazon MWS processes the report request and when the report is
        completed, sets the status of the report request to _DONE_.
        Reports are retained for 90 days.

        `Learn more <Read more: http://docs.developer.amazonservices.com/en_US/reports/Reports_RequestReport.html>`__
        """   # noqa: E501
        flatten_list(kwargs, 'MarketplaceIdList', 'Id')
        return self.client.post(
            'RequestReport', self.URI, kwargs, self.VERSION
        )

    def get_report_request_list(self, **kwargs):
        """
        Returns a list of report requests that you can use to get the
        ReportRequestId for a report.

        `Learn more <http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportRequestList.html>`__
        """   # noqa: E501
        flatten_list(kwargs, 'ReportTypeList', 'Type')
        flatten_list(kwargs, 'ReportRequestIdList', 'Id')
        flatten_list(kwargs, 'ReportProcessingStatusList', 'Status')
        return self.client.get(
            'GetReportRequestList', self.URI, kwargs, self.VERSION
        )

    def get_report_request_list_by_next_token(self, NextToken):
        """
        Returns a list of report requests using the NextToken,
        which was supplied by a previous request to either
        GetReportRequestListByNextToken or GetReportRequestList,
        where the value of HasNext was true in that previous request.

        `Learn more <http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportRequestListByNextToken.html>`__
        """   # noqa: E501
        return self.client.get(
            'GetReportRequestListByNextToken', self.URI,
            {'NextToken': NextToken}, self.VERSION
        )

    def get_report_request_count(self, **kwargs):
        """
        Returns a count of report requests that have been submitted
        to Amazon MWS for processing.

        `Learn more <http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportRequestCount.html>`__
        """   # noqa: E501
        return self.client.get(
            'GetReportRequestCount', self.URI, kwargs, self.VERSION
        )

    def cancel_report_request(self, **kwargs):
        """
        Cancels one or more report requests.

        `Learn more <http://docs.developer.amazonservices.com/en_US/reports/Reports_CancelReportRequests.html>`__
        """  # noqa: E501
        return self.client.post(
            'CancelReportRequests', self.URI, kwargs, self.VERSION
        )

    def get_report_list(self, **kwargs):
        """
        Returns a list of reports that were created in the previous 90 days.

        `Learn more <http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportList.html>`__
        """   # noqa: E501
        flatten_list(kwargs, 'ReportTypeList', 'Type')
        flatten_list(kwargs, 'ReportRequestIdList', 'Id')
        flatten_list(kwargs, 'MarketplaceIdList', 'Id')
        return self.client.get(
            'GetReportList', self.URI, kwargs, self.VERSION
        )

    def get_report_list_by_next_token(self, NextToken):
        """
        Returns a list of reports using the NextToken, which was supplied
        by a previous request to either GetReportListByNextToken or
        GetReportList, where the value of HasNext was true in the
        previous call.

        `Learn more <http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportListByNextToken.html>`__
        """   # noqa: E501
        return self.client.get(
            'GetReportListByNextToken', self.URI,
            {'NextToken': NextToken}, self.VERSION
        )

    def get_report_count(self, **kwargs):
        """
        Returns a count of the reports, created in the previous 90 days,
        with a status of _DONE_ and that are available for download.

        `Learn more <http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportCount.html>`__
        """   # noqa: E501
        return self.client.get(
            'GetReportCount', self.URI, kwargs, self.VERSION
        )

    def get_report(self, ReportId):
        """
        Returns the contents of a report and the Content-MD5 header for the
        returned report body.

        `Learn more <http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReport.html>`__
        """   # noqa: E501
        return self.client.get(
            'GetReport', self.URI,
            {'ReportId': ReportId}, self.VERSION
        )
