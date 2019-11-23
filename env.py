import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


def one(key):
    return os.environ.get(key)


def API_KEY():
    return one("API_KEY")


def SUMMARY_KEY():
    return one("SUMMARY_KEY")
