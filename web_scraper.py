from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from typing import List
import pandas as pd
import re
import os

def remove_html_tags(text: str) -> str:
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', str(text))


def scrape_article_links(year: int) -> List[str]:
    """
    Scrape links of WBUR articles for a specified year
    param year: year for which WBUR articles will be scraped
    return: list of URLs
    """
    # Take into considerations leap years and days when no articles are published
    pass


def scrape_articles(urls: List[str]) -> List[str]:
    """
    Scrape contents of articles given the URLs
    param urls: list of urls
    param year: the year of the articles that will be scraped
    return: a list of articles
    """
    base_url = "https://www.wbur.org"
    articles = []
    
    for url in urls:
        url = f'{base_url}{url}'
        req = Request(url)
        html_page = urlopen(req)
        
        soup = BeautifulSoup(html_page, 'lxml')
        paragraphs = soup.find_all('p', class_="")
        
        # Removing HTML tags from text
        clean_text = []
        for paragraph in paragraphs:
            clean_text.append(remove_html_tags(paragraph))
            
        clean_str = ''.join(clean_text)
        
        articles.append(clean_str)
        
    return articles


def create_csv(articles: List[str], year: int) -> None:
    """
    Creates and saves a csv file containing a 
    single column for the scraped articles
    param articles: a list of articles
    return: None, saves the csv to disk
    """
    df = pd.DataFrame({
        'text': articles
    })
    
    df.to_csv(f'wbur{year}.csv')


test_scrape = scrape_articles(["/news/2014/01/01/family-homelessness", "/news/2014/01/01/james-avery", "/news/2014/01/01/woman-killed-in-boston-drawbridge-accident"])
test_csv = create_csv(test_scrape, 2014)

'''
# Opening the archive page that contains links to the articles that were published on 01/01/2014
req = Request("https://www.wbur.org/news/archive/2014/01/01")
html_page = urlopen(req)

# Parsing the HTML
soup = BeautifulSoup(html_page, "lxml")

# Getting all the links on the page
links = []
for link in soup.findAll('a'):
    links.append(link.get('href'))


# Only getting the links that contain "2014/01/01" since these would be the article links 
for link in links:
    if link != None:
        if "2014/01/01" in link:
            print(link)

# Opening the page of an article
req = Request("https://www.wbur.org/news/2014/01/01/james-avery")
html_page = urlopen(req)

# Parsing HTML
soup = BeautifulSoup(html_page, "lxml")

# Viewing the html
#print(soup.prettify())

# Saving all the paragraphs in a list
paragraphs = soup.find_all('p', class_="")

# Deleting the last paragraph since it is not a part of the article
del paragraphs[-1]

# Removing HTML tags from each paragraph
clean = []

for i in paragraphs:
    clean.append(remove_html_tags(i))

print(clean)

# Turning the list with all the paragraphs into a string
clean_paragraph = ''.join(clean)
print(clean_paragraph)

# Creating a txt file and saving all the paragraphs to it
f = open("avery.txt", 'w')
for i in clean:
    f.write(i)
f.close()
'''