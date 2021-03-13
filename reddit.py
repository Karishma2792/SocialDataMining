#import neccessary library
import praw
from pymongo import MongoClient
import apikeys

#OAuth authentication for Reddit
reddit = praw.Reddit(client_id = apikeys.reddit.client_id, 
                     client_secret =  apikeys.reddit.client_secret,
                     user_agent = apikeys.reddit.user_agent,
                     redirect_uri = apikeys.reddit.redirect_uri,
                     refresh_token = apikeys.reddit.refresh_token)

#scrape data from my reddit account
def main():
    posts_data = []                     
    for posts in reddit.subreddit("subreddit").new():
        post = {"id": posts.id,
                 "author_name": posts.author.name,
                 "title": posts.title,
                 "text": posts.selftext}
        posts_data.append(post)

 #Mongodb connection
    def get_mongo():
        client = MongoClient(
           "mongodb+srv://username:passwordcluster0.rj36d.mongodb.net/dbname?retryWrites=true&w=majority"
        )
        db = client['dbname']
        return db
    
    db = get_mongo()
    collection = db['collection_name']
    collection.insert_many(posts_data)
    
#main function to execute flask app.py        
if __name__ == '__main__':
    main()