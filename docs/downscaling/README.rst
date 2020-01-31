===========
Downscaling
===========

In this tutorial we:

1. We create a Vanilla cluster.
2. Downscaling!, using replicas.
3. Downscaling!, using snapshots.


Starting a Vanilla cluster
--------------------------

A Vanilla cluster is a three node cluster that runs on a single host. Each of the
nodes share the file system and operating system scheduler of the host, to form a cluster.
This rig provides parallel processing power on large scale data, when you only have one
host, and this comes at the cost increased latency in writes.

Steps:

1. `git clone https://github.com/crate/crate.git`

   Naturally, **git**, **java 11** or later, and a **terminal** are available to you,
   and you have an account in GitHub_.

2. Execute:

   - `cd crate`
   - `./gradlew clean` (if you already had the clone)
   - `./gradlew distTar`.

3. Create a folder somewhere, I suggest `~/workspace/DATA`. It should contain this structure:

   - `~/workspace/DATA/dist`: **CrateDB** distributions.
   - `~/workspace/DATA/conf`: **CrateDB** configurations, each node has a folder in there, and the
     folder contains the `crate.yml` and `log4j2.properties` configuration files.
   - `~/workspace/DATA/data`: **CrateDB** data, be mindful on how you setup the `path.data`.
   - `~/workspace/DATA/repo`: **CrateDB** repo, be mindful on how you setup the `path.repo`.
   - `~/workspace/DATA/startnode`: script to start **CrateDB** on a given config, read on.
   - `~/workspace/DATA/crate`: a symlink to a particular distribution in the `dist` folder.

4. `cp crate/app/build/distributions/crate-X.Y.Z-SNAPSHOT-<hash>.tar.xz ~/workspace/DATA/dist`

5. Execute:

   - `cd ~/workspace/DATA/dist`
   - `tar -xzvf crate-X.Y.Z-SNAPSHOT-<hash>.tar.xz`

     Now you have a folder `~/workspace/DATA/dist/crate-X.Y.Z` with the latest **CrateDB**.
   - `cd ~/workspace/DATA`
   - `rm -f crate`
   - `ln -s dist/crate-X.Y.Z crate`

6.- Now we need the configuration for the Vanilla cluster:

    - `cat ~/workspace/DATA/conf/n1/crate.yml`

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

    - `cat ~/workspace/DATA/conf/n2/crate.yml`

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

    - `cat ~/workspace/DATA/conf/n2/crate.yml`

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

    - You may use this `log4j2.properties` setup:

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

7. The `startnode` script could look something like this:

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

   - `./startnode n1`
   - `./startnode n2`
   - `./startnode n3`

   Which will form the Vanilla cluster.


Downscaling (by means of replicas)
----------------------------------


Downscaling (by means of snapshots)
-----------------------------------


.. _GitHub: https://github.com/crate/crate.git