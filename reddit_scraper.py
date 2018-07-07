import config
import praw

client_id = config.CLIENT_ID
client_secret = config.CLIENT_SECRET
username = config.USERNAME
password = config.PASSWORD
user_agent = config.USER_AGENT

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     password=password,
                     user_agent=user_agent,
                     username=username)
reddit.read_only = True
