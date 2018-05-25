from flask import render_template
from . import main
from ..requests import get_sources, get_articles
from ..models import Sources

@main.route('/')
def index():
    title = "Welcome to the News page."

    general = get_sources('general')
    technology = get_sources('technology')
    return render_template('index.html',title = title, general = general, technology = technology)

@main.route('/articles/<source_id>')
def articles(source_id):
    '''
    Function that returns articles based on their sources
    '''
    news_source = get_articles(source_id)
    title = 'Articles | News Articles'
    return render_template('articles.html', title = title, name = source_id, news = news_source)
