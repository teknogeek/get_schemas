#!/usr/bin/env python3

from urllib.parse import urlparse
import helpers.console
import json
import subprocess

DEFAULT_DAL_FILE = '/.well-known/assetlinks.json'

def get_domains_for_applinks(deeplinks):
    domains = []
    for _, handlers in deeplinks.items():
        for deeplink in sorted(handlers):
            if deeplink.startswith('http'):
                domains.append(urlparse(deeplink).netloc)
    return set(domains)


def sha256_is_in_dal(url, sha256, verbose):
    dal = subprocess.Popen(
        'curl ' + url + DEFAULT_DAL_FILE + ' -s', shell=True, stdout=subprocess.PIPE
    ).stdout.read().decode()
    if verbose:
        print(dal)
    try:
        dal_json = json.loads(dal)
        for entry in dal_json:
            if "target" in entry:
                if "sha256_cert_fingerprints" in entry["target"]:
                    if sha256 in entry["target"]["sha256_cert_fingerprints"]:
                        return True
    except:
        return False
    return False


def check_dal(url, sha256, verbose):
    helpers.console.write_to_console(
        '\nChecking DAL for ' + url, 
        color=helpers.console.bcolors.OKBLUE
    )
    if sha256_is_in_dal(url, sha256, verbose):
        helpers.console.write_to_console(
            'Certificate\'s SHA-256 was found inside DAL.', 
            helpers.console.bcolors.OKGREEN
        )
    else:
        helpers.console.write_to_console(
            'Certificate\'s SHA-256 was not found inside DAL.', 
            helpers.console.bcolors.FAIL
        )
