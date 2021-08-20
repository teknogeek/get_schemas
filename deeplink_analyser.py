#!/usr/bin/env python3

import helpers.setup
import helpers.adb
import helpers.get_schemes
import helpers.poc
import os

POC_FILENAME = 'poc.html'
CHROME_PACKAGE = 'com.android.chrome/com.google.android.apps.chrome.Main'

def main(strings_file, manifest_file, package, apk, op):
    deeplinks = helpers.get_schemes.get_schemes(strings_file, manifest_file)

    if op == "list-all" or op == "list-applinks":
        for activity, handlers in deeplinks.items():
            print(activity)
            if op == "list-all":
                print('\n'.join(f'  {h}' for h in sorted(handlers)))
            if op == "list-applinks":
                print('\n'.join(f'  {h}' for h in sorted(handlers) if h.startswith('http')))

    if op == "build-poc" or op == "launch-poc":
        helpers.poc.write_deeplinks_to_file(deeplinks, POC_FILENAME)
        print("Finished writing POC to local file " + POC_FILENAME)

    if op == "launch-poc":
        helpers.adb.check_device_configs(package, apk)
        os.system("adb push ./" + POC_FILENAME + " /sdcard/")
        os.system("adb shell am start -n " + CHROME_PACKAGE + " -a android.intent.action.VIEW -d 'file:///sdcard/" + POC_FILENAME + "'")

if __name__ == '__main__':
    args = helpers.setup.get_parsed_args()
    if args.manifest is None or args.strings is None:
        if args.apk is None:
            print("You must specify either an APK or the manifest and strings file path")
            exit()
        else:
            helpers.setup.decompile_apk(args.apk)
            apk_filename = os.path.basename(args.apk).split('.apk')[0]
            strings_file_path = open(apk_filename + "/res/values/strings.xml")
            manifest_file_path = open(apk_filename + "/AndroidManifest.xml")
            main(strings_file_path, manifest_file_path, args.package, args.apk, args.op)
            if args.clear:
                print("Clearing decompiled directory")
                os.system("rm -rf " + dir)
    else:
        strings_file_path = open(args.strings)
        manifest_file_path = open(args.manifest)
        main(strings_file_path, manifest_file_path, args.package, args.apk, args.op)