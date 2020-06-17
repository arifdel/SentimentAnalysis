from vaderSentiment.vaderSentiment  import SentimentIntensityAnalyzer
import tweepy
import pandas as pd
import csv
import re
import itertools


consumerKey = "XXXXXXXXXXXXXXXXXXXXXXXXXX"
consumerSecret = "XXXXXXXXXXXXXXXXXXXXXXXXXX"
accessToken = "XXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXX"
accessTokenShort = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"


auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenShort)
api = tweepy.API(auth, wait_on_rate_limit=True)


searchTerm = '@Adani_Elec_Mum'
noOfSearchTerms = 100
posts = []
datetime = []

# Create a function to clean the tweets
def cleanTxt(text):
    text = re.sub('@[A-Za-z0–9]+', '', text)  # Removing @mentions
    text = re.sub('#', '', text)  # Removing '#' hash tag
    text = re.sub('RT[\s]+', '', text)  # Removing RT
    text = re.sub('https?:\/\/\S+', '', text)  # Removing hyperlink
    # print (text)
    return text

def getTweets():
    for status in tweepy.Cursor(api.search, q=searchTerm, lang='en', tweet_mode='extended').items(noOfSearchTerms):
        clean_Text = cleanTxt(status.full_text)
        posts.append(clean_Text)
        datetime.append(str(status.created_at))

def runAnalysis():
    lol = []
    analyzer = SentimentIntensityAnalyzer()
    for (sentence, date) in zip(posts, datetime):
        ss = analyzer.polarity_scores(sentence)
        if ss['compound'] >= 0.05:
            sentiment = 'Positive'
        if ss['compound'] <= -0.05:
            sentiment = 'Negative'
        if ss['compound'] < 0.05 and ss['compound'] > -0.05:
            sentiment = 'Neutral'
        ss['sentence'] = sentence
        ss['sentiment'] = sentiment
        ss['date'] = date
        lol.append(ss)

    df = pd.DataFrame(lol)
    df = df[['sentence' , 'neg' , 'neu' , 'pos' , 'compound' , 'date' , 'sentiment']]
    df.to_csv('C:\\Users\\mohd.arif.siddiqui\\Desktop\\Abhishek\\twittersentiments.csv')
    print ("CSV file created with sentiment analysis")

def main():
    getTweets()
    runAnalysis()

if __name__ == "__main__":
    main()