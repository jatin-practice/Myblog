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

from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
import urllib2
from bs4 import BeautifulSoup
from heapq import nlargest

class SummaryTool(object):

    # Naive method for splitting a text into sentences
    def split_content_to_sentences(self, content):
        content = content.replace("\n", ". ")
        return content.split(". ")

    # Naive method for splitting a text into paragraphs
    def split_content_to_paragraphs(self, content):
        return content.split("\n\n")

    # Caculate the intersection between 2 sentences
    def sentences_intersection(self, sent1, sent2):

        # split the sentence into words/tokens
        s1 = set(sent1.split(" "))
        s2 = set(sent2.split(" "))

        # If there is not intersection, just return 0
        if (len(s1) + len(s2)) == 0:
            return 0

        # We normalize the result by the average number of words
        return len(s1.intersection(s2)) / ((len(s1) + len(s2)) / 2)

    # Format a sentence - remove all non-alphbetic chars from the sentence
    # We'll use the formatted sentence as a key in our sentences dictionary
    def format_sentence(self, sentence):
        sentence = re.sub(r'\W+', '', sentence)
        return sentence

    # Convert the content into a dictionary <K, V>
    # k = The formatted sentence
    # V = The rank of the sentence
    def get_senteces_ranks(self, content):

        # Split the content into sentences
        sentences = self.split_content_to_sentences(content)

        # Calculate the intersection of every two sentences
        n = len(sentences)
        values = [[0 for x in xrange(n)] for x in xrange(n)]
        for i in range(0, n):
            for j in range(0, n):
                values[i][j] = self.sentences_intersection(sentences[i], sentences[j])

        # Build the sentences dictionary
        # The score of a sentences is the sum of all its intersection
        sentences_dic = {}
        for i in range(0, n):
            score = 0
            for j in range(0, n):
                if i == j:
                    continue
                score += values[i][j]
            sentences_dic[self.format_sentence(sentences[i])] = score
        return sentences_dic

    # Return the best sentence in a paragraph
    def get_best_sentence(self, paragraph, sentences_dic):

        # Split the paragraph into sentences
        sentences = self.split_content_to_sentences(paragraph)

        # Ignore short paragraphs
        if len(sentences) < 2:
            return ""

        # Get the best sentence according to the sentences dictionary
        best_sentence = ""
        max_value = 0
        for s in sentences:
            strip_s = self.format_sentence(s)
            if strip_s:
                if sentences_dic[strip_s] > max_value:
                    max_value = sentences_dic[strip_s]
                    best_sentence = s

        return best_sentence

    # Build the summary
    def get_summary(self, title, content, sentences_dic):

        # Split the content into paragraphs
        paragraphs = self.split_content_to_paragraphs(content)

        # Add the title
        summary = []
        summary.append(title.strip())
        summary.append("")

        # Add the best sentence from each paragraph
        for p in paragraphs:
            sentence = self.get_best_sentence(p, sentences_dic).strip()
            if sentence:
                summary.append(sentence)

        return ("\n").join(summary)

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
    fs = SummaryTool()
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

