#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from click.testing import CliRunner

from pymws import MWS, cli

"""Tests for `pymws` package."""


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
    }
    client = MWS('US')
    assert client.build_query_string(params) == \
        'City=Los%20%C3%81ngeles&Name=ST'
