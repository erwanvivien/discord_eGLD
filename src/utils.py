import requests
import json

import os
import datetime


LOG_FILE = "db/log"


def get_content(file):
    # Read file content
    try:
        file = open(file, "r")
        s = file.read()
        file.close()
    except Exception as error:
        log("get_content", error, f"error reading file {file}")
        return ""

    return s


def log(fctname, error, message):
    now = datetime.datetime.now()
    log = f"[{now}]: " + \
        str(error) + '\n' + ('+' * 4) + (' ' * 4) + \
        fctname + (" " * (20-len(fctname))) + \
        ': ' + message + '\n'

    print(log)

    f = open(LOG_FILE, "a+")

    f.write(log)
    f.close()


if not os.path.exists("db"):
    log("DB folder", "DB folder did not exist", "Creating DB folder")

    os.mkdir("db")
    f = open(LOG_FILE, "w")
    f.close()
