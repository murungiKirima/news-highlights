import urllib.request
import json
from .models import Sources, Articles
from datetime import datetime

api_key = None
sources_base_url = None
articles_url = None


def configure_request(app):
    global api_key,sources_base_url, articles_url
    api_key = app.config['NEWS_API_KEY']
    sources_base_url = app.config['SOURCES_BASE_URL']
    articles_url = app.config['ARTICLES_URL']

def get_sources(category):
    get_sources_url = sources_base_url.format(category,api_key)
    with urllib.request.urlopen(get_sources_url) as url:
        get_sources_data = url.read()
        get_sources_response = json.loads(get_sources_data.decode("utf-8"))

        sources_results = None

        if get_sources_response['sources']:
            sources_results_list = get_sources_response['sources']
            sources_results = process_results(sources_results_list)

    return sources_results

def process_results(sources_list):
    sources_results = []
    for source_item in sources_list:
        id = source_item.get('id')
        name = source_item.get('name')
        description = source_item.get('description')
        url = source_item.get('url')
        category = source_item.get('category')
        language = source_item.get('language')
        country = source_item.get('country')

        source_object = Sources(id,name,description,url,category,language,country)
        sources_results.append(source_object)

    return sources_results

def get_articles(id):
    get_article_location_url = articles_url.format(id,api_key)
    print(get_article_location_url)

    with urllib.request.urlopen(get_article_location_url) as url:
        articles_location_data = url.read()
        articles_location_response = json.loads(articles_location_data.decode("utf-8"))

        articles_location_results = None

        if articles_location_response['articles']:
            articles_location_results = process_articles(articles_location_response['articles'])

    return articles_location_results

def process_articles(my_articles):
    article_location_list = []

    for article in my_articles:
        author = article.get('author')
        title = article.get('title')
        description = article.get('description')
        urlToImage = article.get('urlToImage')
        url = article.get('url')
        date = article.get('publishedAt')

        date = datetime(year=int(date[0:4]),month=int(date[5:7]),day=int(date[8:10]),hour=int(date[11:13]),minute=int(date[14:16]))

        if urlToImage:
            article_source_object = Articles(author,title,description,urlToImage,url,date)
            article_location_list.append(article_source_object)

    return article_location_list
