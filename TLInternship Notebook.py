#!/usr/bin/env python
# coding: utf-8

# <h1> Install required libraries </h1>

# In[1]:


import sys
get_ipython().system('{sys.executable} -m pip install langdetect')
get_ipython().system('{sys.executable} -m pip install beautifulsoup4')
get_ipython().system('{sys.executable} -m pip install nltk')
get_ipython().system('{sys.executable} -m pip install gensim')


# In[ ]:





# <h1> Import required libraries </h1>

# In[2]:


from warcio.archiveiterator import ArchiveIterator
from warcio.capture_http import capture_http
from bs4 import BeautifulSoup
from langdetect import detect
from nltk.tokenize import word_tokenize,sent_tokenize
import gensim
import re
import requests
import sys
import numpy as np


# In[3]:


import nltk
nltk.download('punkt')


# In[4]:


def prepare_source_data():
    content = ''
    source_url_list = ['https://www.brookings.edu/research/ten-facts-about-covid-19-and-the-u-s-economy/#:~:text=The%20COVID%2D19%20crisis%20also,(U.S.%20Census%20Bureau%202020a).',
                      'https://www.mckinsey.com/business-functions/risk/our-insights/covid-19-implications-for-business#',
                      'https://www.richmondfed.org/publications/research/econ_focus/2020/q2-3/feature1']
    for url in source_url_list:
        content += get_text_from_html(requests.get(url).text)
    
    file_docs = []
    tokens = sent_tokenize(content)
    for line in tokens:
        file_docs.append(line)
    
    gen_docs = [[w.lower() for w in word_tokenize(text)] 
            for text in file_docs]
    dictionary = gensim.corpora.Dictionary(gen_docs)
    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
    tf_idf = gensim.models.TfidfModel(corpus)
    sims = gensim.similarities.Similarity('workdir/',tf_idf[corpus],
                                        num_features=len(dictionary))
    
    return tf_idf, sims, dictionary, file_docs
    
  
        


# In[5]:


def isSimilar(text, tf_idf, sims, dictionary, file_docs):
    file2_docs = []
    
    tokens = sent_tokenize(text)
    
    for line in tokens:
        file2_docs.append(line)
        
    for line in file2_docs:
        query_doc = [w.lower() for w in word_tokenize(line)]
        query_doc_bow = dictionary.doc2bow(query_doc)
    query_doc_tf_idf = tf_idf[query_doc_bow]
    similarityList = [i>=0.5 for i in sims[query_doc_tf_idf]]
    if any(similarityList):
        return True
    return False


# In[6]:


def get_text_from_html(html_page):
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)
    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        # there may be more elements you don't want, such as "style", etc.
    ]

    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)

    return (output)


# In[7]:


def get_urls(tf_idf, sims, dictionary, file_docs):
    url_list = []
    file_name = "https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2020-16/segments/1585370490497.6/warc/CC-MAIN-20200328074047-20200328104047-00000.warc.gz"
    stream = None

    if file_name.startswith("http://") or file_name.startswith("https://"):
        stream = requests.get(file_name, stream=True).raw
    else:
        stream = open(file_name, "r+")

    for record in ArchiveIterator(stream):
        if len(url_list) > 1000:
            break
        contents = (
            record.content_stream()
                .read()
                .decode("utf-8", "replace")
        )
        contents = get_text_from_html(contents)
        try:
            if contents and detect(contents) == 'en':
                get_similarity = isSimilar(contents, tf_idf, sims, dictionary, file_docs)
                if get_similarity:
                    print(record.rec_headers.get_header('WARC-Target-URI'))
                    url_list.append(record.rec_headers.get_header('WARC-Target-URI'))
        except:
            continue
    return url_list


# In[8]:


tf_idf, sims, dictionary, file_docs = prepare_source_data()


# In[ ]:


get_urls(tf_idf, sims, dictionary, file_docs)


# In[ ]:




