#encoding = utf8

import requests
from bs4 import BeautifulSoup


def fetch(url):
    proxies = {
        'http': 'http://127.0.0.1:8087',
    }

    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'Referer':'http://www.economist.com/printedition/2017-02-18'
    }

    r = requests.get(url, headers=headers,proxies=proxies)
    return r.text


def parseArticle(text):
    soup = BeautifulSoup(text,'html5lib')
    headline = soup.article.h1.text
    print '------------------'
    print headline
    for content in soup.article.select('.main-content'):
        print content

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
if __name__ == '__main__':
    run()