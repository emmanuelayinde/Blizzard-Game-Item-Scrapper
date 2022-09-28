import os
import requests
import tweepy
from dotenv import load_dotenv

from utils.date import now

load_dotenv()

# TWITTER API CREDENTIALS 
consumerKey = os.environ.get("CONSUMER_KEY")
consumerSecret = os.environ.get("CONSUMER_SECRET")
accessToken = os.environ.get("ACCESS_TOKEN")
accessTokenSecret = os.environ.get("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuth1UserHandler(
    consumerKey,
    consumerSecret,
    accessToken,
    accessTokenSecret
)
client = tweepy.API(auth)

# The app and the corresponding credentials must have the Write permission
def tweet(tweet, media = None):
    if media == None:
        response = client.update_status(
            status = tweet
        )
    else:
        tweet_image(media, tweet)

def tweet_image(url, message):
    file = 'temp.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(file, 'wb') as image:
            for chunk in request:
                image.write(chunk)

        media_file = client.media_upload(filename = file)
        response = client.update_status(status = message, media_ids = [media_file.media_id_string])
        print('Tweeted.................................', now())
        os.remove(file)
    else:
        print("Unable to download image")
