# text-chat

> Chat from command line, make it look like you're working

This documentation isn't finished. Basic steps to get this working with `aws-s3` plugin (the only one so far):

1. Install python3
1. Install boto3 as a python3 module
1. Setup your `~/.aws/credentials` file with appropriate credentials
1. Either create a bucket and a blank file/path/key with the contents of: `[]` (this will be fixed in later versions)
1. Adjust your `text-chat/config` file with appropriate values
1. Run `python3 chat.py -c config`
1. Make sure someone else has appropriate access to the s3 bucket/path
1. ???
1. Look like doing work
