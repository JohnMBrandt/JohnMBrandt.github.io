---
layout: post
title:  "Building a Simple Web Scraper with Python"
date:   2017-10-26
desc: "No description"
keywords: "easy, scraping, web, python"
categories: [Python]
tags: [webscraping, python]
icon: icon-html
---

In this post we are going to use the requests package in combination with google's API to build a Python program that will download PDFs based upon multiple google searches.

1. We begin by importing the relevant Python packages. All of these can be installed using conda install in terminal or through the Anaconda navigator. This post uses Python 3.

``` python
from google import search
import requests
import re
import os
from googleapiclient.discovery import build
from pandas import DataFrame
```

2. We begin by creating two empty lists, url_list and url_list_all_cities.
Replace or add onto the list_of_cities list with cities that you want to download documents from.
This tutorial grabs documents from Nashville and Dallas.
The last line of code just concatenates two word cities into one word.

``` python
url_list = []
url_list_all_cities = []
list_of_cities = ['nashville', 'dallas']
list_of_cities_concat = [item.replace(' ', '') for item in list_of_cities]
```

3. We now build our function to do a google search.

``` python
def google_results(query, **kwargs):
    service = build("customsearch", "v1",
                    developerKey="API KEY")
    result = service.cse().list(
            q=query,
            cx='API KEY, **kwargs
        ).execute()
        return result["items"]
```

4. Iterate over every city in the list_of_cities list and google the city name + a topic.
Replace "climate action plan" with whatever sort of plan you're interested in finding.

``` python
for item in list_of_cities:
    for url in google_results("%s climate action plan filetype:pdf" % item):
        url_list.append(url)
        if len(url_list) >=4:
            url_list_all_cities.append(url_list)
            url_list = []
            break
```


5. It's as simple as that - navigate to the folder with your python script and you should see the files appear as they download.

