#!/usr/bin/env python3

from re import A
from deeplink_analyser import APKTOOL_PATH
import helpers.get_schemes
import helpers.adb
import helpers.console
import argparse
import os

OP_LIST_ALL = 'list-all'
OP_LIST_APPLINKS = 'list-applinks'
OP_VERIFY_APPLINKS = 'verify-applinks'
OP_BUILD_POC = 'build-poc'
OP_LAUNCH_POC = 'launch-poc'
OP_TEST_WITH_ADB = 'adb-test'
OP_MODES = [OP_LIST_ALL, OP_LIST_APPLINKS, OP_VERIFY_APPLINKS, OP_BUILD_POC, OP_LAUNCH_POC, OP_TEST_WITH_ADB]

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
                        help='Path to the APK (required for `verify-applinks` operation mode)')
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
                        help='Operation mode: "' + '", "'.join(OP_MODES) + '".')
    parser.add_argument('-p', '--package',
                        dest="package",
                        required=False,
    					type=str,
                        help='Package identifier, e.g.: "com.myorg.appname" (required for some operation modes)')
    parser.add_argument('-v', '--verbose',
                        dest='verbose',
                        required=False,
                        action='store_true',
                        help='Verbose mode')
    parser.add_argument('-c', '--clear',
                        dest='clear',
                        required=False,
                        action='store_true',
                        help='Whether or not the script should delete the decompiled directory after running (default: False)')
    args = parser.parse_args()
    if args.manifest is None or args.strings is None:
        if args.apk is None:
            error_msg = 'You must specify either an APK or a manifest and strings file path'
            helpers.console.write_to_console(error_msg, helpers.console.bcolors.FAIL)
            exit()
    elif args.op == OP_VERIFY_APPLINKS:
        error_msg = 'You need to use the -apk option when using the "verify-applinks" operation mode'
        helpers.console.write_to_console(error_msg, helpers.console.bcolors.FAIL)
        exit()
    if args.op not in OP_MODES:
        error_msg = 'The specified operation mode is not supported.'
        error_msg += '\nSupported operation modes: "' + '", "'.join(OP_MODES) + '".'
        helpers.console.write_to_console(error_msg, helpers.console.bcolors.FAIL)
        exit()
    if args.op == OP_TEST_WITH_ADB or args.op == OP_LAUNCH_POC or args.op == OP_VERIFY_APPLINKS:
        if args.package is None:
            error_msg = 'You must specify the package id in order to use this operation mode'
            helpers.console.write_to_console(error_msg, helpers.console.bcolors.FAIL)
            exit()
    return args

def decompile_apk(apk):
    os.system(APKTOOL_PATH + ' d ' + apk)
