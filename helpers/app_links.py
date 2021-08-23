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


def get_relation_in_dal(url, sha256, package, verbose):
    dal = subprocess.Popen(
        'curl ' + url + DEFAULT_DAL_FILE + ' -s', shell=True, stdout=subprocess.PIPE
    ).stdout.read().decode()
    if verbose:
        print(dal)
    try:
        dal_json = json.loads(dal)
        for entry in dal_json:
            if "target" in entry:
                if "package_name" in entry["target"] and "sha256_cert_fingerprints" in entry["target"]:
                    if package == entry["target"]["package_name"] and sha256 in entry["target"]["sha256_cert_fingerprints"]:
                        if "relation" in entry:
                            return entry["relation"]
                        else:
                            return []
    except:
        return None
    return None


def check_dal(url, sha256, package, verbose):
    helpers.console.write_to_console(
        '\nChecking DAL for ' + url + '\n', 
        color=helpers.console.bcolors.BOLD
    )
    relation = get_relation_in_dal(url, sha256, package, verbose)
    if relation is not None:
        helpers.console.write_to_console(
            'Certificate\'s SHA-256 is set for package "' + package + '" inside DAL.\n', 
            helpers.console.bcolors.OKGREEN
        )
        helpers.console.write_to_console(
            'Relation: ' + str(relation), 
            helpers.console.bcolors.OKCYAN
        )
    else:
        helpers.console.write_to_console(
            'Certificate\'s SHA-256 was not found for package "' + package + '" inside DAL.', 
            helpers.console.bcolors.FAIL
        )
