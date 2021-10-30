#!/usr/bin/env python3

from os import error
from types import resolve_bases
from helpers.apk_cert import get_sha256_cert_fingerprint
from helpers.console import write_to_console, bcolors
from urllib.parse import urlparse
import requests
import helpers.get_schemes
import helpers.console
import json

DEFAULT_ROBOTS_FILE = '/robots.txt'
DEFAULT_DAL_FILE = '/.well-known/assetlinks.json'

def get_dal(url):
    domain = urlparse(url).netloc
    res = requests.get('https://' + domain + DEFAULT_DAL_FILE)
    if res.status_code != 200:
        raise Exception('DAL should be returned with status code 200, not ' + str(res.status_code) + '.')
    if 'Content-Type' not in res.headers or 'application/json' not in res.headers['Content-Type']:
        raise Exception('DAL should be served with \"application/json\" content type.')
    return res.text

def get_relation_list_in_dal(url, sha256, package, verbose):
    try:
        dal = get_dal(url)
        if verbose:
            print(dal)
        dal_json = json.loads(dal)
        for entry in dal_json:
            if 'target' in entry:
                target = entry['target']
                if 'namespace' not in target or target['namespace'] != 'android_app':
                    continue
                if 'package_name' not in target or target['package_name'] != package:
                    continue
                if 'sha256_cert_fingerprints' not in target:
                    continue
                registered_certs = target['sha256_cert_fingerprints']
                for cert in registered_certs:
                    if cert == sha256:
                        if 'relation' in entry:
                            return entry['relation']
                        else:
                            return []
    except Exception as err:
        helpers.console.write_to_console('x ' + str(err), bcolors.FAIL)
        return None
    return None

def check_manifest_keys_for_deeplink(handlers, deeplink, cicd):
    if handlers[deeplink][helpers.get_schemes.AUTOVERIFY_KEY]:
        helpers.console.write_to_console('\n✓ includes autoverify=true', bcolors.OKGREEN)
    else:
        helpers.console.write_to_console('\nx does not include autoverify=true', bcolors.FAIL)
        if cicd:
            exit(1)
    if handlers[deeplink][helpers.get_schemes.INCLUDES_VIEW_ACTION_KEY]:
        helpers.console.write_to_console('✓ includes VIEW action', bcolors.OKGREEN)
    else:
        helpers.console.write_to_console('x does not include VIEW action', bcolors.FAIL)
        if cicd:
            exit(1)
    if handlers[deeplink][helpers.get_schemes.INCLUDES_BROWSABLE_CATEGORY_KEY]:
        helpers.console.write_to_console('✓ includes BROWSABLE category', bcolors.OKGREEN)
    else:
        helpers.console.write_to_console('x does not include BROWSABLE category', bcolors.FAIL)
        if cicd:
            exit(1)
    if handlers[deeplink][helpers.get_schemes.INCLUDES_DEFAULT_CATEGORY_KEY]:
        helpers.console.write_to_console('✓ includes DEFAULT category', bcolors.OKGREEN)
    else:
        helpers.console.write_to_console('x does not include DEFAULT category', bcolors.FAIL)
        if cicd:
            exit(1)

def check_dals(deeplinks, apk, package, verbose, cicd):
    sha256 = get_sha256_cert_fingerprint(apk)
    if sha256 is None:
        write_to_console(
            'The APK\'s signing certificate\'s SHA-256 fingerprint could not be found',
            bcolors.FAIL
        )
        exit(1)
    write_to_console(
        '\nThe APK\'s signing certificate\'s SHA-256 fingerprint is: \n' + sha256,
        bcolors.HEADER
    )
    for activity, handlers in deeplinks.items():
        write_to_console('\n' + activity + '\n', bcolors.BOLD)
        for deeplink in sorted(handlers.keys()):
            if deeplink.startswith('http'):
                print('Checking ' + deeplink)
                check_manifest_keys_for_deeplink(handlers, deeplink, cicd)
                relation_list = get_relation_list_in_dal(deeplink, sha256, package, verbose)
                if relation_list is not None:
                    helpers.console.write_to_console('✓ DAL verified\n', helpers.console.bcolors.OKGREEN)
                    print('  Relations: ')
                    for relation in relation_list:
                        if 'delegate_permission/common.handle_all_urls' in relation or 'delegate_permission/common.get_login_creds' in relation:
                            helpers.console.write_to_console('    - [Standard] ' + relation, helpers.console.bcolors.OKCYAN)
                        else:
                            helpers.console.write_to_console('    - [Custom]   ' + relation, helpers.console.bcolors.WARNING)
                else:
                    helpers.console.write_to_console('x DAL verification failed\n', helpers.console.bcolors.FAIL)
                    if cicd:
                        exit(1)
                print()
    
    print('Read more about relation strings here: https://developers.google.com/digital-asset-links/v1/relation-strings\n')
