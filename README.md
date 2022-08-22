# get_schemas

Pretty straightforward, just gets all the URL schemas and the corresponding activities and prints them all out.

You're going to want to decompile the app with `apktool` before running this so that you have a decoded copy of:

- AndroidManifest.xml
- res/values/strings.xml

Both of these files are required for this tool to work as it substitutes any `@string/x_y_z` values.

## Requirements
- Python 3.7+

## Installation

```
$ pip3 install -r requirements.txt
```

## Usage

```
$ python3 get_schemas.py -h
usage: get_schemas.py [-h] [-m MANIFEST] [-s STRINGS]

optional arguments:
  -h, --help            show this help message and exit
  -m MANIFEST, --manifest MANIFEST
                        Path to AndroidManifest.xml (default:
                        ./AndroidManifest.xml)
  -s STRINGS, --strings STRINGS
                        Path to strings.xml (default:
                        ./res/values/strings.xml)
```

## Example

```
$ python3 get_schemas.py -m ./com.twitter.android/AndroidManifest.xml -s ./com.twitter.android/res/values/strings.xml
com.twitter.android.ProfileActivity (exported=False)
  content://com.android.contacts
com.twitter.app.deeplink.UrlInterpreterActivity (exported=False)
  http://mobile.twitter.com/.*
  http://twitter.com/.*
  http://www.twitter.com/.*
  https://ads.twitter.com/mobile
  https://mobile.twitter.com/.*
  https://twitter.com/.*
  https://www.twitter.com/.*
  twitter://account
  twitter://alerts/landing_page/.*
  twitter://bouncer
  twitter://broadcasts
  twitter://collection
  twitter://connect_people
  twitter://dm_conversation
  twitter://events/timeline/.*
  twitter://events/tv_show/.*
  twitter://explore
  twitter://flow/setup_profile
...
```
