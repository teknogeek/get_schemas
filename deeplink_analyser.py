#!/usr/bin/env python3

import helper
import argparse
import os

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg

def list_schemes(activity_handlers):
    for activity, handlers in activity_handlers.items():
        print(activity)
        print('\n'.join(f'  {h}' for h in sorted(handlers)))

def verify_schemes(activity_handlers):
    os.system("adb kill-server")
    os.system("adb start-server")
    for activity, handlers in activity_handlers.items():
        print("\n" + activity + "\n")
        for deeplink in sorted(handlers):
            if "http" in deeplink:
                print(deeplink)
                os.system("adb shell am start -W -a android intent.action.VIEW -d " + deeplink)

def main(manifest, strings, verify, clear):
    activity_handlers = helper.get_schemes(strings, manifest)
    if verify:
        verify_schemes(activity_handlers)
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
    parser.add_argument('--verify',
                        dest='verify',
                        required=False,
                        action='store_true',
                        help='Whether or not the script should verify the App Links (default: False)')
    parser.add_argument('--clear',
                        dest='clear',
                        default=False,
                        required=False,
                        type=bool,
                        help='Whether or not the script should delete the decompiled directory after running (default: False)')
    args = parser.parse_args()
    if args.manifest is None or args.strings is None:
        if args.apk is None:
            print("You must specify either an APK or the manifest and strins file path")
            exit()
        else:
            decompile_and_get_files(args.apk)
            dir = args.apk.split(".apk")[0]
            manifest_file = open(dir + "/AndroidManifest.xml")
            strings_file = open(dir + "/res/values/strings.xml")
            main(manifest_file, strings_file, args.verify, args.clear)
    else:
        main(open(args.manifest), open(args.strings), args.verify, args.clear)