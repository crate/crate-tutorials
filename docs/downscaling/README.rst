===========
Downscaling
===========

In this tutorial we:

1. Create a Vanilla cluster.
2. Downscale it!, using replicas.
3. Downscale it!, using snapshots.


Starting a Vanilla cluster
--------------------------

A Vanilla cluster is a three node cluster that runs on a single host. Each of the
nodes share the file system and operating system scheduler of the host, to form a cluster.
This rig provides parallel processing power on large scale data, when you only have one
host, and this comes at the cost increased latency in writes.

Proceed:

1. *git clone https://github.com/crate/crate.git*

   Assumed **git**, **java 11** or later, and a **terminal** are available to you,
   and you have an account in GitHub_.

2.

   - *cd crate*
   - *./gradlew clean* (if you already had the clone)
   - *./gradlew distTar*.

3. Create a folder somewhere, I suggest *~/workspace/DATA*. It should contain this structure:

   - *dist*: **CrateDB** distributions.
   - *conf*: **CrateDB** configurations, each node in the cluster has a folder in there, with
     the *crate.yml* and *log4j2.properties* configuration files in it.
   - *data*: **CrateDB** through configuration the nodes will log under *data/nodes/[0,1,2]*
   - *repo*: **CrateDB** repo, for snapshotting.
   - *startnode*: script to start **CrateDB** with a given config.
   - *crate*: a symlink to a particular distribution in the *dist* folder (not the **CrateDB**,
     executable script).

4. *cp crate/app/build/distributions/crate-X.Y.Z-SNAPSHOT-<hash>.tar.xz ~/workspace/DATA/dist*

5.

   - *cd ~/workspace/DATA/dist*
   - *tar -xzvf crate-X.Y.Z-SNAPSHOT-<hash>.tar.xz*

     At this point you have a folder, *~/workspace/DATA/dist/crate-X.Y.Z*, containing the
     latest, unreleased, **CrateDB**.

   - *cd ~/workspace/DATA*
   - *rm -f crate*
   - *ln -s dist/crate-X.Y.Z crate*

6.- Now we need the configuration for the Vanilla cluster:

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

   Which will form the Vanilla cluster.


Adding some data to the cluster
-------------------------------

You can interact with the Vanilla cluster by opening a browser and pointing it to
*http://localhost:4200*.

Proceed:

1. Create a table:

  ::

    CREATE TABLE logs (log_time timestamp NOT NULL,
                       client_ip ip NOT NULL,
                       request string NOT NULL,
                       status_code short NOT NULL,
                       object_size long NOT NULL);

2. Produce a CSV file with some data for the logs table. You could use a script like:

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

  to produce 3600 rows:

  ::

    ./data.py > logs.csv

3. Load the data:

   ::

     COPY logs FROM 'file:///...../logs.csv';
     REFRESH TABLE logs;
     SELECT count(*) FROM logs;

     The three nodes would have performed the copy, so we are expecting to see 3600 * 3 rows, with "repeated"
     data. Because we did not define a primary key, **CrateDB** created the default *_id*, which is a
     monotonic unique long.


Downscaling (by means of replicas)
----------------------------------





Downscaling (by means of snapshots)
-----------------------------------


.. _GitHub: https://github.com/crate/crate.git