import pymongo
import os

#CONNECTION_STRING = "mongodb://jatin:Jatin@123@ds119044.mlab.com:19044/heroku_m1jwc5f7"  # replace it with your settings
CONNECTION_STRING="mongodb://heroku_m1jwc5f7:pscl5u32sdhnq02vjol6q7fdb2@ds119044.mlab.com:19044/heroku_m1jwc5f7"
CONNECTION = pymongo.MongoClient(CONNECTION_STRING)

'''Leave this as is if you dont have other configuration'''

DATABASE = CONNECTION.heroku_m1jwc5f7
POSTS_COLLECTION = DATABASE.posts
USERS_COLLECTION = DATABASE.users
SETTINGS_COLLECTION = DATABASE.settings

SECRET_KEY = ""
basedir = os.path.abspath(os.path.dirname(__file__))
secret_file = os.path.join(basedir, '.secret')
if os.path.exists(secret_file):
    # Read SECRET_KEY from .secret file
    f = open(secret_file, 'r')
    SECRET_KEY = f.read().strip()
    f.close()
else:
    # Generate SECRET_KEY & save it away
    SECRET_KEY = os.urandom(24)
    f = open(secret_file, 'w')
    f.write(SECRET_KEY)
    f.close()
    # Modeify .gitignore to include .secret file
    gitignore_file = os.path.join(basedir, '.gitignore')
    f = open(gitignore_file, 'a+')
    if '.secret' not in f.readlines() and '.secret\n' not in f.readlines():
        f.write('.secret\n')
    f.close()

LOG_FILE = "app.log"

DEBUG = True  # set it to False on production
