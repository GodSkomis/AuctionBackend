#!/bin/sh

if [ -z "$@" ];
then
    echo "Remove leftover socket file"
    rm /tmp/*.sock
else
    eval $@
fi