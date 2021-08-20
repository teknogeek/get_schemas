#!/usr/bin/env python3

from typing import List
import subprocess
import os

ADB_PATH="adb"

def adbdevices(adbpath=ADB_PATH):
    lines = subprocess.check_output([adbpath, 'devices']).splitlines()
    devices = []
    for line in lines:
        if line.decode().endswith('\tdevice'):
            devices.append(line.decode().split('\t')[0])
    return set(devices)

def package_is_installed(package):
    lines = adbshell('pm list packages -f').splitlines()
    for line in lines:
        package_name = line.decode().split('apk=')[1]
        if package_name == package:
            return True
    return False

def check_device_configs(package, apk):
    devices = adbdevices()
    if len(devices) == 0:
        print("No devices were detected by adb")
        exit()
    if not package_is_installed(package):
        if apk is None:
            print("Package is not installed and APK was not specified ...")
        else:
            print("Package is not installed ...")
            os.system("adb install " + apk)

def adbshell(command, serial=None, adbpath=ADB_PATH):
    args = [adbpath]
    if serial is not None:
        args.extend(['-s', serial])
    args.extend(['shell', command])
    return subprocess.check_output(args)
