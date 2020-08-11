#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from click.testing import CliRunner

from pymws import MWS, cli
from pymws.utils import flatten_list


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
