# Sentiment Analysis of Tweets

This project was developed as part of my A-Level Computer Science coursework. It uses the Twitter API to fetch tweets based on a specified user or keyword, analyzes the sentiment of those tweets, and visualizes the results in various formats, including word clouds, pie charts, scatter graphs, and gauges.

The core functionality of the program includes:
- **Fetching Tweets**: Retrieve recent tweets from a specific user or based on a keyword.
- **Sentiment Analysis**: Each tweet is analyzed for its polarity (positive, neutral, negative) and subjectivity using the TextBlob library.
- **Visualization**: Interactive visualizations (word clouds, pie charts, scatter plots, and gauge charts) are generated to represent the sentiment of the tweets.

## Important Note: Twitter API Changes

As of 2024, **Twitter no longer offers a free API**, which means that the API calls in this project will not work unless you have access to a paid Twitter Developer account. As a result, the current version of this project will not function as expected unless these API access changes are addressed. You can refer to the official [Twitter Developer documentation](https://developer.twitter.com/en/docs) for more information on current API offerings.

### Features:

- **Sentiment Classification**: Tweets are classified as positive, negative, or neutral based on sentiment polarity.
- **Data Processing**: Tweets are cleaned by removing mentions, hashtags, and URLs to improve analysis accuracy.
- **Word Cloud Generation**: A word cloud is created from the most frequently used words in the tweets.
- **Visualization Tools**: 
    - **Pie chart** showing the distribution of positive, negative, and neutral tweets.
    - **Scatter plot** for polarity vs. subjectivity.
    - **Gauge chart** showing the average polarity of all tweets.
  
---

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/domparsons/twitter-sentiment-analysis.git
    cd sentiment-analysis-twitter
    ```

2. Set up a virtual environment and install the required dependencies:

    ```bash
    uv sync
    ```

3. Obtain Twitter API access:
    - Due to changes in Twitter’s API policy, you will need access to a paid Twitter Developer account to use this project. Update the `TwitterConnector` class with your own API keys if you have access.

---

## Usage

1. **Run the Script**: After setting up the environment and ensuring you have API access, you can run the script:

    ```bash
    python sentiment_analysis.py
    ```

2. **Input**: The program will prompt you to either input a Twitter username or a keyword for the sentiment analysis.

3. **Results**: The program will output the percentage of positive, negative, and neutral tweets. It will also display a word cloud, pie chart, scatter plot, and a gauge for the average polarity.

---

## File Structure

```plaintext
sentiment-analysis-twitter/
├── cloudMask/
│   └── mask.png                # Mask image for the word cloud
├── sentiment_analysis.py       # Main script for sentiment analysis
├── requirements.txt            # List of dependencies
└── README.md                   # Project documentation