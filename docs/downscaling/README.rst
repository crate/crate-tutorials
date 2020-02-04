===========
Downscaling
===========

In this tutorial we:

- Create a Vanilla cluster.
- Downscale it, using replicas.
- Downscale it, using snapshots.


Starting a Vanilla cluster
--------------------------

A Vanilla cluster is a three node cluster that runs on a single host. Each of the
nodes share the file system and operating system scheduler of the host, to form a
cluster. This rig provides parallel processing power on large scale data, when you
only have one host, and this comes at the cost increased latency in writes.

Proceed:

1. *git clone https://github.com/crate/crate.git*

   Assumed **git**, **java 11** or later, and a **terminal** are available to you,
   and you have an account in GitHub_.

2.

   - *cd crate*
   - *./gradlew clean* (if you already had the clone)
   - *./gradlew distTar*.

3. Create a folder somewhere, I suggest *~/workspace/DATA*. It should contain this
   structure:

   - *dist*: **CrateDB** distributions.
   - *conf*: **CrateDB** configurations, each node in the cluster has a folder
     in there, with the *crate.yml* and *log4j2.properties* configuration files
     in it.
   - *data*: **CrateDB** through configuration the nodes will log under
     *data/nodes/[0,1,2]*
   - *repo*: **CrateDB** repo, for snapshotting.
   - *startnode*: script to start **CrateDB** with a given config.
   - *crate*: a symlink to a particular distribution in the *dist* folder (not
     the **CrateDB**, executable script).

4. *cp crate/app/build/distributions/crate-X.Y.Z-SNAPSHOT-<hash>.tar.xz ~/workspace/DATA/dist*

5.

   - *cd ~/workspace/DATA/dist*
   - *tar -xzvf crate-X.Y.Z-SNAPSHOT-<hash>.tar.xz*

     At this point you have a folder, *~/workspace/DATA/dist/crate-X.Y.Z*, containing the
     latest, unreleased, **CrateDB**.

   - *cd ~/workspace/DATA*
   - *rm -f crate*
   - *ln -s dist/crate-X.Y.Z crate*

6.- Now you need the configuration for the Vanilla cluster:

    - *cat ~/workspace/DATA/conf/n1/crate.yml*

      ::

        cluster.name: vanilla
        node.name: n1
        stats.service.interval: 0
        network.host: _local_
        node.max_local_storage_nodes: 3
        http.cors.enabled: true
        http.cors.allow-origin: "*"
        transport.tcp.port: 4301
        gateway.expected_nodes: 3
        gateway.recover_after_nodes: 2
        discovery.seed_hosts:
        - 127.0.0.1:4301
        - 127.0.0.1:4302
        cluster.initial_master_nodes:
        - 127.0.0.1:4301
        - 127.0.0.1:4302

    - *cat ~/workspace/DATA/conf/n2/crate.yml*

      ::

        cluster.name: vanilla
        node.name: n2
        stats.service.interval: 0
        network.host: _local_
        node.max_local_storage_nodes: 3
        http.cors.enabled: true
        http.cors.allow-origin: "*"
        transport.tcp.port: 4302
        gateway.expected_nodes: 3
        gateway.recover_after_nodes: 2
        discovery.seed_hosts:
        - 127.0.0.1:4301
        - 127.0.0.1:4302
        cluster.initial_master_nodes:
        - 127.0.0.1:4301
        - 127.0.0.1:4302

    - *cat ~/workspace/DATA/conf/n3/crate.yml*

      ::

        cluster.name: vanilla
        node.name: n3
        stats.service.interval: 0
        network.host: _local_
        node.max_local_storage_nodes: 3
        http.cors.enabled: true
        http.cors.allow-origin: "*"
        transport.tcp.port: 4303
        gateway.expected_nodes: 3
        gateway.recover_after_nodes: 2
        discovery.seed_hosts:
        - 127.0.0.1:4301
        - 127.0.0.1:4302
        cluster.initial_master_nodes:
        - 127.0.0.1:4301
        - 127.0.0.1:4302

    - And for convenience, you may use this *log4j2.properties* setup, save it to a file
      alongside each *crate.yml*.:

      ::

        status = error
        rootLogger.level = info
        rootLogger.appenderRef.console.ref = console
        # log action execution errors for easier debugging
        logger.action.name = org.crate.action.sql
        logger.action.level = debug
        appender.console.type = Console
        appender.console.name = console
        appender.console.layout.type = PatternLayout
        appender.console.layout.pattern = [%d{ISO8601}][%-5p][%-25c{1.}] [%node_name] %marker%m%n

7. The *startnode* script could look something like this:

   ::

     #!/bin/sh

     node_name=default
     path_data=$(pwd)/data
     path_repo=$(pwd)/repo
     case $# in
         1)
           node_name=$1
           ;;

         2)
           node_name=$1
           path_data=$2
           ;;

         3)
           node_name=$1
           path_data=$2
           path_repo=$3
           ;;

         -h | -help | --h | --help)
            echo "syntax: $0 [node_name [data_path [repo_path]]]"
            echo 'defaults: '
            echo " - node_name: default"
            echo " - path_data: $path_data"
            echo " - path_repo: $path_repo"
            exit 1
           ;;
     esac

     path_conf="$(pwd)/conf/$node_name"
     if [ ! -d  $path_conf ]; then
       echo "No configuration available in [conf/$node_name]."
       exit 1
     fi

     export CRATE_HEAP_SIZE=2G
     echo 'setup: '
     echo " - node_name: $node_name"
     echo " - path_data: $path_data"
     echo " - path_repo: $path_repo"
     echo " - CRATE_HEAP_SIZE: $CRATE_HEAP_SIZE"

     ./crate/bin/crate -Cpath.conf=$path_conf -Cpath.data=$path_data -Cpath.repo=$path_repo

8. Now in three separate terminals, start the three nodes:

   - *./startnode n1*
   - *./startnode n2*
   - *./startnode n3*

   Which will form the Vanilla cluster, electing a leader. You can interact
   with the Vanilla cluster by opening a browser and pointing it to
   *http://localhost:4200*.


Adding some data to the cluster
-------------------------------

Proceed:

1. Create a table:

  ::

    CREATE TABLE logs (log_time timestamp NOT NULL,
                       client_ip ip NOT NULL,
                       request string NOT NULL,
                       status_code short NOT NULL,
                       object_size long NOT NULL);

2. Produce a CSV file with some data for the logs table. You could use a *data.py*
   script similar to:

  ::

    #!/usr/bin/env python3

    import random
    import string
    import ipaddress
    import time


    # to achieve log lines as in:
    #     2012-01-01T00:00:00Z,25.152.171.147,/books/Six_Easy_Pieces.html,404,271
    # -> timestamp,
    # -> random ip address,
    # -> random request,
    # -> random status code,
    # -> random object size,

    def timestamp_range(start, end, format):
        st = int(time.mktime(time.strptime(start, format)))
        et = int(time.mktime(time.strptime(end, format)))
        dt = 1 # 1 sec
        fmt = lambda x: time.strftime(format, time.localtime(x))
        return (fmt(x) for x in range(st, et, dt))

    def rand_ip():
        return str(ipaddress.IPv4Address(random.getrandbits(32)))

    def rand_request():
        rand = lambda src: src[random.randint(0, len(src) - 1)]
        path = lambda: "/".join((rand(("usr", "bin", "workspace", "temp", "home", "crate"))) for _ in range(4))
        name = lambda: ''.join(random.sample(string.ascii_lowercase, 7))
        ext = lambda: rand(("html", "pdf", "log", "gif", "jpeg", "js"))
        return "{}/{}.{}".format(path(), name(), ext())

    def rand_object_size():
        return str(random.randint(0, 1024))

    def rand_status_code():
        return str(random.randint(100, 500))

    if __name__ == "__main__":
        print("log_time,client_ip,request,status_code,object_size")
        for ts in timestamp_range("2019-01-01T00:00:00Z", "2019-01-01T01:00:00Z", '%Y-%m-%dT%H:%M:%SZ'):
            print(",".join([ts, rand_ip(), rand_request(), rand_status_code(), rand_object_size()]))

  to produce 3600 rows (1 hour's worth of logs @1Hz):

  ::

    ./data.py > logs.csv

3. Load the data:

   ::

     COPY logs FROM 'file:///..<path>../logs.csv';
     REFRESH TABLE logs;
     SELECT count(*) FROM logs;

   The three nodes perform the copy, so we are expecting to see 3600 * 3 rows, with
   "repeated" data. Because we did not define a primary key, **CrateDB** created the
   default *_id* primary key, which is a unique hash (varchar), so in effect, because
   each row has a unique id, they are all inserted, and the net effect is that you
   think there are duplicates.

   ::

     select _id, * from logs order by log_time limit 10000;


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

Having a look at the setup for table *logs*:

::

  SHOW CREATE TABLE logs;

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
of the cluster have access to all the shards, even when one node is missing.

1.- We need to ensure that the number of replicas matches the number of nodes:

::

  ALTER TABLE logs SET (number_of_replicas = '1-all');

In the `Admin UI`_, we can follow the progress of the replication, and when it
is completed we can take two nodes down.

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


Downscaling (by means of snapshots)
-----------------------------------


.. _GitHub: https://github.com/crate/crate.git
.. _`Admin UI`: http://localhost:4200