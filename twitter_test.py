from twython import Twython # pip3 install twython

from config import *    # my dropbox API key and Push bullet API key

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

print(twitter.verify_credentials())
