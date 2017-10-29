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


For this example we'll be using tika, a python-based java wrapper of a popular OCR package.
We import the package and then set the working directory for python to the location of the PDF files to be converted. We then create a list of all files in that path.

``` python
from tika import parser
import os

path = '/your/path/here/'
files = os.listdir(path)
```

Because we are only interested in converting the PDF files in the folder, we need to remove items from the "files" list that aren't a PDF. The easiest way to do this is to loop through the names of the files "for file in files:" and then checking if "pdf" is in the lowercase name of the file.
If it is, we append it to an empty list "pdf_files_in_folder", if it isn't, we simply skip it.

``` python
pdf_files_in_folder = []
for file in files:
    if "pdf" in file.lower():
        pdf_files_in_folder.append(file)
    else:
        continue
```       

This is the bulk of the processing for this example. We create a dictionary to receive the plain text, and then loop through every PDF file in the folder and parse out the characters, updating the dictionary with each new file.

``` python
text = {}
for file in pdf_files_in_folder:
    texttemp = (parser.from_file(file))
    text.update({file:texttemp})
```

The output is a dictionary of a dictionary of tuples. Python tuples are immutable objects, and we need to do a bit of data munging to get into a workable form. <br>

The first thing that we do is to un-nest the dictionary. The current output is of the form {file: {content: (a,b,c,d), metadata: (x,y,z)}}. We only need to consider the content, and so we pull that out by iterating over the key,value pairs in the nested dictionary. <br>

Afterwards, we convert the dictionary of tuples into a dictionary of strings.

``` python
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


``` python
words_list = {}
for k, v in content_list_final.items():
    words = v.split()
    words = [i for i in words if 3 <= len(i) <=20]
    words_list.update({k:words})
```


``` python
words_dataframe_wide = DataFrame.from_dict(words_list, orient="index")
words_dataframe_long = words_dataframe_wide.transpose()
words_dataframe_long
```
<!--{% include carto_pm10.html max-width="600px" %}-->
