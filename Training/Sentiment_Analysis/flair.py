from datetime import datetime, timedelta
import requests
import pandas as pd
import time
import re

whitespace = re.compile(r"\s+")
web_address = re.compile(r"(?i)http(s):\/\/[a-z0-9.~_\-\/]+")
tesla = re.compile(r"(?i)@Solana(?=\b)")
user = re.compile(r"(?i)@[a-z0-9_]+")
# read bearer token for authentication

BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAMR1TQEAAAAAg7XmeThysyZhVgfGdRuWWbrp27w%3DSFFQdgkHK0y3j3DpzbRBE1TeboIHPoSJ9ZlY3iRwrSV5HgE4d7'

# setup the API request
endpoint = 'https://api.twitter.com/2/tweets/search/recent'
headers = {'authorization': f'Bearer {BEARER_TOKEN}'}
params = {
    'query': '(solana OR SOL OR ignition) (lang:en)',
    'max_results': '100',
    'tweet.fields': 'created_at,lang'
}

def get_data(tweet):
    data = {
        'id': tweet['id'],
        'created_at': tweet['created_at'],
        'text': tweet['text']
    }
    return data

increment = 0
dtformat = '%Y-%m-%dT%H:%M:%SZ'  # the date format string required by twitter

# we use this function to subtract 60 mins from our datetime string
def time_travel(now, mins):
    now = datetime.strptime(now, dtformat)
    back_in_time = now - timedelta(minutes=mins)
    return back_in_time.strftime(dtformat)
    
now = datetime.now()
now -= timedelta(seconds=10)  # get the current datetime, this is our starting point
last_week = now - timedelta(days=7)  # datetime one week ago = the finish line
now = now.strftime(dtformat)  # convert now datetime to format for API

df = pd.DataFrame()  # initialize dataframe to store tweets

df = pd.DataFrame()  # initialize dataframe to store tweets
while True:
    if datetime.strptime(now, dtformat) < last_week:
        # if we have reached 7 days ago, break the loop
        break
    pre60 = time_travel(now, 60)  # get 60 minutes before 'now'
    # assign from and to datetime parameters for the API
    params['start_time'] = pre60
    params['end_time'] = now
    response = requests.get(endpoint,
                            params=params,
                            headers=headers)  # send the request
    now = pre60  # move the window 60 minutes earlier

    for tweet in response.json()['data']:
        row = get_data(tweet)  # we defined this function earlier
        df = df.append(row, ignore_index=True)
        tweets = df.text.values.tolist()
        print(tweets)

    for tweet in tweets: 
        whitespace = re.compile(r"\s+")
        web_address = re.compile(r"(?i)http(s):\/\/[a-z0-9.~_\-\/]+")
        tesla = re.compile(r"(?i)@Solana(?=\b)")
        user = re.compile(r"(?i)@[a-z0-9_]+")

        # we then use the sub method to replace anything matching
        tweet = whitespace.sub(' ', tweet)
        tweet = web_address.sub('', tweet)
        tweet = tesla.sub('Solana', tweet)
        tweet = user.sub('', tweet)


