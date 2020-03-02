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

function set_python3_bin ()
{
    # get major installed binary version
    output=$(python --version 2>&1 | awk '{print $2}' | sed 's/\..*//')
    if [ "$output" != "3" ]; then
        if which python3 >/dev/null 2>&1; then
            alias python='python3'
        else
            echo "Can't find python3!"
            exit 1
        fi
    fi
}

function check_python_deps ()
{
    badDeps=0

    while (( "$#" )); do

        if ! python -c "import $1" >/dev/null 2>&1; then
            echo "Python needs $1 - try \`pip install $1\`"
            badDeps=$(( $badDeps + 1))
        fi
        shift
    done

    if [ $badDeps -gt 0 ]; then
        exit 1
    fi
}

set_python3_bin
