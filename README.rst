=================
Python MWS Client
=================


.. image:: https://img.shields.io/pypi/v/pymws.svg
        :target: https://pypi.python.org/pypi/pymws

.. image:: https://github.com/fulfilio/pymws/workflows/CI%20(pip)/badge.svg
        :target: https://github.com/fulfilio/pymws/actions

.. image:: https://readthedocs.org/projects/pymws/badge/?version=latest
        :target: https://pymws.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/fulfilio/pymws/shield.svg
     :target: https://pyup.io/repos/github/fulfilio/pymws/
     :alt: Updates



Python client for Amazon Marketplace Web Services (MWS)


* Free software: MIT license
* Documentation: https://pymws.readthedocs.io.


Installation
------------

.. code-block::

    pip install pymws

Usage
-----

Import the package

.. code-block:: python

    from pymws import MWS

Create a client instance

.. code-block:: python

  client = MWS(
      marketplace="US", merchant_id="1234",
      access_key_id="key", secret_key="secret",
      auth_token="token"
  )

Once you have a client with valid credentials, you can now
call operations.

.. code-block:: python

  start_date = datetime(2020, 1, 20, 10, 30)
  client.orders.list_orders(CreatedAfter=start_date)
