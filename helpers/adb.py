#!/usr/bin/env python3

from typing import List
import helpers.console
import subprocess
import os

CHROME_PACKAGE = 'com.android.chrome/com.google.android.apps.chrome.Main'

def get_adb_devices(adbpath):
    lines = subprocess.check_output([adbpath, 'devices']).splitlines()
    devices = []
    for line in lines:
        if line.decode().endswith('\tdevice'):
            devices.append(line.decode().split('\t')[0])
    return set(devices)

def package_is_installed(package, adbpath):
    args = [adbpath]
    args.extend(['shell', 'pm list packages -f'])
    lines = subprocess.check_output(args).splitlines()
    for line in lines:
        package_name = line.decode().split('apk=')[1]
        if package_name == package:
            return True
    return False

def check_device_requirements(package, apk, adbpath="adb"):
    devices = get_adb_devices(adbpath)
    if len(devices) == 0:
        helpers.console.write_to_console('No devices detected by adb', helpers.console.bcolors.WARNING)
        exit()
    if not package_is_installed(package, adbpath="adb"):
        if apk is None:
            error_msg = 'Package is not installed and APK was not specified ...'
            helpers.console.write_to_console(error_msg, helpers.console.bcolors.WARNING)
            exit()
        else:
            error_msg = 'Package is not installed ...'
            helpers.console.write_to_console(error_msg, helpers.console.bcolors.OKBLUE)
            os.system("adb install " + apk)

def write_file_to_device(file, dest, adbpath="adb"):
    os.system(adbpath + ' push ./' + file + ' ' + dest)

def open_file_in_device_with_chrome(filepath, adbpath="adb"):
    os.system(adbpath + ' shell am start -n ' + CHROME_PACKAGE + ' -a android.intent.action.VIEW -d "file://' + filepath + '"')