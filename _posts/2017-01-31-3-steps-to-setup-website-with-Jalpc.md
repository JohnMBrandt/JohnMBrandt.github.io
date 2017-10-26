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

Let's learn how to do this.

1. 

``` python
from google import search
import requests
import re
import os
from googleapiclient.discovery import build
from pandas import DataFrame
```

2.
``` python
url_list = []
url_list_all_cities = []
list_of_cities = ['nashville', 'dallas']
list_of_cities_concat = [item.replace(' ', '') for item in list_of_cities]
```

3.
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

4. 
``` python
for item in list_of_cities:
    for url in google_results("%s climate action plan filetype:pdf" % item):
        url_list.append(url)
        if len(url_list) >=4:
            url_list_all_cities.append(url_list)
            url_list = []
            break
```


5. Enter into repository directory and edit following file list:

3. Push changes to your github repository and view your website, done!

From now on, you can post your blog to this website by creating md files at `post/` directory and push it to GitHub, you can clear files at this directory before you post blogs.

If you like this repository, I appreciate you star this repository. Please don't hesitate to mail me or post issues on GitHub if you have any questions. Hope you have a happy blog time!😊
