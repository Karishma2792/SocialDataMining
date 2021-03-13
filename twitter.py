#import neccessary library
import tweepy
from pymongo import MongoClient
import apikeys

#OAuth authentication for twitter
auth = tweepy.OAuthHandler(apikeys.twitter.API_KEY, apikeys.twitter.API_secret_key)
auth.set_access_token(apikeys.twitter.Access_Token, apikeys.twitter.Access_TokenSecret)
api = tweepy.API(auth)

#empty list to store tweets
tweets_data = []
#scrape data from my twitter account
def main():
    columns = set()
    allowed_types = [str,int]
    for status in api.user_timeline("username"):
        status_dict = dict(vars(status))
        keys = ['id', 'text', 'retweet_count', 'favorite_count', 'lang', 'source']
        single_tweet_data = {"user": status.user.screen_name}
        
        for k in keys:
            v_type = type(status_dict[k])
            if v_type in allowed_types:
                single_tweet_data[k] = status_dict[k]
                columns.add(k)
        tweets_data.append(single_tweet_data)
        
        #Mongodb connection
    def get_mongo():
        client = MongoClient(
           "mongodb+srv://username:password@cluster0.rj36d.mongodb.net/dbname?retryWrites=true&w=majority"
           )
        db = client['dbname']
        return db
    db = get_mongo()
    collection = db['collection_name']
    collection.insert_many(tweets_data)
#main function to execute flask app.py    
if __name__ == '__main__':
    main()