"""
Individual pages
"""

from dominate import document
from dominate.tags import *
import urllib2
from bs4 import BeautifulSoup
from pyteaser import SummarizeUrl
from flask import (
    Blueprint,
    g,
    render_template)

analytics = Blueprint('analytics', __name__)
from summarytool import SummaryTool
fs = SummaryTool()


urls = [
        'http://www.wired.com/',
        'http://www.nytimes.com/',
        'http://www.moneycontrol.com'
    ]

'''

from collections import defaultdict

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
    headlines=[]
    for url in urls:
        page = urllib2.urlopen(url).read().decode('utf8')
        soup = BeautifulSoup(page)
        title='Analytics'
        content = ' '.join(map(lambda p: p.text.encode('ascii', 'ignore'), soup.find_all('p')))
        #headlines='\n'.join(str(line.encode('ascii', 'ignore')) for line in summaries)
        sentences_dic = fs.get_senteces_ranks(content)
        summary=fs.get_summary(title, content, sentences_dic)
        headlines.append('%s\n'%(content))
    with document(title='Analytics') as doc:
        h1('Title')
        headline='\n'.join(str(line) for line in headlines)
        h2(headline)
    with open('templates/analytics.html', 'w') as f:
        f.write(doc.render())
    return render_template('analytics.html')

