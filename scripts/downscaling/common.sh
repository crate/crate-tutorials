#!/bin/sh

display_usage_and_exit() {
    echo "usage: $0 node_name"
    exit 1
}

if [ $# -lt 1 ]; then
    display_usage_and_exit
fi

node_name=$1
path_conf="$(pwd)/conf/$node_name"
if [ ! -d $path_conf ]; then
    echo "No configuration available in [conf/$node_name]."
    exit 1
fi
path_home=$(pwd)/crate
path_data=$(pwd)/data
path_repo=$(pwd)/repo

if [ -z "$CRATE_HEAP_SIZE" ]; then
    export CRATE_HEAP_SIZE="2G"
fi
echo 'setup: '
echo " - path_home: $path_home"
echo " - node_name: $node_name"
echo " - path_data: $path_data"
echo " - path_repo: $path_repo"
echo " - CRATE_HEAP_SIZE: $CRATE_HEAP_SIZE"
