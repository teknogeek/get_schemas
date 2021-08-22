# Android "App Link Verification" Tester

Tool that helps with checking if an Android application has successfully completed the "App Link Verification" process for Android App Links.

You can see more info about this process [here](https://developer.android.com/training/app-links/verify-site-associations).

## How does it work?

This tool supports 6 operation modes:

* `list-all`: simple enumeration, lists all deep links registered by the application regardless of format
* `list-applinks`: lists all Android App Links registered by the application
* `check-dals`: fetches the DAL file under `/.well-known/assetlinks.json` for each protocol + domain combination used for a registered App Link, as specified [here](https://developer.android.com/training/app-links/verify-site-associations)
* `adb-test`: uses `adb` to open all of the application's App Links and allows you to check if they're being automatically opened by the intended application
* `build-poc`: creates an HTML page with links to all of the registered Android App Links, in order to simplify the process of testing their verification process
* `launch-poc`: sends the HTML page created on the previus mode to a connected device (via `adb`), and opens it with Chrome

## Installation

```
python3 -m pip install -r requirements.txt
```

**Important Notes**

1. If you want to provide an `.apk` file instead of the `AndroidManifest.xml` and `strings.xml`, then you need to have [apktool](https://ibotpeaches.github.io/Apktool/) installed and accessible on the `$PATH`.
2. If you want to use the `adb-test` or `launch-poc` operation modes, you need to have [adb](https://developer.android.com/studio/command-line/adb) installed and accessible on the `$PATH`.

## Usage

```
~ python3 Android-Deep-Link-Analyser/deeplink_analyser.py --help
usage: deeplink_analyser.py [-h] [-apk FILE] [-m FILE] [-s FILE] -op OP
                            [-p PACKAGE] [--clear]

optional arguments:
  -h, --help            show this help message and exit
  -apk FILE             Path to the APK
  -m FILE, --manifest FILE
                        Path to the AndroidManifest.xml file
  -s FILE, --strings FILE
                        Path to the strings.xml file
  -op OP, --operation-mode OP
                        Operation mode: "list-all", "list-applinks", "check-
                        dals", "build-poc", "launch-poc", "adb-test".
  -p PACKAGE, --package PACKAGE
                        Package identifier, e.g.: com.myorg.appname. Required
                        for any operation that interacts with the device
  --clear               Whether or not the script should delete the decompiled
                        directory after running (default: False)
```

## Examples

### Use an APK to list all registered deep links

![Screenshot 2021-08-22 at 16 43 03](https://user-images.githubusercontent.com/39055313/130361357-cfdfd212-88b7-4f7e-8c2f-64b28cf5e01b.png)

### Use the manifest+strings file to list all registered Android App links

![Screenshot 2021-08-22 at 16 57 25](https://user-images.githubusercontent.com/39055313/130361750-a6688560-35b5-4a7b-a2cc-a803ca78c039.png)

### Use an (already decompiled) APK to check for DALs for all App Links

![Screenshot 2021-08-22 at 16 43 53](https://user-images.githubusercontent.com/39055313/130361397-e7bd5323-42f2-4a79-a809-5c1bd8049f8a.png)

### Use an (already decompiled) APK to automatically test all of the App Links using ADB

![Screenshot 2021-08-22 at 16 58 38](https://user-images.githubusercontent.com/39055313/130361770-745db650-0973-489e-bbb5-968a42607fcb.png)

### Use the manifest and the strings file to create a POC locally

```
~ python3 Android-Deep-Link-Analyser/deeplink_analyser.py \
	-op build-poc \
	-m com.twitter.android_2021-08-16/AndroidManifest.xml \
	-s com.twitter.android_2021-08-16/res/values/strings.xml 

Finished writing POC to local file poc.html
```

### Use an (already decompiled) APK to send the POC to the device and open it with Chrome**

```
~ python3 Android-Deep-Link-Analyser/deeplink_analyser.py \
	-op launch-poc \
	-p com.twitter.android \
	-apk com.twitter.android_2021-08-16.apk

Destination directory (/Users/inesmartins/Desktop/com.twitter.android_2021-08-16) already exists. Use -f switch if you want to overwrite it.
Finished writing POC to local file poc.html
./poc.html: 1 file pushed, 0 skipped. 1.2 MB/s (1010 bytes in 0.001s)
Starting: Intent { act=android.intent.action.VIEW dat=file:///sdcard/poc.html cmp=com.android.chrome/com.google.android.apps.chrome.Main }```
```

As a result, your Android device should display something like this:

![Screenshot_20210820-210127](https://user-images.githubusercontent.com/39055313/130288058-625056b5-c569-4597-b852-c911de1d4704.png)

Then, you can manually click on each of the links: **if the OS prompts you to choose between Chrome and one or more apps, then the App Link Verification process is not correctly implemented**.
