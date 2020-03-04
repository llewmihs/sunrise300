from twython import Twython # pip3 install twython

from config import *    # my dropbox API key and Push bullet API key

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

video = open('/path/to/file/video.mp4', 'rb')
response = twitter.upload_video(media=video, media_type='video/mp4')
twitter.update_status(status='Checkout this cool video!', media_ids=[response['media_id']])