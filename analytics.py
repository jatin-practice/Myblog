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
@analytics.route('/')
def index():
    """main index page"""
    return render_template('index2.html', pages=g.pages.sorted[:3])
'''

@analytics.route('/analytics/')
def analytics_check():
    """about page"""
    for url in urls:
        summary=summaries = SummarizeUrl(url)
    with document(title='Analytics') as doc:
        h1('News Summary')
        print summary
    
    with open('templates/analytics.html', 'w') as f:
        f.write(doc.render())
    return render_template('analytics.html')

