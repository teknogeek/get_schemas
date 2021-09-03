#!/usr/bin/env python3

from helpers.apk_cert import get_sha256_cert_fingerprint
from helpers.console import write_to_console, bcolors
from urllib.parse import urlparse
import helpers.get_schemes
import helpers.console
import json
import subprocess

DEFAULT_DAL_FILE = '/.well-known/assetlinks.json'

def get_relation_in_dal(url, sha256, package, verbose):
    domain = urlparse(url).netloc
    dal = subprocess.Popen(
        'curl https://' + domain + DEFAULT_DAL_FILE + ' -s', shell=True, stdout=subprocess.PIPE
    ).stdout.read().decode()
    if verbose:
        print(dal)
    try:
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
    except:
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
                relation = get_relation_in_dal(deeplink, sha256, package, verbose)
                if relation is not None:
                    helpers.console.write_to_console('✓ DAL verified', helpers.console.bcolors.OKGREEN)
                    helpers.console.write_to_console('  relation: ' + str(relation) + '\n', helpers.console.bcolors.OKCYAN)
                else:
                    helpers.console.write_to_console('x DAL verification failed\n', helpers.console.bcolors.FAIL)
                    if cicd:
                        exit(1)
