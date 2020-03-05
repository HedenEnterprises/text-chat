
import boto3
import sys
import os
import json
import time


def init(options):

    global s3client
    global s3resource

    try:
        s3client = boto3.client("s3", verify = False)
        s3resource = boto3.resource("s3", verify = False)
    except:
        print("something went wrong initializing s3 client/resource")
        sys.exit(1)


def process_config(options):

    try:
        file = open(options.config, "r")
    except:
        print("something went wrong opening file (" + options.config + ") for reading")
        sys.exit(1)

    for l in file:
        line = l.strip()
        words = line.split("=")
        if len(words) != 2:
            continue
        key = words[0].strip()
        value = words[1].strip()

        if key == "s3bucket":
            options.s3bucket = value
        if key == "s3path":
            options.s3path = value

    file.close()
    return options


def get_s3_file(options):
    try:
        s3client.download_file(options.s3bucket, options.s3path, options.tmp_file)
    except:
        print("something went wrong downloading s3://" + options.s3bucket + "/" + options.s3path + " to file (" + options.tmp_file + ")")


def put_s3_file(options):
    try:
        s3client.upload_file(options.tmp_file, options.s3bucket, options.s3path)
    except:
        type, value, traceback = sys.exc_info()
        print("exception: type: " + type + ", value: " + value + ", traceback: " + traceback)
        print("something went wrong uploading file (" + options.tmp_file + ") to s3://" + options.s3bucket + "/" + options.s3path)



def check_for_new_messages(options):

    # get the bucket
    get_s3_file(options)

    # load the file as object
    file = open(options.tmp_file)
    
    messages = json.load(file)
    file.close()

    unread_messages = []
    processed_messages = []

    # loop over messages and generate the message list
    for message in messages:
        if "read-by" not in message or options.name not in message["read-by"]:
            unread_messages.append(message)
        if "read-by" not in message:
            message["read-by"] = []
        if options.name not in message["read-by"]:
            message["read-by"].append(options.name)
        processed_messages.append(message)

    # update the local file
    file = open(options.tmp_file, "w")
    json.dump(processed_messages, file)
    file.close()

    # upload the file to the bucket
    put_s3_file(options)

    # delete the tmp file
    #os.remove(options.tmp_file)

    # return all the un-read messages
    return unread_messages


def send_chat(contents, options):

    message = { 
        "message" : contents,
        "name": options.name,
        "time": str(int(time.time())),
        "read-by": [ options.name ]
    }
    
    # get the bucket
    get_s3_file(options)

    file = open(options.tmp_file)
    messages = json.load(file)
    file.close()

    try:
        messages.append(message)
    except:
        print("something wrong appending message..")

    file = open(options.tmp_file, "w")
    json.dump(messages, file)
    file.close()

    put_s3_file(options)

    os.remove(options.tmp_file)


def sanity_check(options):
    
    if "s3bucket" not in options:
        print("must specify 's3bucket' in config file")
        sys.exit(1)

    if "s3path" not in options:
        print("must specify 's3path' in config file")
        sys.exit(1)
