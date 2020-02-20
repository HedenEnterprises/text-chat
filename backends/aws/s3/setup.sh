#!/bin/bash

. ../../lib.sh

check_args $# 1 "Usage: ./$0 <s3-bucket-name>"
check_deps aws

name=$1
