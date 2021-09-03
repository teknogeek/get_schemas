# Android "App Link Verification" Tester

Tool that helps with checking if an Android application has successfully completed the "App Link Verification" process for Android App Links.

You can see more info about this process [here](https://developer.android.com/training/app-links/verify-site-associations).

## How does it work?

This tool supports 6 operation modes:

* `list-all`: simple enumeration, lists all deep links registered by the application regardless of format
* `list-applinks`: lists all Android App Links registered by the application
* `verify-applinks`: for each App Link, displays checklist with each of the necessary steps for verification, indicates if they've been completed successfully
* `adb-test`: uses `adb` to open all of the application's App Links and allows you to check if they're being automatically opened by the intended application
* `build-poc`: creates an HTML page with links to all of the registered Android App Links, in order to simplify the process of testing their verification process
* `launch-poc`: sends the HTML page created on the previus mode to a connected device (via `adb`), and opens it with Chrome

It also supports 3 additional flags:

* `clear`: removes the decompiled directory after execution
* `verbose`: prints additional information about the execution
* `ci-cd`: ideal for running in CI/CD pipelines, exits with `1` if any of the App Links are not correctly verified; automatically runs with `clear`and `verbose` flags

## Installation

```
python3 -m pip install -r requirements.txt
```

**Important Notes**

1. If you want to provide an `.apk` file instead of the `AndroidManifest.xml` and `strings.xml`, then you need to have [apktool](https://ibotpeaches.github.io/Apktool/) installed and accessible on the `$PATH`;
2. If you want to use the `adb-test` or `launch-poc` operation modes, you need to have [adb](https://developer.android.com/studio/command-line/adb) installed and accessible on the `$PATH`;
3. If you want to use the `verify-applinks` operation mode or if you want to be able to install the package on the device, you must use the `-apk` option instead of the manifest+strings file combination.
4. If you want to use the `verify-applinks` operation mode, you need to have [keytool](https://docs.oracle.com/javase/7/docs/technotes/tools/windows/keytool.html) installed and accessible on the `$PATH`;
5. If you want to use the `adb-test`, `launch-poc` or `verify-applinks` operation modes you must specify the `-p` option.

## Usage

```
~ python3 Android-Deep-Link-Analyser/deeplink_analyser.py --help
usage: deeplink_analyser.py [-h] [-apk FILE] [-m FILE] [-s FILE] -op OP
                            [-p PACKAGE] [-v] [-c]

optional arguments:
  -h, --help            show this help message and exit
  -apk FILE             Path to the APK (required for `verify-applinks`
                        operation mode)
  -m FILE, --manifest FILE
                        Path to the AndroidManifest.xml file
  -s FILE, --strings FILE
                        Path to the strings.xml file
  -op OP, --operation-mode OP
                        Operation mode: "list-all", "list-applinks", "verify-
                        applinks", "build-poc", "launch-poc", "adb-test".
  -p PACKAGE, --package PACKAGE
                        Package identifier, e.g.: "com.myorg.appname"
                        (required for some operation modes)
  -v, --verbose         Verbose mode
  -c, --clear           Whether or not the script should delete the decompiled
                        directory after running (default: False)
```

## Examples

### Use an APK to list all registered deep links

```
~ python3 Android-Deep-Link-Analyser/deeplinks_analyser.py \
-op list-all \
-apk <path-to-apk>
```

### Use the manifest+strings file to list all registered Android App links

```
~ python3 Android-Deep-Link-Analyser/deeplinks_analyser.py \
-op list-applinks \
-m <path-to-android-manifest> \
-s <path-to-strings-file>
```

### Use an APK to check for DALs for all App Links

```
~ python3 Android-Deep-Link-Analyser/deeplinks_analyser.py \
-op verify-applinks \
-apk <path-to-apk> \
-p <package-name>
```

Note that you can also specify the `-v` flag to print the entire DAL file.

An example output for the Twitter Android app would be:

![Screenshot 2021-09-03 at 13 38 57](https://user-images.githubusercontent.com/39055313/132006669-b7653b92-5c80-414c-baa9-e0717bf5bc0e.png)

### Use an APK to automatically test all of the App Links using ADB

```
~ python3 Android-Deep-Link-Analyser/deeplinks_analyser.py \
-op adb-test \
-apk <path-to-apk> \
-p <package-name>
```

Note that the package was not installed on the phone previously, so the script installed the APK using `adb`.

### Use the manifest+strings file to create a local POC

```
~ python3 Android-Deep-Link-Analyser/deeplinks_analyser.py \
-op build-poc \
-m <path-to-android-manifest> \
-s <path-to-strings-file>
```

### Use an APK to send the POC to the device via adb

```
~ python3 Android-Deep-Link-Analyser/deeplinks_analyser.py \
-op launch-poc \
-apk <path-to-apk> \
-p <package-name>
```

As a result, your Android device should display something like this:

![Screenshot_20210820-210127](https://user-images.githubusercontent.com/39055313/130288058-625056b5-c569-4597-b852-c911de1d4704.png)

Then, you can manually click on each of the links: **if the OS prompts you to choose between Chrome and one or more apps, then the App Link Verification process is not correctly implemented**.
