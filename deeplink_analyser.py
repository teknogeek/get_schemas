#!/usr/bin/env python3

from helpers.console import write_to_console
import helpers.setup
import helpers.adb
import helpers.get_schemes
import helpers.poc
import helpers.console
import helpers.app_links
import os
import subprocess

APKTOOL_PATH = 'apktool'
ADB_PATH = 'adb'
KEYTOOL_PATH = 'keytool'
DEFAULT_DAL_FILE = '/.well-known/assetlinks.json'
DEFAULT_STRINGS_FILE = '/res/values/strings.xml'
DEFAULT_MANIFEST_FILE = '/AndroidManifest.xml'
POC_FILENAME = 'poc.html'
POC_DEST_DIR = '/sdcard/'

def main(strings_file, manifest_file, package, apk, op):
    deeplinks = helpers.get_schemes.get_schemes(strings_file, manifest_file)

    if op == helpers.setup.OP_LIST_ALL or op == helpers.setup.OP_LIST_APPLINKS:
        for activity, handlers in deeplinks.items():
            helpers.console.write_to_console('\n' + activity + '\n', helpers.console.bcolors.BOLD)
            if op == helpers.setup.OP_LIST_ALL:
                helpers.console.write_to_console(
                    '\n'.join(f'  {deeplink}' for deeplink in sorted(handlers)), 
                    helpers.console.bcolors.OKGREEN
                )
            if op == helpers.setup.OP_LIST_APPLINKS:
                helpers.console.write_to_console(
                    '\n'.join(f'  {deeplink}' for deeplink in sorted(handlers) if deeplink.startswith('http')), 
                    helpers.console.bcolors.OKGREEN
                )
    
    if op == helpers.setup.OP_CHECK_DALS:
        apk_cert = subprocess.Popen(
            KEYTOOL_PATH + ' -printcert -jarfile ' + apk, shell=True, stdout=subprocess.PIPE
        ).stdout.read().decode()
        sha256 = apk_cert.split('SHA256: ')[1].split('\n')[0]
        dict = helpers.app_links.get_protocol_and_domain_dict(deeplinks)
        for domain in dict:
            for protocol in dict.get(domain):
                url = protocol + '://' + domain
                helpers.console.write_to_console('\nChecking DAL for ' + url, color=helpers.console.bcolors.OKBLUE)
                dal = subprocess.Popen(
                    'curl ' + url + DEFAULT_DAL_FILE + ' -s', shell=True, stdout=subprocess.PIPE
                ).stdout.read().decode()
                if sha256 in dal:
                    helpers.console.write_to_console('Certificate\'s SHA-256 was found inside DAL.', helpers.console.bcolors.OKGREEN)
                else:
                    helpers.console.write_to_console('Certificate\'s SHA-256 was not found inside DAL.', helpers.console.bcolors.FAIL)
                if args.verbose:
                    print(dal)

    if op == helpers.setup.OP_BUILD_POC or op == helpers.setup.OP_LAUNCH_POC:
        helpers.poc.write_deeplinks_to_file(deeplinks, POC_FILENAME)
        helpers.console.write_to_console(
            'Finished writing POC to local file ' + POC_FILENAME, 
            helpers.console.bcolors.OKGREEN
        )

    if op == helpers.setup.OP_LAUNCH_POC:
        helpers.adb.check_device_requirements(package, apk, ADB_PATH)
        helpers.adb.write_file_to_device(POC_FILENAME, POC_DEST_DIR)
        helpers.adb.open_file_in_device_with_chrome(POC_DEST_DIR + POC_FILENAME)

    if op == helpers.setup.OP_TEST_WITH_ADB:
        helpers.adb.check_device_requirements(package, apk, ADB_PATH)
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