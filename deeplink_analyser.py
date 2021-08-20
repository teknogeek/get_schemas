#!/usr/bin/env python3

import get_schemes_helper
import adb_helper
import argparse
import os
import subprocess

ADB_PATH="adb"

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg

def list_schemes(activity_handlers):
    for activity, handlers in activity_handlers.items():
        print(activity)
        print('\n'.join(f'  {h}' for h in sorted(handlers)))

def verify_schemes(activity_handlers, package, apk):
    devices = adb_helper.adbdevices()
    if len(devices) == 0:
        print("No devices were detected by adb")
        exit()
    if not adb_helper.package_is_installed(package):
        if apk is None:
            print("Package is not installed and APK was not specified ...")
        else:
            print("Package is not installed ...")
            os.system("adb install " + apk)

    for activity, handlers in activity_handlers.items():
        print("\n" + activity + "\n")
        for deeplink in sorted(handlers):
            if "http" in deeplink:
                print(deeplink)
                os.system("adb shell am start -W -a android intent.action.VIEW -d " + deeplink)

def main(manifest, strings, package, apk, verify):
    activity_handlers = get_schemes_helper.get_schemes(strings, manifest)
    if verify:
        verify_schemes(activity_handlers, package, apk)
    else:
        list_schemes(activity_handlers)

def decompile_and_get_files(apk):
    os.system("apktool d " + apk)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-apk',
                        dest='apk',
                        required=False,
                        metavar="FILE", 
    					type=lambda x: is_valid_file(parser, x),
                        help='Path to the APK')
    parser.add_argument('-m', '--manifest', 
                        dest="manifest",
                        required=False,
                        metavar="FILE", 
    					type=lambda x: is_valid_file(parser, x),
                        help='Path to the AndroidManifest.xml file')
    parser.add_argument('-s', '--strings',
                        dest="strings",
                        required=False,
                        metavar="FILE", 
    					type=lambda x: is_valid_file(parser, x),
                        help='Path to the strings.xml file')
    parser.add_argument('-p', '--package',
                        dest="package",
                        required=False,
    					type=str,
                        help='Package name')
    parser.add_argument('--verify',
                        dest='verify',
                        required=False,
                        action='store_true',
                        help='Whether or not the script should verify the App Links (default: False)')
    parser.add_argument('--clear',
                        dest='clear',
                        required=False,
                        action='store_true',
                        help='Whether or not the script should delete the decompiled directory after running (default: False)')
    args = parser.parse_args()
    if args.manifest is None or args.strings is None:
        if args.apk is None:
            print("You must specify either an APK or the manifest and strins file path")
            exit()
        else:
            decompile_and_get_files(args.apk)
            package_name = os.path.basename(args.apk).split('.apk')[0]
            manifest_file = open(package_name + "/AndroidManifest.xml")
            strings_file = open(package_name + "/res/values/strings.xml")
            main(manifest_file, strings_file, package_name, args.apk, args.verify)
            if args.clear:
                print("Clearing decompiled directory")
                os.system("rm -rf " + dir)

    else:
        main(open(args.manifest), open(args.strings), args.package, args.apk, args.verify)