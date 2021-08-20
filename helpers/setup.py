import helpers.get_schemes
import helpers.adb
import argparse
import os

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg

def get_parsed_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-apk',
                        dest='apk',
                        required=False,
                        metavar="FILE", 
    					type=lambda x: helpers.setup.is_valid_file(parser, x),
                        help='Path to the APK')
    parser.add_argument('-p', '--package',
                        dest="package",
                        required=True,
    					type=str,
                        help='Package identifier, e.g.: com.myorg.appname')
    parser.add_argument('-m', '--manifest', 
                        dest="manifest",
                        required=False,
                        metavar="FILE", 
    					type=lambda x: helpers.setup.is_valid_file(parser, x),
                        help='Path to the AndroidManifest.xml file')
    parser.add_argument('-s', '--strings',
                        dest="strings",
                        required=False,
                        metavar="FILE", 
    					type=lambda x: helpers.setup.is_valid_file(parser, x),
                        help='Path to the strings.xml file')
    parser.add_argument('-op', '--operation-mode',
                        dest='op',
                        required=True,
                        type=str,
                        help='Operation mode: can be "list-all", "list-applinks", "build-poc" or "launch-poc"')
    parser.add_argument('--clear',
                        dest='clear',
                        required=False,
                        action='store_true',
                        help='Whether or not the script should delete the decompiled directory after running (default: False)')
    return parser.parse_args()

def decompile_apk(apk):
    os.system("apktool d " + apk)
