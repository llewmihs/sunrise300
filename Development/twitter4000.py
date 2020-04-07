from config import *    # my dropbox API key and Push bullet API key
from twython import Twython, TwythonError # pip3 install twython
from pushbullet import Pushbullet
from glob import glob # for the file upload process


pb = Pushbullet(PUSHBULLET)
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

def upload_to_twitter():
    try:
        video = glob("/home/pi/sunrise300/*.mp4")[0]
        response = twitter.upload_video(media=video, media_type='video/mp4')
        twitter.update_status(status="Here's this morning's sunrise...", media_ids=[response['media_id']])
        push = pb.push_note("Video tweeted", "Woop")
    except TwythonError as e:
        print(e)
        push = pb.push_note("There was a failure with the Twitter Upload.", e)

if __name__ == "__main__":
    upload_to_twitter()
