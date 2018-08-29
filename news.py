from newsapi import NewsApiClient
import os


# def obtain_news():
#     """Call News API to obtain immigration news"""

#     news_api = NewsApiClient(api_key=os.environ["NEWS_API_KEY"])

#     top_headlines = news_api.get_everything(q="immigration",
#                                             language="en",
#                                             sort_by="relevancy")

#     # dropdown with different searches

#     return [totalResults]


def obtain_news():
    """Call News API to obtain immigration news"""

    news_api = NewsApiClient(api_key=os.environ["NEWS_API_KEY"])

    all_articles = news_api.get_everything(q="immigration",
                                           language='en',
                                           sort_by='relevancy',
                                           page=1)

    return all_articles["articles"]



