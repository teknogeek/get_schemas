#!/usr/bin/env python3

import helpers.adb
import helpers.get_schemes
import helpers.setup
import os

def main(strings_file, manifest_file, package, apk, verify):
    activity_handlers = helpers.get_schemes.get_schemes(strings_file, manifest_file)
    if not verify:
        for activity, handlers in activity_handlers.items():
            print(activity)
            print('\n'.join(f'  {h}' for h in sorted(handlers)))
    else:
        helpers.setup.check_device_configs(package, apk)
        for activity, handlers in activity_handlers.items():
            print("\n" + activity + "\n")
            for deeplink in sorted(handlers):
                if "http" in deeplink:
                    print(deeplink)
                    os.system('adb shell am start -a android.intent.action.VIEW -d ' +  deeplink + ' ' + package)

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
            main(strings_file_path, manifest_file_path, args.package, args.apk, args.verify)
            if args.clear:
                print("Clearing decompiled directory")
                os.system("rm -rf " + dir)
    else:
        strings_file_path = open(args.strings)
        manifest_file_path = open(args.manifest)
        main(strings_file_path, manifest_file_path, args.package, args.apk, args.verify)