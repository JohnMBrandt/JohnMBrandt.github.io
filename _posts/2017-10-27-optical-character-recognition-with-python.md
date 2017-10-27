---
layout: post
title:  "Optical character recognition (OCR) with python for text analysis"
date:   2017-10-27
desc: "No description"
keywords: "text analysis, OCR, pandas, python"
categories: [Python]
tags: [python, OCR]
icon: icon-html
---

## Coming soon


``` python
from tika import parser

path = '/your/path/here/'
files = os.listdir(path)

pdf_files_in_folder = []
for url in files:
    if "pdf" in url.lower():
        pdf_files_in_folder.append(url)
    else:
        continue

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
content_list_final

```
<!--{% include carto_pm10.html max-width="600px" %}-->
