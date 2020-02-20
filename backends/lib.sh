#!/bin/bash

function check_args ()
{
    if [ $1 -ne $2 ]; then
        shift
        shift
        echo $@
        exit 1
    fi
}

function check_deps ()
{
    badDeps=0

    while (( "$#" )); do

        if ! which $1 >/dev/null 2>&1; then
            echo "Missing dependency '$1'"
            badDeps=$(( $badDeps + 1 ))
        fi
        shift
    done

    if [ $badDeps -gt 0 ]; then
        exit 1
    fi
}
