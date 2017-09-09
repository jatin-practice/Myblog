"""
Individual pages
"""

from dominate import document
from dominate.tags import *
from pyteaser import SummarizeUrl
from flask import (
    Blueprint,
    g,
    render_template)

analytics = Blueprint('analytics', __name__)


urls = [
        'http://www.wired.com/',
        'http://www.nytimes.com/',
        'http://www.technologyreview.com/lists/technologies/2014/'
    ]

'''

from collections import defaultdict
from string import punctuation
import urllib2
from bs4 import BeautifulSoup
from app.summarytool import SummaryTool

@analytics.route('/')
def index():
    """main index page"""
    return render_template('index2.html', pages=g.pages.sorted[:3])
'''

def get_only_text(url):
    """ 
     return the title and the text of the article
     at the specified url
    """
    page = urllib2.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(page)
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return soup.title.text, text

@analytics.route('/analytics/')
def analytics_check():
    """about page"""
    global SummaryTool
    fs = SummaryTool()
    print "Dict is %s"%(fs.__dict__)
    for url in urls:
        feed_xml = urllib2.urlopen(url).read()
        feed = BeautifulSoup(feed_xml.decode('utf8'))
        to_summarize = map(lambda p: p.text, feed.find_all('guid'))

    for article_url in to_summarize[:5]:
        title, text = get_only_text(article_url)
        #headlines='\n'.join(str(line.encode('ascii', 'ignore')) for line in summaries)
        sentences_dic = st.get_senteces_ranks(text)
        headlines=st.get_summary(title, content, sentences_dic)
        with document(title='Analytics') as doc:
            h1(title)
            #print headlines
            h2(headlines)
    
    with open('templates/analytics.html', 'w') as f:
        f.write(doc.render())
    return render_template('analytics.html')

