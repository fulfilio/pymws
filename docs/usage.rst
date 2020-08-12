=====
Usage
=====

To use Python MWS Client in a project::

    import pymws

Create a client instance by providing credentials::

    client = MWS(
        marketplace="US", merchant_id="1234",
        access_key_id="key", secret_key="secret",
        auth_token="token"
    )

Now you have a client instance, that can then be used
for operations.

Quick start
-----------

Fetch a list of orders::

    start_date = datetime(2020, 1, 20, 10, 30)
    response = client.orders.list_orders(CreatedAfter=start_date)

The returned response is the XML result from the API call as an
lxml object. You can browse through the response::

    for order in response.Orders.getchildren():
        print(order.AmazonOrderId)

The returned lxml objectify object is a quick and easy way to
navigate the XML response.
    
To fetch the next page of orders::

    orders_page_2 = client.orders.list_orders_by_next_token(
        response.NextToken
    )


Design pattern
--------------

The API client is a thin layer over the MWS api. Methods
accept the same parameters as the MWS api and hence MWS
API documentation for your marketplace should be your
primary reference.

Supported parameters
````````````````````

All parameters provided are passed directly to the MWS
API after type casting into the appropriate format. For
example, dates and datetimes are converted into the ISO
format.

List parameters are treated differently. Amazon MWS API
requires you to enumerate paramaters.

For example, if you want to get the report list for two
report ids, Amazon expects it to be enumerated::


    POST /Reports/2009-01-01 HTTP/1.1
    ...
    ...

    &ReportRequestIdList.Id.1=2291326454
    &ReportRequestIdList.Id.2=2294446454
    ...


The equivalent with the api would be::

    client.reports.get_report_list(
        ReportRequestIdList=['2291326454', '2294446454']
    )


Response objects
`````````````````

Amazon MWS API supports two primary response formats:

* XML
* Tab separated value (TSV) list

TSVs are more common for reports while XML is the default
response type for most responses.


XML responses
.............

XML responses are converted into lxml objectify objects.
Knowing how to use the lxml API can make your code prettier
and simpler.

* `Example parsing with lxml <https://www.saltycrane.com/blog/2011/07/example-parsing-xml-lxml-objectify/>`_
* `Objectify API docs <https://lxml.de/objectify.html>`_

TSV responses
.............

Any tsv response is converted into a list of dictionaries.

Example using settlement reports::

    available_reports = reports = client.reports.get_report_list(
        ReportTypeList=['_GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2_']
    )
    tsv_report = client.reports.get_report(
        available_reports.ReportInfo[0].ReportId
    )

Browse the list::

    for row in tsv_report:
        print(row['marketplace-name'])
