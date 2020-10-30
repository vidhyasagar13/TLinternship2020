# TLinternship2020
## Find Articles relevant to COVID-19 Economic Impact

This article aims to find links that are relevant to having an economic impact due to COVID – 19.

This system is based on finding URLs that are available on the common crawl website.
The following were used: beautifulsoup, NLTK and Gensen and request library

The code can be broken down into 4 parts, which are explained on the basis of the function used:

# Definition of Functions

## Preparation of the source data: 

prepare_source_data-

For the preparation of the source data, the URLs that were involved with having an economic impact due to COVID 19 were manually selected and a dictionary was built.

## Isolating similar URLs: 

isSimilar-

This function was defined such that it could find the similarities between the source data and the URLs fetched from the common crawl website.
It works by tokenizing the sentences based on the words.
The threshold value was set at 0.8, which means that if the score in the similarity dictionary was above this threshold, the related article was relevant to our search criteria – economically impacted by COVID 19, using the NLTK library.

## Scraping and processing of websites:

get_text_from_html-

The website was scraped using requests library and this generated a html document. This html content was processed using beautifulsoup so that all the html tags were removed and the text from it was isolated.

## Generation of URLs:

get_urls:

The warc file from the commoncrawl website of the months March/Arpril 2020 were extracted and the webpages in this duration were considered.
These selected webpages were compared with the webpages in the source data using the Gensen library and the similar webpages were extracted.

These URLs were returned. 


# How to run this file:

The file has to be downloaded and can be executed by using Jupyter or any python supported IDE.
