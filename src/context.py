import os
from json import load, dump
import requests
from bs4 import BeautifulSoup
import base64


def json_save(data, fname):
    with open(fname, 'w') as fp:
        dump(data, fp)


def json_load(fname):
    with open(fname, 'r') as fp:
        return load(fp)
