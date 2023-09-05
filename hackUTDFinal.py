from datetime import date
import requests
import re
import sys
import pandas as pd
import statistics
from textblob import TextBlob
import os
import tweepy
import tweepy as tw

from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple


def Reddit(Keyword):
    # API SET UP  -----------------------------------

    # Client = public ID, secret = private ID
    CLIENT_ID = 'fOdEZ8Yc1loBTItp5lZbwQ'
    SECRET_KEY = '_--kBWfMZATzf2dJ4kOKLK8OplI_mg'

    # authentication info
    import requests
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

    # data info
    data = {
        'grant_type': 'password',
        'username': 'UTDProject',
        'password': 'TheUTDTeam123',
    }

    # header info
    headers = {'User-Agent': 'UTDProject1'}

    # requesting access to api w/ auth, data, and header
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)

    # TOKEN set up
    TOKEN = res.json()['access_token']

    # updating headers with access TOKEN
    headers = {**headers, **{'Authorization': f'bearer {TOKEN}'}}

    # IMPORT AND ACTUALLY RUN -----------------------------------

    # importing praw. also need to !pip install praw
    import praw

    # creating reddit object
    reddit = praw.Reddit(
        client_id="fOdEZ8Yc1loBTItp5lZbwQ",
        client_secret="_--kBWfMZATzf2dJ4kOKLK8OplI_mg",
        user_agent="UTDProject1",
    )

    # creates subreddit             change this
    subreddit = reddit.subreddit('cryptocurrency')
    # creates specific search (new, hot, etc.)
    # and limit of how many total posts (each post's replies gets displayed)
    top_cryptocurrency_lastday = subreddit.top('day', limit=100)

    # list to hold the comment
    reddittext = []
    my_keywords = [Keyword]

    Sent_polarity_R = []
    Sent_subjectivity_R = []

    # for every submission in cryptocurrency (top) in the last day, with a limit of 50 posts to search (change above)
    for submission in top_cryptocurrency_lastday:
        # ignores pinned posts
        if not submission.stickied:
            # DEBUG: prints title but doesnt save it
            # print('SEARCHING COMMENTS FOR POST TITLE: {}'.format(submission.title))

            # displays all comments on the post, then saves it to reddittext
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                if any(keyword in comment.body for keyword in my_keywords):
                    reddittext = comment.body
                    Sent_polarity_R.append(TextBlob(reddittext).sentiment.polarity)
                    Sent_subjectivity_R.append(TextBlob(reddittext).sentiment.subjectivity)
                    avg_Sent_polarity = statistics.mean(Sent_polarity_R)
                    avg_Sent_subjectivity = statistics.mean(Sent_subjectivity_R)
                    global R_pol
                    R_pol = avg_Sent_polarity
                    global R_sub
                    R_sub = avg_Sent_subjectivity
                #    print(reddittext)



    print(" The average polarity score for each Reddit post about {} is ".format(Keyword) + str(avg_Sent_polarity))
    print(" The average subjectivity score for each Reddit post about {} is ".format(Keyword) + str(avg_Sent_subjectivity))

def twitter(Keyword):
    consumer_key = 'dNQdkY02S5Jay5etZzFRJ4LLt'
    consumer_secret = 'T1jAc89jDd5omk3c3ZLEPLZX0Tv3jX4v81Y8lgXmZw8wUdBnDE'
    access_token = '771340796964409345-ATobywd9lqj0CQThSiEHOcvmVqVK56K'
    access_token_secret = 'atRqVq2zSUNlAPfADZ0O1BLVYbsJHM9cb359bNT3WKcIG'

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    date_since = "2021-11-13"
    posts_Tweets = []
    tweetytext = ""
    for tweets in api.search_tweets(q=Keyword, lang="en", result_type="recent", count=1000):
        whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789')
        tweetytext = tweets.text
        tweetytext = ' '.join(re.sub("[\.\,\!\?\:\;\-\=]", " ", tweetytext).split())
        tweetytext = ''.join(filter(whitelist.__contains__, tweetytext))
        posts_Tweets.append(tweetytext)
    lengthofTWEETS = len(posts_Tweets)
    Sent_polarity = []
    Sent_subjectivity = []
    for x in range(lengthofTWEETS):
        Sent_polarity.append(TextBlob(posts_Tweets[x]).sentiment.polarity)
        Sent_subjectivity.append(TextBlob(posts_Tweets[x]).sentiment.subjectivity)
    avg_Sent_polarity = statistics.mean(Sent_polarity)
    avg_Sent_subjectivity = statistics.mean(Sent_subjectivity)
    global twitter_pol
    twitter_pol = avg_Sent_polarity
    global twitter_sub
    twitter_sub = avg_Sent_subjectivity
    print(" The average polarity score for each Tweet about {} is ".format(Keyword) + str(avg_Sent_polarity))
    print(" The average subjectivity score for each Tweet about {} is ".format(Keyword) + str(avg_Sent_subjectivity))


def NEWS(Keyword):
    today = date.today();
    topic = Keyword
    sortBy = "popularity"
    apiKey = "1be56d5b7dad4c16845cd5565e091d2b"
    response = requests.get("https://newsapi.org/v2/everything?q=" + topic +
                            "&from=" + today.strftime("%d/%m/%Y") + "&sortBy=" +
                            sortBy + "top-headlines?country=us&apiKey=" + apiKey)
    response.request
    request = response.request
    request.url
    request.path_url
    request.method
    request.headers
    # print(response)

    data = response.json()
    # print(response.text)
    # print(data)

    # print(response.status_code)
    cnt = response.status_code
    onlineSentences = []
    for x in range(int(cnt / 10) - 1):
        onlineSentences.append(data['articles'][x]['content'])
        # print(data['articles'][x]['description'])
        # print(TextBlob(onlineSentences[x]).sentiment)

    Sent_polarity_news = []
    Sent_subjectivity_news = []
    for x in range(len(onlineSentences)):
        Sent_polarity_news.append(TextBlob(onlineSentences[x]).sentiment.polarity)
        Sent_subjectivity_news.append(TextBlob(onlineSentences[x]).sentiment.subjectivity)
    avg_Sent_polarity = statistics.mean(Sent_polarity_news)
    avg_Sent_subjectivity = statistics.mean(Sent_subjectivity_news)
    print(" The average polarity score for each Article content about {} is ".format(Keyword) + str(avg_Sent_polarity) )
    print(" The average subjectivity score for each Article Description {} is ".format(Keyword) + str(avg_Sent_subjectivity) )

    global News_pol
    News_pol = avg_Sent_polarity
    global News_sub
    News_sub = avg_Sent_subjectivity
def ALL(Keyword):


    twitter(Keyword)
    print("\n")
    Reddit(Keyword)
    print("\n")
    NEWS(Keyword)
    print("\n")


def main():
   Keyword = input("Enter Keyword to see: ")
   np.random.seed(42)

   def Bitcoin():
     ALL("Bitcoin")
     global ar_Bitcoin
     ar_Bitcoin=[twitter_pol,twitter_sub,R_pol,R_sub,News_pol,News_sub]
     print("\n")

   def Ethereum ():
     ALL("Ethereum")
     global ar_Ethereum
     ar_Ethereum =[twitter_pol,twitter_sub,R_pol,R_sub,News_pol,News_sub]
     print("\n")


   def BinanceCoin():
     ALL("Binance Coin")
     global ar_BinanceCoin
     ar_BinanceCoin=[twitter_pol,twitter_sub,R_pol,R_sub,News_pol,News_sub]
     print("\n")


   def Tether ():
       ALL("Tether")
       global ar_Tether
       ar_Tether  = [twitter_pol,twitter_sub,R_pol,R_sub,News_pol,News_sub]
       print("\n")


   def Cardano ():
       ALL("Cardano")
       global ar_Cardano
       ar_Cardano  = [twitter_pol,twitter_sub,R_pol,R_sub,News_pol,News_sub]
       print("\n")

   def Solana  ():
       ALL("Solana ")
       global ar_Solana
       ar_Solana   = [twitter_pol,twitter_sub,R_pol,R_sub,News_pol,News_sub]
       print("\n")

   def XRP   ():
       ALL("XRP")
       global ar_XRP
       ar_XRP    = [twitter_pol,twitter_sub,R_pol,R_sub,News_pol,News_sub]
       print("\n")

   def Polkadot ():
       ALL("Polkadot")
       global ar_Polkadot
       ar_Polkadot  = [twitter_pol,twitter_sub,R_pol,R_sub,News_pol,News_sub]
       print("\n")

   def Shiba_Inu ():
       ALL("Shiba Inu")
       global ar_Shiba_Inu
       ar_Shiba_Inu  = [twitter_pol,twitter_sub,R_pol,R_sub,News_pol,News_sub]
       print("\n")

   def Dogecoin():
       ALL("Dogecoin")
       global ar_Dogecoin
       ar_Dogecoin = [twitter_pol,twitter_sub,R_pol,R_sub,News_pol,News_sub]
       print("\n")

   def User(Keyword):
       twitter(Keyword)

       NEWS(Keyword)

       global ar_User
       ar_User = [twitter_pol,twitter_sub,0,0,News_pol,News_sub]
       print("\n")

   Bitcoin()
   print(ar_Bitcoin)
   Ethereum()
   print(ar_Ethereum)
   BinanceCoin()
   print(ar_BinanceCoin)
   Tether()
   print(ar_Tether)
   Cardano()
   print(ar_Cardano)
   Solana()
   print(ar_Solana)
   XRP()
   print(ar_XRP)
   Polkadot()
   print(ar_Polkadot)
   Shiba_Inu()
   print(ar_Shiba_Inu)
   Dogecoin()
   print(ar_Dogecoin)
   User(Keyword)
   print(ar_User)

main()
root = Tk()
root.title('Coin Selection Window')
root.iconbitmap()
root.geometry("400x665")
np.random.seed(42)
Crypto = namedtuple('Crypto', ['name'])
Score = namedtuple('Score', ['score', 'percentile'])

# GLOBAL CONSTANTS
test_names = ['Twitter \nPolarity', 'Twitter \nSubjectivity', 'Reddit \nPolarity', 'Reddit \nSubjectivity',
              'News \nPolarity', 'News \nSubjectivity']

def attach_ordinal(num):
    """Convert an integer to an ordinal string, e.g. 2 -> '2nd'."""
    suffixes = {str(i): v
                for i, v in enumerate(['th', 'st', 'nd', 'rd', 'th',
                                       'th', 'th', 'th', 'th', 'th'])}
    v = str(num)
    # special case early teens
    if v in {'11', '12', '13'}:
        return v + 'th'
    return v + suffixes[v[-1]]

def format_ycursor(y):
    y = int(y)
    if y < 0 or y >= len(test_names):
        return ''
    else:
        return test_names[y]

def plot_results(student, scores):
    fig, ax1 = plt.subplots(figsize=(9, 7))  # Create the figure
    fig.subplots_adjust(left=0.115, right=0.88)
    fig.canvas.manager.set_window_title('Bitcoin Sentiment Analysis')

    pos = np.arange(len(test_names))

    rects = ax1.barh(pos, [scores[k].percentile for k in test_names],
                     align='center',
                     height=0.5,
                     tick_label=test_names,
                     color=['cyan', 'cyan', 'orange', 'orange', 'red', 'red'])

    ax1.set_title(student.name)

    ax1.set_xlim([-1, 1])
    ax1.xaxis.set_major_locator(MaxNLocator(11))
    ax1.xaxis.grid(True, linestyle='--', which='major',
                   color='grey', alpha=.25)

    # Plot a solid vertical gridline to highlight the median position
    ax1.axvline(50, color='grey', alpha=0.25)

    # Set the right-hand Y-axis ticks and labels
    ax2 = ax1.twinx()

    # Set the tick locations
    ax2.set_yticks(pos)
    # Set equal limits on both yaxis so that the ticks line up
    ax2.set_ylim(ax1.get_ylim())

    # Set the tick labels
    ax2.set_yticklabels([(scores[k].score) for k in test_names])

    ax2.set_ylabel('Sentiment Metric')

    xlabel = ('Calculated Rate')
    ax1.set_xlabel(xlabel.format())

    # Make the interactive mouse over give the bar title
    ax2.fmt_ydata = format_ycursor
    # Return all of the artists created
    return {'fig': fig,
            'ax': ax1,
            'ax_right': ax2,
            'bars': rects}



crypto1 = Crypto('Bitcoin')
scores1 = dict(zip(
    test_names,
    (Score(v, p) for v, p in
     zip(ar_Bitcoin, ar_Bitcoin))))

crypto2 = Crypto('Ethereum')
scores2 = dict(zip(
    test_names,
    (Score(v, p) for v, p in
     zip(ar_Ethereum, ar_Ethereum))))

crypto3 = Crypto('BinanceCoin')
scores3 = dict(zip(
    test_names,
    (Score(v, p) for v, p in
     zip(ar_BinanceCoin, ar_BinanceCoin))))

crypto4 = Crypto('Tether')
scores4 = dict(zip(
    test_names,
    (Score(v, p) for v, p in
     zip(ar_Tether, ar_Tether))))

crypto5 = Crypto('Cardano')
scores5 = dict(zip(
    test_names,
    (Score(v, p) for v, p in
     zip(ar_Cardano, ar_Cardano))))

crypto6 = Crypto('Solana')
scores6 = dict(zip(
    test_names,
    (Score(v, p) for v, p in
     zip(ar_Solana, ar_Solana))))

crypto7 = Crypto('XRP')
scores7 = dict(zip(
    test_names,
    (Score(v, p) for v, p in
     zip(ar_XRP, ar_XRP))))

crypto8 = Crypto('Polkadot')
scores8 = dict(zip(
    test_names,
    (Score(v, p) for v, p in
     zip(ar_Polkadot, ar_Polkadot))))

crypto9 = Crypto('Shiba inu')
scores9 = dict(zip(
    test_names,
    (Score(v, p) for v, p in
     zip(ar_Shiba_Inu, ar_Shiba_Inu))))

crypto10 = Crypto('DogeCoin')
scores10 = dict(zip(
    test_names,
    (Score(v, p) for v, p in
     zip(ar_Dogecoin, ar_Dogecoin))))

crypto11 = Crypto("User Input")
scores11 = dict(zip(
    test_names,
    (Score(v, p) for v, p in
     zip(ar_User, ar_User))))





def graph1():
    arts = plot_results(crypto1, scores1)
    plt.show()

def graph2():
    arts = plot_results(crypto2, scores2)
    plt.show()

def graph3():
    arts = plot_results(crypto3, scores3)
    plt.show()

def graph4():
    arts = plot_results(crypto4, scores4)
    plt.show()

def graph5():
    arts = plot_results(crypto5, scores5)
    plt.show()

def graph6():
    arts = plot_results(crypto6, scores6)
    plt.show()

def graph7():
    arts = plot_results(crypto7, scores7)
    plt.show()

def graph8():
    arts = plot_results(crypto8, scores8)
    plt.show()

def graph9():
    arts = plot_results(crypto9, scores9)
    plt.show()

def graph10():
    arts = plot_results(crypto10, scores10)
    plt.show()

def graph11():
    arts = plot_results(crypto11, scores11)
    plt.show()

l = Label(root, text = "Cypto Options")
l.config(font=("Berlin Sans FB", 40))
l.place(x=45, y=20)

my_button = Button(root, text="Bitcoin", width=50, height=2, bg='#f2a900', command=graph1)
my_button.place(x=20, y=100)

my_button = Button(root, text="Ethereum", width=50, height=2, bg='#716b9d', command=graph2)
my_button.place(x=20, y=150)

my_button = Button(root, text="BinanceCoin", width=50, height=2, bg='#f3ba2f', command=graph3)
my_button.place(x=20, y=200)

my_button = Button(root, text="Tether", width=50, height=2, bg='#50af95', command=graph4)
my_button.place(x=20, y=250)

my_button = Button(root, text="Cardano", width=50, height=2, bg='#2a71d0', command=graph5)
my_button.place(x=20, y=300)

my_button = Button(root, text="Solana", width=50, height=2, bg='#00ffa3', command=graph6)
my_button.place(x=20, y=350)

my_button = Button(root, text="XRP", width=50, height=2, bg='#00aae4', command=graph7)
my_button.place(x=20, y=400)

my_button = Button(root, text="Polkadot", width=50, height=2, bg='#739dad', command=graph8)
my_button.place(x=20, y=450)

my_button = Button(root, text="Shiba inu", width=50, height=2, bg='#fbd491', command=graph9)
my_button.place(x=20, y=500)

my_button = Button(root, text="DogeCoin", width=50, height=2, bg='#3a3a3a', command=graph10)
my_button.place(x=20, y=550)

my_button = Button(root, text="User Input", width=50, height=2, bg='#ffc0cb', command=graph11)
my_button.place(x=20, y=600)

root.mainloop()