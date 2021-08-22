#!/usr/bin/env python3

from urllib.parse import urlparse

def get_protocol_and_domain_dict(deeplinks):
    domains = {}
    for _, handlers in deeplinks.items():
        for deeplink in sorted(handlers):
            if deeplink.startswith('http'):
                is_https = deeplink.startswith('http')
                domain = urlparse(deeplink).netloc
                if domains.get(domain) is None:                  
                    if is_https:
                        domains[domain] = ['https']
                    else:
                        domains[domain] = ['http']
                else:
                    if is_https and 'https' not in domains.get(domain):
                        domains[domain].append('https')
                    elif 'http' not in domains.get(domain):
                        domains[domain].append('http')
    return domains