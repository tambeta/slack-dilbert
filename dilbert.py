#!/usr/bin/env python3

import configparser
import contextlib
import datetime
import sys

import bs4
import requests
import xdg

CONFIG_FN = xdg.XDG_CONFIG_HOME / "dilbertrc"
GUARD_FN = xdg.XDG_CACHE_HOME / "dilbertts"
COMIC_PAGE_URL = "https://www.postimees.ee/comics"
COMIC_NAME = "Dilbert"
USER_AGENT = "dilbert/0.1"



def fetch_comic_page():

    """ Fetch the daily comic URL and return the raw HTML string. """

    response = requests.get(COMIC_PAGE_URL, headers={"User-Agent": USER_AGENT})

    if not response.ok:
      response.raise_for_status()

    return response.text

def scrape_comic_url(html):

    """ Scrape and return the comic image URL given a HTML string. """

    soup = bs4.BeautifulSoup(html, "html.parser")
    dilbert_title = soup.find(class_="comics-item__name", string=COMIC_NAME)

    with contextlib.suppress(AttributeError):
        for el in dilbert_title.next_siblings:
            if el.name == "img" and "comics-item__img" in el["class"]:
                return el["src"]

    raise LookupError("Could not look up the comic image tag")

def guard_against_duplicate():
    post_date = None
    today = str(datetime.date.today())

    with contextlib.suppress(FileNotFoundError):
        with open(GUARD_FN, "r") as f:
            post_date = f.read().strip()

    if post_date == today:
        err("Already posted to Slack today: refusing to post again before tomorrow")

    with open(GUARD_FN, "w") as f:
        print(today, file=f)

def get_slack_webhook_url():

    """ Read the Slack integration URL from $XDG_CONFIG_HOME/dilbertrc. """

    config = configparser.ConfigParser()
    config.read(CONFIG_FN)

    try:
        return config["slack"]["webhook_url"]
    except KeyError:
        err("Slack webhook URL not configured in {}. See documentation for details.", CONFIG_FN)

def post_to_slack(url):
    webhook_url = get_slack_webhook_url()
    response = requests.post(webhook_url, json=dict(text=url))

    response.raise_for_status()

def err(msg, *args):
    print(msg.format(*args), file=sys.stderr)
    raise SystemExit(1)

def main():
    html = fetch_comic_page()
    url = scrape_comic_url(html)

    guard_against_duplicate()
    post_to_slack(url)

main()
