# text-chat

> Chat from command line, make it look like you're working

This documentation isn't finished. Basic steps to get this working with `aws-s3` plugin (the only one so far):

1. Install python3
1. Install boto3 as a python3 module
1. Install aws cli (if you've completed the preceding steps, just run `pip install awscli`)
1. Setup your `~/.aws/credentials` file with appropriate credentials
1. Either create a bucket and a blank file/path/key with the contents of: `[]` (this will be fixed in later versions)
1. Adjust your `text-chat/config` file with appropriate values
1. Run `python3 chat.py -c config`
1. Make sure someone else has appropriate access to the s3 bucket/path
1. ???
1. Look like doing work


## The prompts and message formatter

There are two important components to making this look more like you're working while you're actually chatting. The first is the chat prompt. The default chat prompt is:

```
chat: _
```

That gives too much away. Let's say you've cloned this repository in your user directory (`/home/heden/text-chat`)... Wouldn't a better prompt be something like:

```
heden@machine-name:~ $
```

Or whatever your default prompt is for your terminal of choice. A good example of a Windows prompt might be:

```
C:\Users\Heden\ > _
```

So now that we have that out of the way, let's talk about the message formatter. Whenever your `text-chat` reaches out to its defined source and downloads new messages, they're passed through a message formatter - because who wants to read raw json. Actually, that might look more like you're working after all - *stay tuned for future plugins*.

The default message formatter is:

```
[%t] %n > %m
```

There are only a few options:

* `%n` - The name of the person who sent the chat
* `%m` - The contents of the chat message that they sent
* `%t` - The human readable version of the time (`%Y-%m-%d %H:%M:%S` format) that the message was sent
* `%T` - The unix timestamp of the time that the message was sent

Wouldn't something better look like:

```
%n@machine-name:~ $ _
```

(or on Windows):

```
C:\Users\%%n> _
```

*Note:* the double `%` is not an accident. This is necessary when you specify the formatter from the command line.

So, putting this altogether might look something like:-P "heden@machine-name:~ $"

```
python3 chat.py -c config -f "%n@machine-name:~ $ " -P "heden@machine-name:~ $"
```

```
python chat.py -c config -f "C:\Users\%%n> %%m" -P "C:\Users\Heden> "
```


## FAQ

* Q: Did you try and recreate IRC?
* A: No


## Backend plugin API

> Documentation is work in progress

To write a plugin, all you need to do is:

1. Create the appropriate directories in `backend/` directory. (Example: `aws-s3` requires a directory `backends/aws/s3`)
1. Create a file `plugin.py` in that directory
1. I haven't figured out how to use variable import directories in python yet, so you'll have to update the conditional block in the `load_plugin()` function in `chat.py` to accomodate your new plugin
1. More data on what these do later - but at the very least your new plugin must contain the following functions:
    1. `init`
    1. `process_configs`
    1. `check_for_new_messages`
    1. `send_chat`
    1. `sanity_check`
1. ???
1. Be a giant cli-based chat corporation? (If you find some way to make money off of this, and you don't include me I'm going to send you at least one very angry letter. It'll probably be an electronic letter - aka email)


### `init`

* arguments:
    * `options`
* details:
    

