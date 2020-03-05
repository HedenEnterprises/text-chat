
import argparse
import sys
import os
import time
import importlib
import time
from datetime import datetime


__version__ = '0.0.0'
__default_format__ = '[%%t] %%n > %%m'
__default_prompt__ = 'chat: '
__tmp_file__ = 'tmp'


def parse_arguments():
    parser = argparse.ArgumentParser(description = 'text-chat: make it look like you\'re working from cli')
    parser.add_argument('-p', '--print-backends', action = 'store_true',
        help = 'print available backends and quit')
    parser.add_argument('-i', '--interactive', action = 'store_true',
        help = 'run chat in interactive mode')
    parser.add_argument('-b', '--backend', metavar = '<backend>',
        help = 'the chat server backend')
    parser.add_argument('-c', '--config', required = True, metavar = '<file>',
        help = 'the configuration file to use')
    parser.add_argument('-s', '--send', metavar = '<message>',
        help = 'a message to send to the chat server')
    parser.add_argument('-f', '--format', metavar = '<fmt string>', default = __default_format__,
        help = 'the message formatter. %%n: name, %%m: msg, %%t: human time, %%T: unix time, default (' + __default_format__ + ')')
    parser.add_argument('-v', '--version', action = 'version', version = __version__,
        help = 'print version information and quit')
    parser.add_argument('-P', '--prompt', default = __default_prompt__,
        help = 'the prompt to display for chat input, default (' + __default_prompt__ + ')')
    parser.add_argument('-n', '--name',
        help = 'the name to identify yourself as in the chat')
    return parser.parse_args()


def process_config(options):

    # check config path
    if not os.path.exists(options.config):
        print("specified config file (" + options.config + ") not found!")
        sys.exit(1)

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

        # we want command line options to override config file values

        if key == "interactive" and options.interactive != True:
            if value.lower().startswith("t"):
                options.interactive = True
            else:
                options.interactive = False

        if key == "backend" and options.backend == None:
            options.backend = value

        if key == "format" and options.format != __default_format__:
            options.format = value

        if key == "prompt" and options.format != __default_prompt__:
            options.prompt = value

        if key == "name" and options.name == None:
            options.name = value

    file.close()

    return options


def sanity_check(options):

    # check if backend was specified
    if options.backend == "" or options.backend == None:
        print("no backend specified!")
        sys.exit(1)

    # make sure the plugin file exists
    backend = options.backend.replace("-", "/")
    plugin_file = "backends/" + backend + "/plugin.py"
    if not os.path.exists(plugin_file):
        print("plugin (" + options.backend + ") requires file '" + plugin_file + "', file not found!")
        sys.exit(1)

    # need a name specified
    if options.name == "" or options.name == None:
        print("you need a name to chat, silly")
        sys.exit(1)

    # todo: check that all necessary functions exist in the plugin


# this function should be as easy as:
# ```
# import_str = "from backends." + backend.replace("-", ".") + " import plugin"
# exec(import_str)
# ```
# but i can't get it to work. so just maintain a list of backend/file
# because it just works
def load_plugin(options):

    # load appropriate backend
    try:
        if options.backend == "aws-s3":
            from backends.aws.s3 import plugin
    except:
        print("something went wrong loading plugin")

    global plugin

    options = plugin.process_config(options)
    plugin.sanity_check(options)
    plugin.init(options)
    return options


def check_for_new_messages(options):
    return plugin.check_for_new_messages(options)


def format_messages(messages, format):
    formatted_messages = []
    for message in messages:
        message_time = int(message['time'])
        formatted_message = format.replace('%%n', message['name']).replace('%%m', message['message']).replace('%%t', datetime.fromtimestamp(message_time).strftime('%Y-%m-%d %H:%M:%S')).replace('%%T', str(message['time']))
        formatted_messages.append(formatted_message)
    return formatted_messages


def print_messages(formatted_messages):
    for message in formatted_messages:
        print(message)


def send_chat(message, options):

    # don't send blank messages
    if message == "" or message == None:
        return

    plugin.send_chat(message, options)


options = process_config(parse_arguments())
sanity_check(options)
options = load_plugin(options)
options.tmp_file = __tmp_file__


# main loop
while True:

    messages = check_for_new_messages(options)
    print_messages(format_messages(messages, options.format))
    send_chat(input(options.prompt), options)

    if not options.interactive:
        break

    time.sleep(1)
