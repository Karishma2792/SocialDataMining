import tweepy
import praw
from flask import Flask, request, redirect
from flask import render_template
from flask_pymongo import PyMongo 
import apikeys

app = Flask(__name__)

#Connect to  Mongodb using connection string
app.config['MONGO_DBNAME'] = 'dbname'
app.config['MONGO_URI'] =  "mongodb+srv://username:password@cluster0.rj36d.mongodb.net/dbname?retryWrites=true&w=majority"
mongo = PyMongo(app)

#OAuth Authentication for twitter
auth = tweepy.OAuthHandler(apikeys.twitter.API_KEY, apikeys.twitter.API_secret_key)
auth.set_access_token(apikeys.twitter.Access_Token, apikeys.twitter.Access_TokenSecret)
api = tweepy.API(auth)

#OAuth Authentication for Reddit
reddit = praw.Reddit(client_id = apikeys.reddit.client_id, 
                     client_secret =  apikeys.reddit.client_secret,
                     user_agent = apikeys.reddit.user_agent,
                     redirect_uri = apikeys.reddit.redirect_uri,
                     refresh_token = apikeys.reddit.refresh_token)


#app_route to index.html
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

#app_route to twitter.html
@app.route('/postTweet', methods=['GET','POST'])
def postTweet():
    if request.method == "POST":
        message = request.form["tweet"]
        status = api.update_status(message)
        collection = mongo.db.twitter
        collection.insert_one({'user':status.user.screen_name,
                               'id':status.id,
                               'text':status.text,
                               'retweet_count':status.retweet_count,
                               'favorite_count':status.favorite_count,
                               'lang':status.lang,
                               'source':status.source })
        return redirect('/')
    return render_template('twitter.html')

#app_route to reddit.html
@app.route('/postReddit', methods=['GET','POST'])
def postReddit():
    if request.method == "POST":
        title = request.form['title']
        message = request.form['message']
        sub = reddit.subreddit("subreddit")
        post = sub.submit(title, message)
        collection = mongo.db.reddit
        collection.insert_one({"id": post.id,
                               "author_name": post.author.name,
                               "title": post.title,
                               "text": post.selftext})
        return redirect('/')
    return render_template('reddit.html')                               

#main function to run flask app.py
if __name__ == '__main__':
    app.run()