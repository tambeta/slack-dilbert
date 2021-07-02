#!/usr/bin/env python3

import collections
import configparser
import contextlib
import datetime
import os
import re
import sys

import bs4
import requests
import xdg

CONFIG_FN = xdg.XDG_CONFIG_HOME / "dilbertrc"
GUARD_FN = xdg.XDG_CACHE_HOME / "dilbertts"
COMIC_PAGE_URL = "https://dilbert.com"
COMIC_NAME = "Dilbert"
USER_AGENT = "dilbert/0.1"



Comic = collections.namedtuple("Comic", ["url", "title"])

def fetch_comic_page():

    """ Fetch the daily comic URL and return the raw HTML string. """

    response = requests.get(COMIC_PAGE_URL, headers={"User-Agent": USER_AGENT})

    if not response.ok:
      response.raise_for_status()

    return response.text

def scrape_comic(html):

    """ Scrape and return the comic image URL given a HTML string. """
    
    soup = bs4.BeautifulSoup(html, "html.parser")    
    img = soup.find("img", class_="img-comic")
    
    if not img:
        raise LookupError("Could not look up the comic image tag")
    
    return Comic(img['src'], re.sub(r"\s*-[^-]*$", "", img['alt']))
    
def guard_against_duplicate():

    """ Guard against duplicate posting on a given date. Also checks for
    guard file existence, readability and writability - all are
    required.
    """

    post_date = None
    today = str(datetime.date.today())

    if not os.access(GUARD_FN, os.F_OK):
        err("Guard file {} not found: create manually for safety", GUARD_FN)
    if not os.access(GUARD_FN, os.R_OK | os.W_OK):
        err("Guard file {} is not readable or writable", GUARD_FN)

    with open(GUARD_FN, "r") as f:
        post_date = f.read().strip()

    if post_date == today:
        err("Already posted to Slack today: refusing to post again before tomorrow")

def write_guard_file():
    with open(GUARD_FN, "w") as f:
        print(datetime.date.today(), file=f)

def get_slack_webhook_url():

    """ Read the Slack integration URL from $XDG_CONFIG_HOME/dilbertrc. """

    config = configparser.ConfigParser()
    config.read(CONFIG_FN)

    try:
        return config["slack"]["webhook_url"]
    except KeyError:
        err("Slack webhook URL not configured in {} - see documentation for details", CONFIG_FN)

def post_to_slack(comic):
    webhook_url = get_slack_webhook_url()
    alt_text = "Dilbert {}".format(datetime.date.today())
    block = dict(type="image", image_url=comic.url, alt_text=alt_text)
    
    requests.post(webhook_url, json=dict(blocks=[block])).raise_for_status()

def err(msg, *args):
    print(msg.format(*args), file=sys.stderr)
    raise SystemExit(1)

def main():
    guard_against_duplicate()

    html = fetch_comic_page()
    comic = scrape_comic(html)

    post_to_slack(comic)
    write_guard_file()

main()
