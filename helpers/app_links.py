#!/usr/bin/env python3

from urllib.parse import urlparse

def get_protocol_and_domain_dict(deeplinks):
    domains = []
    for _, handlers in deeplinks.items():
        for deeplink in sorted(handlers):
            if deeplink.startswith('http'):
                domains.append(urlparse(deeplink).netloc)
    return set(domains)