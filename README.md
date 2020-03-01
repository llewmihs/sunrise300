# sunrise300

## Overview

The sunrise3000 is a Raspberry Pi timelapse camera which builds a timelapse video of sunrise each day and uploads to dropbox

## Dependencies

The following modules are needed:

* dropbox `pip3 install dropbox`
* pushbullet `pip3 install pushbullet.py`
* astral `pip3 install astral`
* python-crontab `pip3 install python-crontab`

### Dropbox

To use dropbox from python, you'll need to find your API Access Token, create an app first: https://www.dropbox.com/developers/apps
In python:

``` python
import dropbox
dbx = dropbox.Dropbox(YOUR_ACCESS_TOKEN, timeout = None)
```

We need to set `timeout=None` to enable uploads of large files that will take longer than the default timeout of 30 seconds.
To upload a file to dropbox:

``` python
with open(filepath, "rb") as f:
    dbx.files_upload(f.read(), filepath, mute = True)
```