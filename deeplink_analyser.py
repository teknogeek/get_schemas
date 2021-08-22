#!/usr/bin/env python3

from helpers.console import write_to_console
import helpers.setup
import helpers.adb
import helpers.get_schemes
import helpers.poc
import helpers.console
import helpers.app_links
import os

DEFAULT_STRINGS_FILE = '/res/values/strings.xml'
DEFAULT_MANIFEST_FILE = '/AndroidManifest.xml'
POC_FILENAME = 'poc.html'
POC_DEST_DIR = '/sdcard/'
CHROME_PACKAGE = 'com.android.chrome/com.google.android.apps.chrome.Main'

def main(strings_file, manifest_file, package, apk, op):
    deeplinks = helpers.get_schemes.get_schemes(strings_file, manifest_file)

    if op == helpers.setup.OP_LIST_ALL or op == helpers.setup.OP_LIST_APPLINKS:
        for activity, handlers in deeplinks.items():
            print(activity)
            if op == helpers.setup.OP_LIST_ALL:
                print('\n'.join(f'  {deeplink}' for deeplink in sorted(handlers)))
            if op == helpers.setup.OP_LIST_APPLINKS:
                print('\n'.join(f'  {deeplink}' for deeplink in sorted(handlers) if deeplink.startswith('http')))

    if op == helpers.setup.OP_CHECK_DALS:
        dict = helpers.app_links.get_protocol_and_domain_dict(deeplinks)
        for domain in dict:
            for protocol in dict.get(domain):
                url = protocol + '://' + domain
                helpers.console.write_to_console('\nChecking DAL for ' + url, color=helpers.console.bcolors.OKBLUE)
                os.system('curl ' + url + '/.well-known/assetlinks.json')

    if op == helpers.setup.OP_BUILD_POC or op == helpers.setup.OP_LAUNCH_POC:
        helpers.adb.check_device_configs(package, apk)
        helpers.poc.write_deeplinks_to_file(deeplinks, POC_FILENAME)
        print('Finished writing POC to local file ' + POC_FILENAME)

    if op == helpers.setup.OP_LAUNCH_POC:
        os.system('adb push ./' + POC_FILENAME + ' ' + POC_DEST_DIR)
        os.system('adb shell am start -n ' + CHROME_PACKAGE + ' -a android.intent.action.VIEW -d "file://' + POC_DEST_DIR + POC_FILENAME + '"')

    if op == helpers.setup.OP_TEST_WITH_ADB:
        helpers.adb.check_device_configs(package, apk)
        for activity, handlers in deeplinks.items():
            write_to_console('\nActivity: ' + activity + '\n', helpers.console.bcolors.BOLD)
            for deeplink in handlers:
                if deeplink.startswith('http'):
                    write_to_console('\nTesting deeplink: ' + deeplink, helpers.console.bcolors.OKGREEN)
                    os.system('adb shell am start -a android.intent.action.VIEW -d "' + deeplink + '"')
                    input("Press 'Enter' to test next App Link ...")

if __name__ == '__main__':
    args = helpers.setup.get_parsed_args()
    if args.apk is not None:
        helpers.setup.decompile_apk(args.apk)
        apk_filename = os.path.basename(args.apk).split('.apk')[0]
        strings_file_path = open(apk_filename + DEFAULT_STRINGS_FILE)
        manifest_file_path = open(apk_filename + DEFAULT_MANIFEST_FILE)
        main(strings_file_path, manifest_file_path, args.package, args.apk, args.op)
        if args.clear:
            print('Clearing decompiled directory')
            os.system('rm -rf ' + dir)
    else:
        strings_file_path = open(args.strings)
        manifest_file_path = open(args.manifest)
        main(strings_file_path, manifest_file_path, args.package, args.apk, args.op)