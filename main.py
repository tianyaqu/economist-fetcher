#encoding = utf8

import requests
from bs4 import BeautifulSoup
import asyncio


async def fetch(url):
    proxies = {
        'http': 'http://127.0.0.1:8087',
    }

    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'Referer':'http://www.economist.com/printedition/2017-02-18'
    }

    r = requests.get(url, headers=headers,proxies=proxies)
    return r.text


async def parseArticle(url):
    text = await fetch(url)
    soup = BeautifulSoup(text,'html5lib')
    headline = soup.article.h1.text
    print('------------------')
    print(headline)
    for content in soup.article.select('.main-content'):
        print (content)

async def parseEdition(url):
    text = await fetch(url)
    baseUrl = 'http://www.economist.com'
    suffix = "/print"
    urls = []
    soup = BeautifulSoup(text,'html5lib')
    for item in soup.body.select('.main-content .list__item'):
        for child in item.children:
            if child['class']:
                sectionName = child['class'][0]
                if sectionName == 'list__title':
                    print('sec ',child.text)
                else:
                    #print child['href'],child.text
                    urls.append(baseUrl + child['href'] + suffix)
        print('---') 

    return urls

async def fetchEdition(rootUrl):
    u = await parseEdition(rootUrl)
    for url in u:
        await parseArticle(url)
'''
def run():
    proxies = {
        'http': 'http://127.0.0.1:8087',
    }

    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'Referer':'http://www.economist.com/printedition/2017-02-18'
    }

    baseUrl = 'http://www.economist.com'
    suffix = "/print"
    urls = []
    r = requests.get('http://www.economist.com/printedition/2017-02-18', headers=headers,proxies=proxies)
    soup = BeautifulSoup(r.text,'html5lib')
    for item in soup.body.select('.main-content .list__item'):
        for child in item.children:
            if child['class']:
                sectionName = child['class'][0]
                if sectionName == 'list__title':
                    print 'sec ',child.text
                else:
                    #print child['href'],child.text
                    urls.append(baseUrl + child['href'] + suffix)
        print '---' 

    for url in urls:
        print url
        text = fetch(url)
        parseArticle(text)
'''        
if __name__ == '__main__':
    #run()
    loop = asyncio.get_event_loop()
    tasks = [parseArticle(url) for url in ['http://www.economist.com/news/world-week/21717118-politics-week/print', 
        'http://www.economist.com/news/britain/21717088-task-recovering-past-errors-goes-and-co-op-bank-puts-itself-up-sale/print', 
        'http://www.economist.com/news/britain/21716932-word-warning-valentines-day-lovestruck-britons-are-losing-50m-year-dating-site/print']]
    loop.run_until_complete(asyncio.wait([fetchEdition('http://www.economist.com/printedition/2017-02-18')]))