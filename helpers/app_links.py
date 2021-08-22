#!/usr/bin/env python3

from urllib.parse import urlparse
import json
import subprocess

DEFAULT_DAL_FILE = '/.well-known/assetlinks.json'

def get_protocol_and_domain_dict(deeplinks):
    domains = []
    for _, handlers in deeplinks.items():
        for deeplink in sorted(handlers):
            if deeplink.startswith('http'):
                domains.append(urlparse(deeplink).netloc)
    return set(domains)

def check_dal(url, sha256):
    dal = subprocess.Popen(
        'curl ' + url + DEFAULT_DAL_FILE + ' -s', shell=True, stdout=subprocess.PIPE
    ).stdout.read().decode()
    dal_json = json.loads(dal)
    for entry in dal_json:
        if "target" in entry:
            if "sha256_cert_fingerprints" in entry["target"]:
                if sha256 in entry["target"]["sha256_cert_fingerprints"]:
                    return True
    return False