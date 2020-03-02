#!/bin/bash

. ../../lib.sh

check_args $# 1 "Usage: ./$0 <s3-bucket-name> <optional region>"
check_deps aws
check_python_deps boto3

name=$1
region=""

if [ x$2 != x ]; then
    region="--region $2"
fi

aws s3api create-bucket --bucket $name $region
