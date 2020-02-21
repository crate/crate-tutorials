.. _gen-ts-python:

======================================
Generate time series data using Python
======================================

This tutorial will show you how to generate some :ref:`experimental time series
data <gen-ts>` by consuming telemetry data from the `International Space Station`_
using `Python`_.

.. SEEALSO::

    :ref:`gen-ts`

.. rubric:: Table of contents

.. contents::
   :local:


Prerequisites
=============

CrateDB must be :ref:`installed and running <install-run>`.

Make sure you're running an up-to-date Python (we recommend 3.7 or higher).

Then, use `Pip`_ to install the `requests`_ and  `crate`_ libraries:

.. code-block:: console

    $ pip install requests crate

The rest of this tutorial is designed for Python's `interactive mode`_ so that
you can experiment with the commands as you see fit. The `standard
Python interpreter`_ works fine for this, but we recommend `IPython`_ for a more
user-friendly experience.

You can install IPython with Pip:

.. code-block:: console

    $ pip install ipython

Once installed, you can start an interactive IPython session like this:

.. code-block:: console

    $ ipython


Use Python to get to get ISS telemetry data
===========================================

You will be consuming telemetry data from `Open Notify`_, a service which provides
a simple API to consume data from NASA. One of these data points is the current location
of the International Space Station. The endpoint for these data can be found at
`<http://api.open-notify.org/iss-now.json>`_.

Start an interactive Python session. Then, import the `requests`_ library::

    >>> import requests

Once imported, we can request the current position of the ISS::

    >>> response = requests.get('http://api.open-notify.org/iss-now.json')
    >>> response.json()
    {
        'message': 'success',
        'iss_position': {
            'longitude': '-148.7513',
            'latitude': '9.9132'
        },
        'timestamp': 1582293874
    }

The endpoint returns a JSON payload consisting of ``iss_position``, which is composed of
``latitude`` and ``longitude``, as well as some other metadata.

You can encapsulate this within a single function to return only the longitude and latitude as a `WKT`_
string::

    >>> def position():
    ...     response = requests.get('http://api.open-notify.org/iss-now.json')
    ...     position = response.json()["iss_position"]
    ...     return f'POINT ({position["longitude"]} {position["latitude"]})'

When you run this function, it should return your point string::

    >>> position()
    'POINT (-30.9188 42.8036)'

Set up CrateDB
==============

First, import the `crate`_ client module:

    >>> from crate import client

Then, `connect`_ to CrateDB:

    >>> connection = client.connect("localhost:4200")

.. NOTE::

    You can omit the function argument if CrateDB is running on
    ``localhost:4200``. We have included it here for the sake of clarity.
    Modify the argument if you wish to connect to a CrateDB node on a different
    host or port number.

Get a `cursor`_:

    >>>  cursor = connection.cursor()

Then, finally, `create a table`_ suitable for writing load averages:

    >>> cursor.execute(
    ...     """CREATE TABLE iss_position (
    ...            timestamp TIMESTAMP GENERATED ALWAYS AS CURRENT_TIMESTAMP,
    ...            position GEO_POINT)"""
    ... )

In the `CrateDB Admin UI`_, you should see the new table when you navigate to
the *Tables* screen using the left-hand navigation menu:

.. image:: ../_assets/img/generate-time-series/table.png


Record the ISS position
=======================

With the table in place, you can start recording the position of the ISS.

The following command calls your ``position`` function and uses the result as `input
values`_ for the `INSERT`_ query:

    >>> cursor.execute("INSERT INTO iss_position (position) VALUES (?)", [position()])

Press the up arrow on your keyboard and hit *Enter* to run the same command a
few more times.

When you're done, you can `SELECT`_ that data back out of CrateDB, like so:

    >>> cursor.execute('SELECT * FROM iss_position ORDER BY timestamp DESC')

Then, `fetch all`_ the result rows at once:

    >>> cursor.fetchall()
    [[1582295967721, [-8.0689, 25.8967]],
     [1582295966383, [-8.1371, 25.967]],
     [1582295926523, [-9.9662, 27.8032]]]

Here you have recorded three sets of ISS position coordinates.


Automate it
===========

Now we have the basics figured out, let's automate the data collection.

Copy the commands you used into a file named ``iss-position.py``, like this:

.. code-block:: python

    import time

    import requests
    from crate import client

    def position():
        response = requests.get('http://api.open-notify.org/iss-now.json')
        position = response.json()["iss_position"]
        return f'POINT ({position["longitude"]} {position["latitude"]})'


    def insert():
        # New connection each time
        connection = client.connect("localhost:4200")
        print("CONNECT OK")
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO iss_position (position) VALUES (?)",
            [position()],
        )
        print("INSERT OK")


    # Loop indefinitely
    while True:
        insert()
        print("Sleeping for 10 seconds...")
        time.sleep(10)

Here, the script sleeps for 10 seconds after each sample. Accordingly, the time
series data will have a *resolution* of 10 seconds. You may want to configure
your script differently.

Run it from the command line, like so:

.. code-block:: console

    $ python iss-position.py
    CONNECT OK
    INSERT OK
    Sleeping for 10 seconds...
    CONNECT OK
    INSERT OK
    Sleeping for 10 seconds...
    CONNECT OK
    INSERT OK
    Sleeping for 10 seconds...

As this runs, you should see the table filling up in the CrateDB Admin UI:

.. image:: ../_assets/img/generate-time-series/rows.png

Lots of freshly generated time series data, ready for use.


.. _connect: https://crate.io/docs/clients/python/en/latest/connect.html
.. _crate: https://crate.io/docs/clients/python/en/latest/
.. _CrateDB Admin UI: https://crate.io/docs/clients/admin-ui/en/latest/
.. _create a table: https://crate.io/docs/crate/reference/en/latest/general/ddl/create-table.html
.. _cursor: https://crate.io/docs/clients/python/en/latest/query.html#using-a-cursor
.. _fetch all: https://crate.io/docs/clients/python/en/latest/query.html#fetchmany
.. _input values: https://crate.io/docs/clients/python/en/latest/query.html#regular-inserts
.. _INSERT: https://crate.io/docs/crate/reference/en/latest/general/dml.html#inserting-data
.. _interactive mode: https://docs.python.org/3/tutorial/interpreter.html#interactive-mode
.. _interactive Python session: https://docs.python.org/3/tutorial/interpreter.html#interactive-mode
.. _international space station: https://www.nasa.gov/mission_pages/station/main/index.html
.. _Internet of Things: https://en.wikipedia.org/wiki/Internet_of_things
.. _IPython: https://ipython.org/
.. _open notify: http://open-notify.org/
.. _Pip: https://pypi.org/project/pip/
.. _Python: https://www.python.org/
.. _requests: https://requests.readthedocs.io/en/master/
.. _SELECT: https://crate.io/docs/crate/reference/en/latest/general/dql/selects.html
.. _standard Python interpreter: https://docs.python.org/3/tutorial/interpreter.html
.. _time series: https://en.wikipedia.org/wiki/Time_series
.. _WKT: https://en.wikipedia.org/wiki/Youll-known_text_representation_of_geometry
