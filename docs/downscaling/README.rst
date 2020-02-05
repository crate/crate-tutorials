===========
Downscaling
===========

In this tutorial we:

- Create a Vanilla cluster.
- Downscale it, using replicas.


Starting a Vanilla cluster
--------------------------

A Vanilla cluster is a three node cluster that runs on a single host. Each of the
nodes share the file system and operating system scheduler of the host, to form a
cluster. This rig provides parallel processing power on large scale data, when you
only have one host, and this comes at the cost increased latency in writes.

Proceed:

1. *~/.../crate-tutorials/scripts/downscaling* should contain:

   - *update-dist*: script to install **CrateDB**.
   - *dist*: **CrateDB** distributions.
   - *crate*: a symlink to a particular distribution in the *dist* folder (not
     the **CrateDB**, executable script), where you will also find a *crate-clone*
     git repository.
   - *conf*: **CrateDB** configurations, each node in the cluster has a folder
     in there, with the *crate.yml* and *log4j2.properties*.
   - *data*: **CrateDB** the nodes will persist their data under *data/nodes/[0,1,2]*.
   - *repo*: **CrateDB** repo, for snapshotting.
   - *start-node*: script to start **CrateDB** with a given configuration.
   - *detach-node*: script to detach a node from the cluster.
   - *bootstrap-node*: script to bootstrap a node to form a new cluster.
   - *data.py*: script produce dummy data.

2. Run *./update-dist*

   - This will install the latest, unreleased, **CrateDB** under *dist/*, creating
     a link *./crate -> dist/crate..*.
   - Assumed **git**, **java 11** or later, **python3** and a **terminal** are
     available to you, and you have an account in GitHub_.

3. The configuration for the Vanilla cluster:

    - *~/.../crate-tutorials/scripts/downscaling/conf/n1/crate.yml*
    - *~/.../crate-tutorials/scripts/downscaling/conf/n2/crate.yml*
    - *~/.../crate-tutorials/scripts/downscaling/conf/n3/crate.yml*
    - *~/.../crate-tutorials/scripts/downscaling/conf/log4j2.properties*

4. Run *./startnode* in three different terminals

   - *./startnode n1*
   - *./startnode n2*
   - *./startnode n3*

   Which will form the Vanilla cluster, electing a master. You can
   interact with the Vanilla cluster by opening a browser and pointing
   it to *http://localhost:4200*, *CrateDB*'s `Admin UI`_.


Adding some data to the cluster
-------------------------------

Proceed:

1. Produce a CSV_ file containing 3600 rows of log data (1 hour's worth of logs @1Hz):

  ::

    ./data.py > logs.csv

2. In the `Admin UI`_:

  ::

    CREATE TABLE logs (log_time timestamp NOT NULL,
                       client_ip ip NOT NULL,
                       request string NOT NULL,
                       status_code short NOT NULL,
                       object_size long NOT NULL);

     COPY logs FROM 'file:///.../crate-tutorials/scripts/downscaling/logs.csv';
     REFRESH TABLE logs;
     select * from logs order by log_time limit 10800;

  The three nodes perform the copy, so we are expecting to see 3600 * 3 rows, with
  what looks like "repeated" data. Because we did not define a primary key, **CrateDB**
  created the default *_id* primary key, which is a unique hash (varchar), so in effect,
  because each row has a unique id, they are all inserted.


Exploring the Data
------------------

Using the `Admin UI`_, shards view on the left:

.. image:: imgs/shards-view.png

We can see the three nodes, each having a number of shards, specifically:

    +-------+---+---+---+---+---+---+
    | Shard | 0 | 1 | 2 | 3 | 4 | 5 |
    +=======+===+===+===+===+===+===+
    |  n1   | . | . | . |   | . |   |
    +-------+---+---+---+---+---+---+
    |  n2   | . | . |   | . |   | . |
    +-------+---+---+---+---+---+---+
    |  n3   |   |   | . | . | . | . |
    +-------+---+---+---+---+---+---+

Thus in this cluster setup, one node can crash, yet the data in the cluster
will still remain fully available because any two nodes have access to all
the shards, when they work together to fulfill query requests. A SQL table
is a composite of shards, six in our case. When a query is executed, the
planner will define steps for accessing all the shards of the table.
By adding nodes to the cluster, the data is spread over more nodes, so that
the computing is parallelized.

Having a look at the setup for table *logs*:

::

  SHOW CREATE TABLE logs;

Will return:

::

  CREATE TABLE IF NOT EXISTS "doc"."logs" (
     "log_time" TIMESTAMP WITH TIME ZONE NOT NULL,
     "client_ip" IP NOT NULL,
     "request" TEXT NOT NULL,
     "status_code" SMALLINT NOT NULL,
     "object_size" BIGINT NOT NULL
  )
  CLUSTERED INTO 6 SHARDS
  WITH (
     ...
     number_of_replicas = '0-1',
     ...
  )

We have a default min number of replicas of zero, and a max of one for each
of our six shards. A replica is simply a copy or a shard.


Downscaling (by means of replicas)
----------------------------------

Downscaling by means of replicas is achieved by making sure the surviving nodes
of the cluster have access to all the shards, even when the other nodes are missing.

1. We need to ensure that the number of replicas matches the number of nodes:

::

  ALTER TABLE logs SET (number_of_replicas = '1-all');

In the `Admin UI`_, we can follow the progress of the replication, and when it
is completed we can take the nodes down (*ctrl^C* in the terminal).

2. Run *./detach-node* to detach **n1** from the cluster:



At this point we just need to adjust the configuration of the surviving node,
and then restart it:

::

  *cat ~/workspace/DATA/conf/n2/crate.yml*

      ::

        node.name: n2
        stats.service.interval: 0
        network.host: _local_
        http.cors.enabled: true
        http.cors.allow-origin: "*"





.. _GitHub: https://github.com/crate/crate.git
.. _`Admin UI`: http://localhost:4200
.. _crate-node: https://crate.io/docs/crate/reference/en/latest/cli-tools.html#cli-crate-node
.. _CSV: https://en.wikipedia.org/wiki/Comma-separated_values