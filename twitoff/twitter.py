"""Retreive Tweets, embeddings, and persist in the databse."""
import basilica
import tweepy
from os import getenv
from .models import DB, Tweet, User

TWITTER_AUTH = tweepy.OAuthHandler(getenv('TWITTER_CONSUMER_KEY'), getenv('TWITTER_CONSUMER_SECRET'))
TWITTER_AUTH.set_access_token(getenv('TWITTER_ACCESS_TOKEN'), getenv('TWITTER_ACCESS_TOKEN_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)

BASILICA = basilica.Connection(getenv('BASILICA_KEY'))


def add_or_update_user(username):
    """Add or update a user and their tweets. No private user"""
    try:
        twitter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id, name=username))
        DB.session.add(db_user)
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False,
            tweet_mode='extended', since_id=db_user.newest_tweet_id
        )
        if tweets:
            db_user.newest_tweet_id = tweets[0].id
        for tweet in tweets:
            # Get embedding for tweet, and store in db
            embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500],
                            embedding=embedding)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)
    except Exception as e:
        print('Error processing {}: {}'.format(username, e))
        raise e
    else:
        DB.session.commit()

def add_user(users):
    for user in users:
        add_or_update_user(user)

def update_all_users():
    for user in User.query.all():
        add_or_update_user(user.name)