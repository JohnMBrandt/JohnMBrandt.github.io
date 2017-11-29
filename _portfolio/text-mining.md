---
title: "Text Mining of Environmental Planning Documents"
excerpt: "Web scraping and text mining of planning documents to identify sustainable and equitable cities for Resilient by Design."
header:
  teaser: assets/images/rbd-th.png
sidebar:
  - title: "Role"
    image: /assets/images/avatar.jpg
    image_alt: "logo"
    text: "Modeling and visualization in R"
  - title: "Responsibilities"
    text: "GLS, NLS, brute-force modeling, cubic splines transformation"
---

``` python

from google import search
import requests
import re
import os
from googleapiclient.discovery import build


## get a list of urls to scrape

url_list = []
url_list_all_cities = []

list_of_cities = ['portland', 'seattle', 'sacramento', 'austin']
list_of_cities_concat = [item.replace(' ', '') for item in list_of_cities]


def google_results(query, **kwargs):
    service = build("customsearch", "v1",
                    developerKey="AIzaSyDwoWAK8OBZGbclC_i-szgLEvFR64chAt0")
    result = service.cse().list(
            q=query,
            cx='012461012779746623813:twmdhymemma', **kwargs
        ).execute()

    return result["items"]

for item in list_of_cities:
    for url in google_results('%s "climate action plan" 2014|2015|2016|2017 filetype:pdf' % item):
        url_list.append(url)
        if len(url_list) >=3:
            url_list_all_cities.append(url_list)
            url_list = []
            break
            
url_list_flattened = [val for sublist in url_list_all_cities for val in sublist]
urls = [li['link'] for li in url_list_flattened]
titles = [li['title'] for li in url_list_flattened]

# create a filename for the pdf

def get_filename(number):
    #return "%d.pdf" % number
    return list_of_cities[int(number/3)] + " %d" % number +".pdf"
filename_list = []

# download the pdf and attach the filename to it
for idx, url in enumerate(urls):
    r = requests.get(url, allow_redirects=True)
    filename = get_filename(idx)
    filename_list.append(filename)
    open(filename, 'wb').write(r.content)


#tika is a python/java wrapper for Tesseract
from tika import parser
import os

path = '/Users/johnbrandt/AnacondaProjects/'
files = os.listdir(path)
i = 1

# remove PDFs that failed to download
for file in files:
    if "pdf" in file:
        if os.path.getsize(file) < 50 * 1024:
            os.remove(file)

# create a list of files within the download folder
files = os.listdir(path)

# create a list of PDFs within that folder
pdf_files_in_folder = []
for url in files:
    if "pdf" in url.lower():
        pdf_files_in_folder.append(url)
    else:
        continue


#this creates a nested dictionary of tuples that must be flattened
#{{file.pdf {content :[(,)], metadata: {[(,)]}}}
text = {}
for file in pdf_files_in_folder:
    texttemp = (parser.from_file(file))
    text.update({file:texttemp})

#This is now a dictionary of tuples that still cannot be iterated over
content_list = {}
for k1,v1 in text.items():
    text_content = (k1,v1['content'])
    content_list.update({k1:text_content})

#finally, the dictionary of tuples is converted to a dictionary of strings like:
# {file:content}

content_list_final = {}
for k1, v1 in content_list.items():
    content_list_final.update({k1:v1[1]})
content_list_final.keys()

#clean up plain text by removing common formatting

content_cleaned = {}
for k,v in content_list_final.items():
    v = v.translate(str.maketrans('','','\n'))
    v = v.translate(str.maketrans('','','\n'))
    v = v.translate(str.maketrans('','','\t'))
    v = v.translate(str.maketrans('','','...'))
    v = v.translate(str.maketrans('','','|'))
    v = v.translate(str.maketrans('','','·'))
    v = v.translate(str.maketrans('','','—'))
    v = v.translate(str.maketrans('','',','))
    v = v.translate(str.maketrans('','','('))
    v = v.translate(str.maketrans('','',')'))
    v = v.translate(str.maketrans('','','='))
    v = v.lower()
    v = v.translate(str.maketrans('','','•'))
    v = v.translate(str.maketrans('','','\uf0b7'))
    v = v.translate(str.maketrans('','','»'))
    v = v.translate(str.maketrans('','','›'))
    v = v.translate(str.maketrans('','','_'))
    v = v.translate(str.maketrans('','','\xa0'))
    content_cleaned.update({k:v})

content_cleaned

#remove extremely long (> 20) and short (< 3) words

words_list = {}
for k, v in content_cleaned.items():
    words = v.split()
    words = [i for i in words if 3 <= len(i) <=20]
    words_list.update({k:words})

import nltk
import pprint

tokenizer = None
tagger = None

def init_nltk():
    global tokenizer
    global tagger
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|[^\w\s]+')
    tagger = nltk.UnigramTagger(nltk.corpus.brown.tagged_sents())

def tag(text):
    global tokenizer
    global tagger
    if not tokenizer:
        init_nltk()
    tokenized = tokenizer.tokenize(text)
    tagged = tagger.tag(tokenized)
    return tagged
dict_tagged = {}
def main():
    text = []
    for k,v in content_list_final.items():
        text = content_list_final["San Rafael HE.pdf"]
        text = text.lower()
        tagged = tag(text)    
        l = list(set(tagged))
        pprint.pprint(l)
        dict_tagged.update(l)
    

if __name__ == '__main__':
    main()

from pandas import DataFrame
from pandas import Series


l_series = Series(dict_tagged)
l_dataframe = DataFrame(l_series)
l_dataframe = l_dataframe.reset_index()
l_dataframe.columns = ['word', 'POS']

l_dataframe_rm = l_dataframe
l_dataframe_rm['word'].value_counts()

portland0 = content_list_final['San Rafael HE.pdf']
listofwords = portland0.split()
listofwordsSeries = Series(listofwords)
listoflongwords = []

#subset words that are 4 characters or more
def long_words(words):
    listoflongwords.append([i for i in words if len(i) >= 4])

long_words(listofwords)
listoflongwords_flattened = [val for sublist in listoflongwords for val in sublist]

#convert the >4 character words to a pandas dataframe 
df1 = DataFrame({'word': listoflongwords_flattened})
df2 = l_dataframe_rm.merge(df1, how="right")

df2['File'] = 'San Rafael'
df2['Type'] = 'Housing Element'
df2[:10]


final2 = final2.append(df2)
len(final2)

final2.to_csv("final2.csv")
```
