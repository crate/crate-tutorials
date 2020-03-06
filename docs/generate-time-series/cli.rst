.. _gen-ts-cli:

===============================================
Generate time series data from the command line
===============================================

This tutorial will show you how to generate some :ref:`experimental time series
data <gen-ts>` from information about the `International Space Station`_
using the `CrateDB Shell`_ (aka *Crash*) and a little bit of `shell scripting`_.

.. SEEALSO::

    :ref:`gen-ts`

.. rubric:: Table of contents

.. contents::
   :local:


Prerequisites
=============

CrateDB must be :ref:`installed and running <install-run>`.

Crash is available as `Pip`_ package. `Install`_ it like this:

.. code-block:: console

    $ pip install crash

We have designed the commands in this tutorial to be run directly from the
`command line`_ so that you can experiment with them as you see fit.

You will need the `curl`_ and `jq`_ tools installed.

.. NOTE::

    This tutorial should work in most POSIX-compatible environments (e.g.,
    Linux, macOS, and Windows Cygwin). Please `let us know`_ if you run into
    issues.


Using ``curl`` to get the current position of the ISS
=====================================================

You can get telemetry data from `Open Notify`_, a third-party service that
provides a simple API to consume data from NASA (specifically, the current
location of the International Space Station). The endpoint for this data is
`<http://api.open-notify.org/iss-now.json>`_.

You can query this endpoint using ``curl``, using the ``-s`` flag to keep
the output to a minimum::

    $ curl -s http://api.open-notify.org/iss-now.json
    {"iss_position": {"latitude": "-51.6051", "longitude": "86.6932"}, "message": "success", "timestamp": 1583490580}

The endpoint returns a JSON payload, which contains an ``iss_position`` object
with ``latitude`` and ``longitude`` data.

Processing the ISS position with ``jq``
=======================================

The ``jq`` command is a convient tool to process JSON payloads on the command
line. You can use the ``|`` character to `pipe`_ the output from ``curl`` into
``jq`` for processing.

For example, to return the whole payload, you can do this::

    $ curl -s http://api.open-notify.org/iss-now.json | jq '.'
    {
      "iss_position": {
        "latitude": "-50.8213",
        "longitude": "97.9703"
      },
      "message": "success",
      "timestamp": 1583490695
    }

However, the most useful information is the latitude and longitude coordinates.
You can use ``jq`` with a filter to isolate those results::

    $ curl -s http://api.open-notify.org/iss-now.json | jq -r '[.iss_position.longitude, .iss_position.latitude] | @tsv'
    111.8643    -48.0634

You're going to want to get the position like this multiple times. You can make
that easier for yourself by defining a `shell function`_  to do it, like so::

    $ position() {curl -s http://api.open-notify.org/iss-now.json | jq -r '[.iss_position.longitude, .iss_position.latitude] | @tsv'; }

Now, when you want the position, you can run ``position``::

    $ position
    126.5203    -42.4264

To insert these values into an SQL query, you need to format them into a `WKT`_
string, which you can do by using the ``echo`` command::

    $ echo "'POINT ($(position))'"
    POINT ( 140.1034 -33.6746 )

Here's a function to do that for you::

    $ wkt_position () { echo "'POINT ($(position))'"; }

Which you can now call using ``wkt_position``::

    $ wkt_position
    POINT ( 143.4071 -30.8853 )


Set up CrateDB
==============

Start an interactive Crash session:

.. code-block:: console

    sh$ crash --hosts localhost:4200

.. NOTE::

    You can omit the ``--hosts`` argument if CrateDB is running on
    ``localhost:4200``. We have included it here for the sake of clarity.
    Modify the argument if you wish to connect to a CrateDB node on a different
    host or port number.

Then, `create a table`_ suitable for writing load averages:

.. code-block:: psql

    cr> CREATE TABLE iss (
            timestamp TIMESTAMP GENERATED ALWAYS AS CURRENT_TIMESTAMP,
            position GEO_POINT
        );

    CREATE OK, 1 row affected  (0.726 sec)

In the `CrateDB Admin UI`_, you should see the new table when you navigate to
the *Tables* screen using the left-hand navigation menu:

.. image:: ../_assets/img/generate-time-series/table.png


Record the ISS position
=======================

With the table in place, you can start recording the position of the ISS.

Crash provides a non-interactive mode that you can use to execute SQL
statements directly from the command line.

First, exit from the interactive Crash session (or open a new terminal). Then,
use ``crash`` with the ``--command`` argument execute an `INSERT`_ query, like
this:

.. code-block:: console

    $ crash --hosts localhost:4200 \
          --command "INSERT INTO iss (position) VALUES (`wkt_position`)"

    CONNECT OK
    INSERT OK, 1 row affected  (0.142 sec)

.. WARNING::

    For any real-world application, you must always sanitize your data before
    interpolating it into an SQL query.

Press the up arrow on your keyboard and hit *Enter* to run the same command a
few more times.

When you're done, you can `SELECT`_ that data back out of CrateDB, like so:

.. code-block:: console

    $ crash --hosts localhost:4200 \
          --command 'SELECT * FROM iss ORDER BY timestamp DESC'
    CONNECT OK
    +---------------+----------------------+
    |     timestamp | position             |
    +---------------+----------------------+
    | 1583491623255 | [156.4084, -17.0207] |
    | 1583491532834 | [152.7272, -21.4128] |
    | 1583491531301 | [152.6639, -21.4852] |
    +---------------+----------------------+
    SELECT 3 rows in set (0.008 sec)

Here you have recorded three sets of ISS position coordinates.

Automate it
===========

Now you have the basics figured out, you can automate the data collection.

Copy the commands you used into a file named ``iss-position.sh``, like this:

.. code-block:: sh

    position() {curl -s http://api.open-notify.org/iss-now.json | jq -r '[.iss_position.longitude, .iss_position.latitude] | @tsv'; }

    wkt_position () { echo "'POINT ($(position))'"; }

    while true; do
        crash --hosts localhost:4200 \
            --command "INSERT INTO iss (position) VALUES (`wkt_position`)"
        echo 'Sleeping for 10 seconds...'
        sleep 10
    done

Here, the script sleeps for 10 seconds after each sample. Accordingly, the time
series data will have a *resolution* of 10 seconds. You may want to configure
your script differently.

Run it from the command line, like so:

.. code-block:: console

    $ sh iss-position.sh

    CONNECT OK
    INSERT OK, 1 row affected  (0.029 sec)
    Sleeping for 10 seconds...
    CONNECT OK
    INSERT OK, 1 row affected  (0.033 sec)
    Sleeping for 10 seconds...
    CONNECT OK
    INSERT OK, 1 row affected  (0.038 sec)
    Sleeping for 10 seconds...

As this runs, you should see the table filling up in the CrateDB Admin UI:

.. image:: ../_assets/img/generate-time-series/rows.png

Lots of freshly generated time series data, ready for use.


.. _command line: https://en.wikipedia.org/wiki/Command-line_interface
.. _CrateDB Admin UI: https://crate.io/docs/clients/admin-ui/en/latest/
.. _CrateDB Shell: https://crate.io/docs/clients/crash/en/latest/
.. _create a table: https://crate.io/docs/crate/reference/en/latest/general/ddl/create-table.html
.. _curl: https://curl.haxx.se/
.. _data sanitization: https://xkcd.com/327/
.. _INSERT: https://crate.io/docs/crate/reference/en/latest/general/dml.html#inserting-data
.. _install: https://crate.io/docs/clients/crash/en/latest/getting-started.html#installation
.. _International Space Station: https://www.nasa.gov/mission_pages/station/main/index.html
.. _jq: https://stedolan.github.io/jq/
.. _let us know: https://github.com/crate/crate-tutorials/issues/new
.. _open notify: http://open-notify.org/
.. _Pip: https://pypi.org/project/pip/
.. _pipe: https://www.geeksforgeeks.org/piping-in-unix-or-linux/
.. _SELECT: https://crate.io/docs/crate/reference/en/latest/general/dql/selects.html
.. _shell function: https://www.gnu.org/software/bash/manual/html_node/Shell-Functions.html
.. _shell scripting: https://en.wikipedia.org/wiki/Shell_script
.. _WKT: https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry
