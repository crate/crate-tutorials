.. _create-sharded-table:

====================
Create sharded table
====================

One core concept CrateDB uses to distribute data across a cluster is sharding. CrateDB splits every table into a configured number of shards, which are distributed evenly across the cluster. You can think of shards as sub-tables with corresponding sub-indexes. If we create a table like the following:

.. code-block:: psql

    CREATE TABLE first_table (
        ts TIMESTAMP,
        val DOUBLE PRECISION
    );

the table is by default is split into 4 shards on a single node cluster. You can check this by running:

.. code-block:: psql

    SHOW CREATE TABLE first_table;

Which should output the following:

.. code-block:: psql

    CREATE TABLE IF NOT EXISTS "doc"."first_table" (
        "ts" TIMESTAMP WITH TIME ZONE,
        "val" DOUBLE PRECISION
    )
    CLUSTERED INTO 4 SHARDS

By default, ingested data is distributed evenly across all available shards. In many cases you don't have to worry about specifying any sharding key or routing column. 



Partitioning
============

CrateDB also supports splitting up data across another dimension with partitioning. You can think of a partition as a set of shards. For each partition the number of shards defined by ``CLUSTERED INTO x SHARDS`` are created, when a first row with a specific partition key is inserted.

In the following example - which represents a very simple time-series use-case - we added another column ``part`` which automatically generates the current month upon insert from the ``ts`` column. The ``part`` column is further used as the _partition key_.

.. code-block:: psql

    CREATE TABLE second_table (
        ts TIMESTAMP,
        val DOUBLE PRECISION,
        part GENERATED ALWAYS AS date_trunc('month',ts)
    ) PARTITIONED BY(part);

If we now insert a first row with the following statement:

.. code-block:: psql

    INSERT INTO second_table (ts,val) VALUES (1617823229974, 1.23);

and then querying for the total amount of shards for the table:

.. code-block:: psql

    SELECT COUNT(*) FROM sys.shards
    WHERE table_name = 'second_table';

We can see that the table is split into 4 shards.

Adding another row to the table with a different partition key (i.e. different month):

.. code-block:: psql

    INSERT INTO second_table (ts,val) VALUES (1620415701974, 2.31);

We can see that there are now 8 shards for the table ``second_table`` in the cluster.


.. danger::

    **Over-sharding and over-partitioning**

    Sharding can drastically improve the performance on large datasets. However, having too many small shards will most likely degrade performance. Over-sharding and over-partitioning are common flaws leading to an overall poor performance.

    **As a rule of thumb, a single shard should hold somewhere between 5 - 100 GB of data.**



.. tip::

    **Example**: You want to create a *partitioned table* on your *single node cluster* to store time-series data with the following assumptions:

    - Inserts: 1.000 records / s
    - Record size: 128 byte / record
    - Throughput: 125 KB / s or 10.3 GB / day

    Depending on query patterns, a good partition key would most likely be the extracted week or month (considering 4 shards per partition). This would give an average shard size between 18 GB to 80 GB.

.. note::

    An optimum sharding and partitioning strategy is always dependant on the use case and typically should be found by conducting benchmarks across various strategies.
