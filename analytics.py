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
from summarytool import SummaryTool

global fs
fs = SummaryTool()


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
    for url in urls:
        page = urllib2.urlopen(url).read().decode('utf8')
        soup = BeautifulSoup(page)
        text = ' '.join(map(lambda p: p.text.encode('ascii', 'ignore'), soup.find_all('p')))
        print 'Text is %s'%(text)
        #headlines='\n'.join(str(line.encode('ascii', 'ignore')) for line in summaries)
        sentences_dic = fs.get_senteces_ranks(text)
        headlines=fs.get_summary(title, content, sentences_dic)
        with document(title='Analytics') as doc:
            h1('Title')
            #print headlines
            h2(headlines)
    
    with open('templates/analytics.html', 'w') as f:
        f.write(doc.render())
    return render_template('analytics.html')

