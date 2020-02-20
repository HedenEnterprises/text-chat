
import sys

def chat():

    # read config file

    # parse arguments
    backend = "aws-s3"

    # load appropriate backend
    if backend == "aws-s3":
        from backends.aws.s3 import plugin
    # elif backend == "":
    else:
        print("No backend specified!")
        sys.exit(1)

    # parse main command
    #if cmd == "read":


chat()
