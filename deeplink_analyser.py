#!/usr/bin/env python3

import helpers.adb
import helpers.get_schemes
import helpers.setup
import os

def main(manifest, strings, package, apk, verify):
    activity_handlers = helpers.get_schemes.get_schemes(strings, manifest)
    if verify:
        helpers.setup.check_device_configs(package, apk)
    for activity, handlers in activity_handlers.items():
        print("\n" + activity + "\n")
        for deeplink in sorted(handlers):
            if "http" in deeplink:
                print(deeplink)
                os.system('adb shell am start -a android.intent.action.VIEW -d ' +  deeplink + ' ' + package)
    else:
        for activity, handlers in activity_handlers.items():
            print(activity)
            print('\n'.join(f'  {h}' for h in sorted(handlers)))

if __name__ == '__main__':
    args = helpers.setup.get_parsed_args()
    if args.manifest is None or args.strings is None:
        if args.apk is None:
            print("You must specify either an APK or the manifest and strins file path")
            exit()
        else:
            helpers.setup.decompile_and_get_files(args.apk)
            apk_filename = os.path.basename(args.apk).split('.apk')[0]
            manifest_file = open(apk_filename + "/AndroidManifest.xml")
            strings_file = open(apk_filename + "/res/values/strings.xml")
            main(manifest_file, strings_file, args.package, args.apk, args.verify)
            if args.clear:
                print("Clearing decompiled directory")
                os.system("rm -rf " + dir)
    else:
        main(open(args.manifest), open(args.strings), args.package, args.apk, args.verify)