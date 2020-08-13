#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from click.testing import CliRunner
import pytest

from pymws import MWS, cli
from pymws.exceptions import AccessDenied
from pymws.utils import flatten_list, flatten_dict


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'pymws.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_query_string_builder():
    params = {
        'Name': 'ST',
        'City': 'Los Ángeles',
        'Timestamp': datetime(2020, 1, 1, 10, 30, 30)
    }
    client = MWS('US')
    assert client.build_query_string(params) == \
        'City=Los%20%C3%81ngeles&Name=ST&Timestamp=2020-01-01T10%3A30%3A30'


def test_list_flattening():
    kwargs = {'ReportTypeList': ['_A_', '_B_']}
    flatten_list(
        kwargs,
        'ReportTypeList',
        'Type'
    )
    assert kwargs['ReportTypeList.Type.1'] == '_A_'
    assert kwargs['ReportTypeList.Type.2'] == '_B_'

    kwargs = {}
    flatten_list(
        kwargs,
        'InexistentKey',
        'Type'
    )
    assert not kwargs


def test_dict_flattening():
    kwargs = {
        'DestinationAddress': {
            'Name': 'John Doe',
            'Line1': 'Random street',
            'StateOrProvinceCode': 'CA',
            'CountryCode': 'US',
        }
    }
    flatten_dict(
        kwargs,
        'DestinationAddress',
    )
    assert kwargs['DestinationAddress.Name'] == 'John Doe'
    assert kwargs['DestinationAddress.CountryCode'] == 'US'

    kwargs = {}
    flatten_dict(
        kwargs,
        'DestinationAddress',
    )
    assert not kwargs


def test_get_service_status(mws_client, mock_adapter, example_response):
    mock_adapter.register_uri(
        'GET',
        mws_client.marketplace.endpoint + '/Orders/2013-09-01',
        status_code=401,
        text=example_response('401.xml'),
        headers={'Content-Type': 'text/xml'}
    )
    with pytest.raises(AccessDenied):
        mws_client.orders.get_service_status()
