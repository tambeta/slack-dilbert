#!/usr/bin/env python3

import argparse
import configparser
import json
import logging
import re
import sys
import traceback

import requests

from lib.configloader import config
from lib.logging import make_log_record
from lib.provider import Provider
from lib.guard import Guard
from lib.util import AllowException

def invoke_provider(provider, guard, force=False):
    
    """ Fetch latest resource of the given provider and post if fresh. """

    resource = provider.fetch_latest_resource()
    
    if force or guard.is_resource_fresh(provider, resource):
        if force:
            logging.info(f"Posting latest resource for \"{provider.id}\" regardless of freshness")
        else:
            logging.info(f"Latest resource for \"{provider.id}\" is fresh ({resource.id}), posting")
        
        post_to_slack(resource)
        guard.write_id(provider, resource)
    else:
        logging.info(f"Latest resource for \"{provider.id}\" is stale ({resource.id})")

def post_to_slack(resource):
    webhook_url = get_slack_webhook_url()
    block = dict(type="image", image_url=resource.url, alt_text=resource.alt_text)
    
    if (resource.title):
        block.update(dict(
            title=dict(
                type="plain_text",
                text=resource.title
            )
        ))
    
    requests.post(webhook_url, json=dict(blocks=[block])).raise_for_status()
    
def get_slack_webhook_url():

    """ Read the Slack integration URL from $XDG_CONFIG_HOME/dilbertrc. """

    config_fn = config.user_config_fn
    user_config = configparser.ConfigParser()
    
    user_config.read(config_fn)

    try:
        return user_config["slack"]["webhook_url"]
    except KeyError:
        err(f"Slack webhook URL not configured in {config_fn} - see documentation for details")

def parse_command_line():
    parser = argparse.ArgumentParser(
        description="Comicbot: post comics to Slack")

    parser.add_argument(
        "-f", "--force", action="store_true",
        help="Force posting the resource(s), even if stale"
    )
    parser.add_argument(
        "-l", "--loglevel", default=config.log_level, type=str,
        help=f"Log level, {config.log_level} by default"
    )
    parser.add_argument(
        "-p", "--providers", type=str, help="Comma-separated list of provider IDs to invoke"
    )

    return parser.parse_args()
    
def setup_logging(level):
    logging.setLogRecordFactory(make_log_record)
    logging.basicConfig(
        format="%(asctime)s %(levelname)7s: %(prefix)s%(message)s",
        level=getattr(logging, level.upper())
    )

def err(e):
    log_error(e)
    raise SystemExit(1)

def log_error(e):
    logging.error(re.sub(r"(^'|'$)", "", str(e)))
    
    if isinstance(e, Exception):
        log_traceback(e)
                
        if isinstance(e, requests.exceptions.HTTPError):
            log_http_error(e)

def log_traceback(e):
    tb = e.__traceback__
    summary = traceback.extract_tb(tb)
    
    for line in summary.format():
        for section in filter(lambda x: x, line.split("\n")):
            logging.debug(re.sub(r"^\s{,2}", "¦ ", section))
            
def log_http_error(e):
    try:
        rq_body = json.dumps(json.loads(e.request.body), indent=2)
    except:
        rq_body = "(no request body available or not JSON)"

    try:
        resp_body = e.response.text
    except:
        resp_body = "(no response body available)"

    logging.debug("Request body follows:")
    
    for line in rq_body.split("\n"):
        logging.debug(f"> {line}") 
        
    logging.debug("Response body follows:")
    
    for line in resp_body.split("\n"):
        logging.debug(f"< {line}") 

def main():
    args = parse_command_line()
    
    setup_logging(args.loglevel)
    
    guard = Guard()
    
    for ConcreteProvider in Provider.get_providers(args.providers):
        logging.info(f"Invoking provider \"{ConcreteProvider.id}\"")

        try:
            invoke_provider(ConcreteProvider(), guard, force=args.force)
        except Exception as e:
            log_error(e)

try:
    main()
except Exception as e:
    log_error(e)
