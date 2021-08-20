# Android Deep Link Analyser

Tool that helps with enumerating deep links in Android, and checking if the App Links are correctly verified.

You can read more about App Link Verification [here](https://developer.android.com/training/app-links/verify-site-associations).

Supports 4 operation modes:

* `list-all`: lists all deeplink URIs registered by the application, regardless of format
* `list-applinks`: lists all Android App Links registered by the application
* `build-poc`: creates an HTML page with links to all the registered Android App Links in order to simplify the process of testing their verification process
* `launch-poc`: sends the HTML page to a connected device, and opens it with Chrome

### Installation

```
python3 -m pip install -r requirements.txt
```

**Important Notes**

If you want to provide an `.apk` file instead of the `AndroidManifest.xml` and `strings.xml`, then you need to have [apktool](https://ibotpeaches.github.io/Apktool/) installed and accessible on the `$PATH`.

If you want to use the `launch-poc` operation mode, you need to have [adb](https://developer.android.com/studio/command-line/adb) installed and accessible on the `$PATH`.

### Usage

```
~ python3 deeplink_analyser.py --help
usage: deeplink_analyser.py [-h] [-apk FILE] -p PACKAGE [-m FILE] [-s FILE]
                            -op OP [--clear]

optional arguments:
  -h, --help            show this help message and exit
  -apk FILE             Path to the APK
  -p PACKAGE, --package PACKAGE
                        Package identifier, e.g.: com.myorg.appname
  -m FILE, --manifest FILE
                        Path to the AndroidManifest.xml file
  -s FILE, --strings FILE
                        Path to the strings.xml file
  -op OP, --operation-mode OP
                        Operation mode: can be "list-all", "list-applinks", "build-poc" or "launch-poc"
  --clear               Whether or not the script should delete the decompiled
                        directory after running (default: False)
```

### Examples

**Launching the POC using an APK file**

```
~ python3 Android-Deep-Link-Analyser/deeplink_analyser.py
    -op launch-poc
    -p com.twitter.android
    -apk com.twitter.android_2021-08-16.apk
I: Using Apktool 2.5.0 on com.twitter.android_2021-08-16.apk
I: Loading resource table...
I: Decoding AndroidManifest.xml with resources...
I: Loading resource table from file: /Users/inesmartins/Library/apktool/framework/1.apk
I: Regular manifest package...
I: Decoding file-resources...
I: Decoding values */* XMLs...
I: Baksmaling classes.dex...
I: Baksmaling classes2.dex...
I: Baksmaling classes3.dex...
I: Baksmaling classes4.dex...
I: Baksmaling classes5.dex...
I: Baksmaling classes6.dex...
I: Baksmaling classes7.dex...
I: Copying assets and libs...
I: Copying unknown files...
I: Copying original files...
I: Copying META-INF/services directory
Finished writing POC to local file poc.html
Package is not installed ...
Performing Push Install
com.twitter.android_2021-08-16.apk: 1 .... 6.3 MB/s (89641501 bytes in 13.558s)
	pkg: /data/local/tmp/com.twitter.android_2021-08-16.apk

Success
./poc.html: 1 file pushed, 0 skipped. 2.4 MB/s (1010 bytes in 0.000s)
Starting: Intent { act=android.intent.action.VIEW dat=file:///sdcard/poc.html cmp=com.android.chrome/com.google.android.apps.chrome.Main }
```

**Building the POC using a Manifest and strings file**

```
~ python3 deeplink_analyser.py 
    -op build-poc
    -p com.myorg.appname
    -m com.myorg.appname_2021-08-10/AndroidManifest.xml
    -s com.myorg.appname_2021-08-10/res/values/strings.xml

Finished writing POC to local file poc.html
```