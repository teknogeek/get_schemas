# get_schemas

Pretty straightforward, just gets all the URL schemas and the corresponding activities and prints them all out.

You're going to want to decompile the app with `apktool` before running this so that you have a decoded copy of:

- AndroidManifest.xml
- res/values/strings.xml

Both of these files are required for this tool to work as it substitutes any `@string/x_y_z` values.

## Installation

```
$ pip install -r requirements.txt
```

## Usage

```
$ ./get_schemas.py -h
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
$ ./get_schemas.py -m ./com.twitter.android/AndroidManifest.xml -s ./com.twitter.android/res/values/strings.xml
com.twitter.android.ProfileActivity
  content://com.android.contacts
com.twitter.app.deeplink.UrlInterpreterActivity
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
  twitter://follow
  twitter://followers/verified
  twitter://front
  twitter://golive
  twitter://hashtag/.*
  twitter://intent/favorite
  twitter://intent/follow
  twitter://intent/like
  twitter://intent/retweet
  twitter://interest_picker
  twitter://internal/.*
  twitter://list
  twitter://lists
  twitter://live/timeline/.*
  twitter://login
  twitter://login-token
  twitter://mentions
  twitter://messages
  twitter://moment
  twitter://moments
  twitter://moments/guide
  twitter://moments/list
  twitter://moments/maker
  twitter://news
  twitter://photo
  twitter://post
  twitter://profiles/edit
  twitter://quote
  twitter://search
  twitter://session/new
  twitter://settings
  twitter://share_via_dm
  twitter://signup
  twitter://status
  twitter://stickers
  twitter://storystream
  twitter://switch_to_logged_in_account
  twitter://teams_invitation
  twitter://timeline
  twitter://topics
  twitter://trends
  twitter://tweet
  twitter://tweet_previews
  twitter://unfollow
  twitter://user
```
