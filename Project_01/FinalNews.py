"""
--------------------------------------------------------------------------
Scraping News Headlines (from New York Times)
--------------------------------------------------------------------------
License:   
Copyright 2019 Irene Kwon

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
Software API:
    
    soup.find_all
      - Finds all instances of the search keys in the parentheses
    
    requests.get
      - Get/retrieve data from the given url
  
--------------------------------------------------------------------------
Background Information: 
 
    * Base code (adapted below):
        * https://stackoverflow.com/questions/55033291/scraping-headlines-from-news-website-homepages-using-beautifulsoup-in-python/
    * Information about libraries:
        * https://www.crummy.com/software/BeautifulSoup/bs4/doc/

--------------------------------------------------------------------------
Outline:
    
    - News headlines from New York Times
    - Scraping news headlines off of nytimes.com
    - Print the top 10 headlines
    
"""
#Import necessary packages
import requests 
from bs4 import BeautifulSoup
import json
import datetime
import textwrap

#Retrieve data from New York Times
url = "https://www.nytimes.com/"
r   = requests.get(url)
now = datetime.datetime.now()
now = now.strftime('%A, %B %d, %I:%M %p')

#Parse the script on the page
r_html = r.text
soup   = BeautifulSoup(r_html, "html.parser")

scripts = soup.find_all('script')
for script in scripts:
    if 'preloadedData' in script.text:
        jsonStr = script.text
        jsonStr = jsonStr.split('=', 1)[1].strip()
        jsonStr = jsonStr.rsplit(';', 1)[0]
        jsonObj = json.loads(jsonStr)

#Print header with the url and date
count   = 0
header  = ('%s\nHeadlines\n%s\n' %(url, now))
article = []

#Print the top 10 headlines
for ele, v in jsonObj['initialState'].items():
    try:
        if v['headline'][0] != '{':
            article.append(v['headline'])
            count += 1
    except:
        continue
    if count == 10:
        break

