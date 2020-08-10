from io import open
import os

import pytest
import requests_mock

from pymws import MWS


@pytest.fixture()
def mws_client():
    return MWS(
        'US',
        access_key_id='ACESSKEY',
        secret_key='SECRET',
        merchant_id='MERCHANT_ID',
        auth_token='amzn.mws.big-fat-token',
    )


@pytest.fixture()
def mock_adapter(mws_client):
    adapter = requests_mock.Adapter()
    mws_client.session.mount(mws_client.marketplace.endpoint, adapter)
    return adapter


@pytest.fixture()
def example_response():
    def get_example_response(path):
        directory = os.path.dirname(
            os.path.abspath(__file__)
        )
        with open(
                os.path.join(directory, 'responses', path),
                encoding='utf-8') as f:
            return f.read()
    return get_example_response
