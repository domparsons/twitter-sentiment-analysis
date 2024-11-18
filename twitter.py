
# ********************************************* Imports ******************************************************************* #

import tweepy # Allows access to Twitter API
from textblob import TextBlob # Textblob: a Python library for processing textual data
from wordcloud import WordCloud # Wordcloud: a Python library to create a word cloud of common words / phrases
import pandas as pd # Pandas: a data analysis and manipulation tool
import numpy as np # Numpy: create a mask for wordcloud
import re # regular expression operation for removing characters when cleaning tweets
import matplotlib.pyplot as plt # for plotting graph
import plotly.graph_objects as go # for creating gauge
from PIL import Image # for saving outputs as image files

# ********************************************* End of imports ************************************************************ #



# ********************************************* Start of Twitter connector class ****************************************** #

class TwitterConnector:
  # Set up the dictionary of Twitter Access Keys
  # If the program were to be used with a different social media platform, this Twitter connector class would be
  # interchanged or amended to provide access to this platform
  TwitterAccessKeys={
  "consumerKey":"",
  "consumerSecret":"",
  "accessToken":"",
  "accessTokenSecret":""
  }

  def __init__(self):
    # Set up the values for the connector
    # If the account used to access the Twitter API were to change, the value pairs for the tokens would be changed here
    self.TwitterAccessKeys["consumerKey"] = "UH0w6z4XBfKhySCpPgHKB3Beo"
    self.TwitterAccessKeys["consumerSecret"] = "5WvEbU63Lu2jrAW7XALO1jfJ542F9cJoZlzeCuct0SBXhbsQER"
    self.TwitterAccessKeys["accessToken"] = "919970217148764161-iqIFHvmm7UNTF3gHHL7OYfWMM8XKPmZ"
    self.TwitterAccessKeys["accessTokenSecret"] = "t2VnWGCyJER6i7adyQYRELD8Hh8liYL8k6QLjdXgTwDMd"
    
  def setUpConnection(self):
    # Create the authentication object
    authenticate = tweepy.OAuthHandler(self.TwitterAccessKeys["consumerKey"], self.TwitterAccessKeys["consumerSecret"])
    # Set the access token and the access token secret
    authenticate.set_access_token(self.TwitterAccessKeys["accessToken"], self.TwitterAccessKeys["accessTokenSecret"])
    # Create API object while passing in authentication information
    api = tweepy.API(authenticate, wait_on_rate_limit = True)
    return api

# ********************************************* End of Twitter connector class ******************************************** #



# ********************************************* Start of data processor class ********************************************* #

# This class will take the dataframe, clean the tweets and apply polarity and subjectivity analysis

class DataProcessor:
  
  def __init__(self):
    pass

  # This function checks that the data frame has Tweets in
  def checkTweets(self,_df):
    if _df.shape[0] == 0:
      return False
    else:
      return True

  # This function applies the cleanTweets_ function to the Tweets column
  def cleanTweets(self, _df):
    _df['Tweets'] = _df['Tweets'].apply(self.cleanTweets_)
    return _df['Tweets']

  # This function applies the getSubjectivity_ function to the Tweets column
  def getSubjectivity(self,_df):
    _df['Subjectivity'] = _df['Tweets'].apply(self.getSubjectivity_)
    return _df['Subjectivity']

  # This function applies the getPolarity_ function to the Tweets column
  def getPolarity(self,_df):
    _df['Polarity'] = _df['Tweets'].apply(self.getPolarity_)
    return _df['Polarity']

  # This function applies the getAnalysis_ function to the Polarity column
  def getAnalysis(self, _df):
    _df['Analysis'] = _df['Polarity'].apply(self.getAnalysis_)
    return _df['Analysis']

  # The following function cleans the text by removing special characters, @ mentions and URLs
  # To aid future development: this function should be amended to correctly remove @ mentions which include special characters
  def cleanTweets_(self,text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text) # removes @ mentions
    text = re.sub(r'#', '', text) # removes hashtag symbol
    text = re.sub(r'RT[\s]+', '', text) # removes retweet
    text = re.sub(r'https?:\/\/\S+', '', text) # removes URLs
    return text

  # This function passes the Tweets into Textblob and retrieves a value based on how subjective the Tweet is
  def getSubjectivity_(self,text):
    return TextBlob(text).sentiment.subjectivity

  # This function passes the Tweets into Textblob and retrieves a value based on the polarity of the Tweet
  def getPolarity_(self,text):
    return TextBlob(text).sentiment.polarity 

  # This function computes the given polarity value and provides each Tweet with the word describing the polarity
  def getAnalysis_(self,score):
    if score < -0.1:
      return "Negative"
    elif score > 0.1:
      return "Positive"
    else: 
      return "Neutral"

  # This function finds the percentage of positive Tweets
  def percentagePositive(self, _df):
    positiveTweets = _df[_df.Analysis == 'Positive']
    positiveTweetsPercentage = str(round((positiveTweets.shape[0] / _df.shape[0]) * 100, 1))
    return positiveTweetsPercentage

  # This function finds the percentage of negative Tweets
  def percentageNegative(self, _df):
    negativeTweets = _df[_df.Analysis == 'Negative']
    negativeTweetsPercentage = str(round((negativeTweets.shape[0] / _df.shape[0]) * 100, 1))
    return negativeTweetsPercentage

  # This function finds the percentage of neutral Tweets
  def percentageNeutral(self, _df):
    neutralTweets = _df[_df.Analysis == 'Neutral']
    neutralTweetsPercentage = str(round((neutralTweets.shape[0] / _df.shape[0]) * 100, 1))
    return neutralTweetsPercentage

  # This function calculates the average polarity of the Tweets
  def findAveragePolarity(self, _df):
    average = _df['Polarity'].sum() / len(_df.index)
    average = str(round(average, 3))
    return average

# ********************************************* End of data processor class *********************************************** #



# ********************************************* Start of data plotter class *********************************************** #

# This class could be used 
class DataPlotter:

  def __init__(self):
    pass

  # Create and display the word cloud with the most frequent words used in the Tweets
  def plotWordCloud(self, _df):
    # Text is a string of all the Tweets concatenated together
    text = ' '.join( [twts for twts in _df['Tweets']] )
    # The mask variable is passed into the WordCloud() function, and is a PNG of a cloud
    mask = np.array(Image.open('cloudMask/mask.png'))
    wordCloud = WordCloud(width = 3000, height = 2000, background_color="white", mask = mask).generate(text)
    plt.imshow(wordCloud, interpolation = 'bilinear')
    plt.axis('off')
    plt.show()

  # Display the percentages of sentiment analysis as a pie chart
  def plotPieChart(self, percentPos, percentNeg, percentNeut):
    labels = 'Positive', 'Negative', 'Neutral'
    sizes = [positiveTweetsPercentage, negativeTweetsPercentage, neutralTweetsPercentage]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  
    plt.show()

  # Plot the polarity and subjectivity scatter graph 
  def plotScatterGraph(self, _df):
    plt.figure(figsize=(8,8))
    for i in range(0,_df.shape[0]):
      plt.scatter(_df['Polarity'][i],_df['Subjectivity'][i], color="Blue")
    plt.title('Sentiment Analysis')
    plt.xlabel('Polarity')
    plt.ylabel('Subjectivity')
    plt.show()

  # Show gauge with average polarity of tweets as the value
  def plotGauge(self, _average):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = float(_average),
        domain = {'x': [0, 0.5], 'y': [0, 1]},
        title = {'text': "Sentiment analysis average", 'font': {'size': 24}},
        gauge = {
            'axis': {'range': [-1, 1], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 0,
            'bordercolor': "gray",
            'steps': [
                {'range': [-1, -0.333], 'color': 'red'},
                {'range': [-0.333, 0.333], 'color': 'orange'},
                {'range': [0.333, 1], 'color': 'green'}]}))
    fig.show()

# ********************************************* End of data plotter class ************************************************* #



# ********************************************* Other functions *********************************************************** #

# This function takes the user input and the api variable to fetch the Tweets for the given username
def userSearch(_user,_api):
  # This line of code fetches 100 Tweets using Tweepy and the input, storing the fetched information under a variable called posts
  posts = _api.user_timeline(screen_name = _user, count = 100, tweet_mode = "extended")
  # This line uses Pandas to create a dataframe with a column called Tweets, with the Tweets just fetched
  df = pd.DataFrame([tweet.full_text for tweet in posts], columns = ['Tweets'])
  return df

# This function takes the user input and the api variable to fetch the Tweets for the given keyword
def keywordSearch(_keyword, _api):
  # This line of code fetches 100 Tweets using Tweepy and the input, storing the fetched information under a variable called keywordTweets
  keywordTweets = _api.search_tweets(q=_keyword, count = 100, tweet_mode="extended")
  # This line uses Pandas to create a dataframe with a column called Tweets, with the Tweets just fetched
  df = pd.DataFrame([tweet.full_text for tweet in keywordTweets], columns = ['Tweets'])
  return df

# This function is unused, but prints the most recent Tweets for the username provided, and can be integrated with one function call
def printRecentUserTweets(posts):
  i=1
  print("Here are the 100 most recent tweets:")
  for tweet in posts[0:100]:
    print(str(i) + ". ")
    print(tweet.full_text)
    print("________________________________________________________________")
    print(" ")
    i = i + 1

# This function is unused, but prints the most recent Tweets for the keyword provided, and can be integrated with one function call
def printRecentKeywordTweets(keywordTweets):
  i=1
  print("Here are the 100 most recent tweets:")
  for tweet in keywordTweets[0:100]:
    print(str(i) + ". ")
    print(tweet.full_text)
    print("________________________________________________________________")
    print(" ")
    i = i + 1

# ********************************************* End of other functions **************************************************** #



# ********************************************* Start of main program ***************************************************** #

# Instantiate the Twitter connection object
Twitter_Connection = TwitterConnector()
api = Twitter_Connection.setUpConnection()

# Asks the user if they wish to retrieve Tweets using a username or keyword, and assigns their answer to a variable
print("Would you like to receive sentiment analysis from a Twitter user or keyword?")
inputType = str(input("Please type 'user' or 'keyword': "))

valid = False
while (valid == False):
  # This if statement checks if the user answered with 'user'
  if (inputType.lower() == "user"):
    # This input asks the user for the Twitter handle to fetch the Tweets with
    user = str(input("Please enter the Twitter handle of the user you wish to receive sentiment analysis about: "))
    user.lower()
    try:
      df = userSearch(user, api)
      valid = True
    except:
      print("There are no Twitter accounts with this handle.")

  # This elif statement checks if the user answered with 'keyword'
  elif (inputType.lower() == "keyword"):
    # This input asks the user for the keyword to fetch the Tweets with
    keyword = str(input("Please enter the keyword you wish to receive sentiment analysis about: "))
    keyword.lower()
    try:
      df = keywordSearch(keyword, api)
      valid = True
    except:
      print("An error has occurred")

  # If the input is not as required, the user is asked again until an appropriate answer is given
  else:
    inputType = str(input("Input does not match the options provided. Please try again. Enter 'user' or 'keyword': "))
    valid = False

# Instantiate the data processor object
data_processor = DataProcessor()
# Check that Tweets are found
tweets_found = data_processor.checkTweets(df)

# Check to ensure that there are Tweets found for the given input
if tweets_found == False:
  print("There are no Tweets found for this input...")

else:
  # Pass the Tweets through the 'cleanTweets' function
  df['Tweets'] = data_processor.cleanTweets(df)

  # Create and fill the 'polarity' and 'subjectivity' columns in the dataframe
  df['Subjectivity'] = data_processor.getSubjectivity(df)
  df['Polarity'] = data_processor.getPolarity(df)

  # Apply positive, negative or neutral to the Tweets
  df['Analysis'] = data_processor.getAnalysis(df)

  # Calculate the percentages of positive, negative and neutral Tweets by calling respective functions
  positiveTweetsPercentage = data_processor.percentagePositive(df)
  negativeTweetsPercentage = data_processor.percentageNegative(df)
  neutralTweetsPercentage = data_processor.percentageNeutral(df)

  # Print the percentages of positive, negative and neutral functions
  print(positiveTweetsPercentage + "% of the tweets were positive")
  print(negativeTweetsPercentage + "% of the tweets were negative")
  print(neutralTweetsPercentage + "% of the tweets were neutral")

  # Calculate and output average polarity
  # The average value is saved as it is used later when creating the gauge output
  average = str(data_processor.findAveragePolarity(df))
  print("The average polarity of the tweets was: " + average)
  print("-1 is extremely negative, +1 is extremely positive and 0 is neutral")

  # Instantiate the data plotter object
  plotter = DataPlotter()

  # Create and display the word cloud with the most frequent words used in the Tweets
  plotter.plotWordCloud(df)

  # Create a pie chart to display the proportions of positive, negative and neutral Tweets
  plotter.plotPieChart(positiveTweetsPercentage, negativeTweetsPercentage, neutralTweetsPercentage)
  
  # Plot the polarity and subjectivity scatter graph
  plotter.plotScatterGraph(df)
  
  # Show gauge with the average polarity of tweets as the value
  plotter.plotGauge(average)

# ********************************************* End of main program ******************************************************* #
