.. _gen-ts-cli:

===============================================
Generate time series data from the command line
===============================================

This tutorial will show you how to generate some :ref:`experimental time series
data <gen-ts>` by sampling your `system load`_ using the `CrateDB Shell`_ (aka
*Crash*) and a little bit of `shell scripting`_.

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

We designed the commands in this tutorial to be run directly from the `command
line`_ so that you can experiment with them as you see fit.

.. NOTE::

    This tutorial should work in most POSIX-compatible environments (e.g.,
    Linux, macOS, and Windows Cygwin). Please `let us know`_ if you run into
    issues.


Process ``uptime`` to get your system load
==========================================

The `uptime`_ command is a convenient way to get your current system load.

The exact output varies a little from system to system, but the ``uptime``
command will typically display something like this:

.. code-block:: console

    $ uptime
    16:58  up 3 days,  5:45, 4 users, load averages: 3.15 4.51 5.06

We can `pipe`_ that through `sed`_ to get the load averages:

.. code-block:: console

    $ uptime | sed -E 's/.*load average(s)?: //' | sed 's/,//g'
    3.06 4.46 5.04

The result is three load values separated by a space. The values correspond to
the one minute average, five-minute average, and 15-minute average.

.. NOTE::

    This command should work for most output formats. Please `let us know`_ if
    you run into issues.

We're going to want to get the load averages like this multiple times, so let's
make things easier for ourselves by defining a `shell function`_ that does it:

.. code-block:: console

    $ loads () { uptime | sed -E 's/.*load average(s)?: //' | sed 's/,//g'; }

Now, when you want the load averages, you can run ``loads``:

.. code-block:: console

    $ loads
    3.06 4.46 5.04

However, we're not finished with our string processing.

To insert these values into an SQL query, we need to be able to get them
individually. There are multiple ways to accomplish this, for example:

.. code-block:: console

    $ loads | cut -d ' ' -f1
    3.06

Here, we told `cut`_ to print the value in the first column, which in our case
is ``3.06``. You can print the second column by changing the ``1`` to ``2``,
and so on.

Let's define another function to do this for us:

.. code-block:: console

    $ avg () { loads | cut -d ' ' -f$1; }

Here, the ``avg`` function:

  1. Calls the ``loads`` function (which prints load average values in three
     columns)

  2. Prints the value in column ``$1`` (the first argument passed to the
     function)

Now, to get the first load average, you can do this:

.. code-block:: console

    $ avg 1
    3.63

Or, get all three, like this:

.. code-block:: console

    $ echo "`avg 1` `avg 2` `avg 3`"
    3.63 4.62 5.10


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

    cr> CREATE TABLE load (
            timestamp TIMESTAMP GENERATED ALWAYS AS CURRENT_TIMESTAMP,
            avg_1m REAL,
            avg_5m REAL,
            avg_15m REAL
        );

    CREATE OK, 1 row affected  (0.726 sec)

In the `CrateDB Admin UI`_, you should see the new table when you navigate to
the *Tables* screen using the left-hand navigation menu:

.. image:: ../_assets/img/generate-time-series/table.png


Record your system load
=======================

With the table in place, you can start recording load averages.

Crash provides a non-interactive mode that you can use to execute SQL
statements directly from the command line.

First, exit from the interactive Crash session (or open a new terminal). Then,
use ``crash`` with the ``--command`` argument execute an `INSERT`_ query, like
this:

.. code-block:: console

    $ crash --hosts localhost:4200 \
          --command "INSERT INTO load (avg_1m, avg_5m, avg_15m) \
              VALUES (`avg 1`, `avg 2`, `avg 3`)"

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
          --command 'SELECT * FROM load ORDER BY timestamp DESC'
    CONNECT OK
    +---------------+--------+--------+---------+
    |     timestamp | avg_1m | avg_5m | avg_15m |
    +---------------+--------+--------+---------+
    | 1580668593202 |   3.28 |   4.4  |    4.45 |
    | 1580668521049 |   4.88 |   4.91 |    4.62 |
    | 1580668509451 |   5.09 |   4.95 |    4.63 |
    +---------------+--------+--------+---------+
    SELECT 3 rows in set (0.008 sec)

Here we have recorded three sets of load averages with a corresponding
timestamp.

Automate it
===========

Now we have the basics figured out, let's automate the data collection.

Copy the commands you used into a file named ``monitor-load.sh``, like this:

.. code-block:: sh

    loads () { uptime | sed -E 's/.*load average(s)?: //' | sed 's/,//g'; }

    avg () { loads | cut -d ' ' -f$1; }

    while true; do
        crash --hosts localhost:4200 \
            --command "INSERT INTO load (avg_1m, avg_5m, avg_15m) \
                VALUES (`avg 1`, `avg 2`, `avg 3`)"
        echo 'Sleeping for 10 seconds...'
        sleep 10
    done

Here, the script sleeps for 10 seconds after each sample. Accordingly, the time
series data will have a *resolution* of 10 seconds. You may want to configure
your script differently.

Run it from the command line, like so:

.. code-block:: console

    $ sh monitor-load.sh

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
.. _cut: https://www.geeksforgeeks.org/cut-command-linux-examples/
.. _data sanitization: https://xkcd.com/327/
.. _INSERT: https://crate.io/docs/crate/reference/en/latest/general/dml.html#inserting-data
.. _install: https://crate.io/docs/clients/crash/en/latest/getting-started.html#installation
.. _let us know: https://github.com/crate/crate-tutorials/issues/new
.. _Pip: https://pypi.org/project/pip/
.. _pipe: https://www.geeksforgeeks.org/piping-in-unix-or-linux/
.. _sed: https://www.geeksforgeeks.org/sed-command-in-linux-unix-with-examples/
.. _SELECT: https://crate.io/docs/crate/reference/en/latest/general/dql/selects.html
.. _shell function: https://www.gnu.org/software/bash/manual/html_node/Shell-Functions.html
.. _shell scripting: https://en.wikipedia.org/wiki/Shell_script
.. _STDIN: https://en.wikipedia.org/wiki/Standard_streams
.. _system load: https://en.wikipedia.org/wiki/Load_(computing)
.. _uptime: https://www.geeksforgeeks.org/linux-uptime-command-with-examples/
