# HackUTD2021
The Code for our HackUTD 2021 Project, featuring Sentiment Analysis and API integration
CryptoFromSentimentAnalysis

NOTE: THE TOKEN FOR THE REDDIT API IS EXPIRED

#Quick Introduction Hello! We are SF = Valid. We are a group of students here at UTD, consisting of John Habeeb (CS), Mark Farid (CE), Kerlous Abdelmalak (CS), and Kevin Mikhaiel (CE). We hope you enjoy our project!

#Inspiration When looking at the possible problems to solve, we realized that Cryptocurrency was one of the most interesting problems to tackle. Unlike traditional investment options, Crypto is very volatile, and relies heavily on sentiment of the people.

#What it does Our code analyzes three sources to see what people think about some of the largest cryptocurrencies, in order to help the user make decisions based on common perception of the coin. It searches through the most popular news articles that mention the cryptocurrencies mentioned, and then checks Twitter and Reddit. This range of sources provides both factual documentation, and popular opinion to provide a good range of data to work with. We then analyze the articles, tweets, and posts for polarity (how positive or negative the text is in regards to the word in question), and subjectivity (how emotionally driven the text is). Using the data we receive, we create a graph for each coin, to help the user make a decision on the best Crypto to consider.

#How we built it The construction of this project was split into 3 parts: Retrieving the source text and filtering it for Sentiment Analysis, running the source files through the Sentiment Analysis and retrieving the corresponding polarity and subjectivity, and outputting that data on a graph for the user to see and utilize.

#Challenges we ran into We faced a couple issues throughout the length of the project. Firstly, pulling recent Tweets wasn't too difficult after obtaining access to Twitter's Developer API (v2), but getting access to Reddit comments proved to be a challenge. On the output side, we had issues with formatting the graph to be as simple as possible, while still being usable.

#Accomplishments that we're proud of We're proud of the functionality of our code, and how we scraped the text from the news articles and social media.

#What we learned We learned a lot about implementing API's and searching for various text parameters using those APIs. We also greatly improved our Python skills, and learned about creating GUI's in Python. We also learned to work together better by splitting the project into smaller tasks, and organizing ways to combine the split functions. What's next for Crypto Suggestions Using Sentiment Analysis

#We would like to expand this code beyond just cryptocurrencies. While Crypto faces the most volatility due to popular sentiment, stocks are also influenced by popular opinion, and our code can reflect those with minor improvements. We'd also love to improve the graphical interface and make it more aesthetically pleasing. Overall, we are proud of our project, and feel as though we have achieved our core goal
