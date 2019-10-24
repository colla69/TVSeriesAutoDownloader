import os
from json import load, dump
import requests
from bs4 import BeautifulSoup
import base64

conf_path = os.path.expanduser("~/.config/SeriesAutoDownloader/")
json_name = "config.json"


def json_save(data, fname):
    with open(fname, 'w') as fp:
        dump(data, fp)


def json_load(fname):
    with open(fname, 'r') as fp:
        return load(fp)


def load_config():
    if not os.path.exists(conf_path):
        os.mkdir(conf_path)
    try:
        conf = json_load(conf_path+json_name)
    except Exception as e:
        print(e)
        conf = None
    return conf
