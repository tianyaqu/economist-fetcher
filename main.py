#encoding = utf8

import requests
from bs4 import BeautifulSoup
import asyncio,aiohttp
from io import open as iopen

async def fetch_async(url):
    proxies = 'http://127.0.0.1:8087'

    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'Referer':'http://www.economist.com/printedition/2017-02-18'
    }

    isText = True
    parts = url.split('.')
    if len(parts) > 0 :
        suffix = parts[-1].lower()
        if suffix == 'jpg' or suffix == 'png' or suffix == 'jpeg':
            isText = False

    data = None
    async with aiohttp.ClientSession() as session:
        async with session.get(url,proxy=proxies,headers=headers) as resp:
            if resp.status != 200:
                print('response not 200',url)
            else:
                if isText:
                    data = await resp.text()
                else :
                    data = await resp.read()
    return data

async def save(url):
    print('fetch and save',url)
    data =  await fetch_async(url)
    if not data :
        print('err fetch ',url,' no data')
        return
    name = url.split('/')[-1]
    #print(name,' ',len(r))
    with iopen(name, 'wb') as fw:
        fw.write(r)

async def parseArticle(url):
    request = await fetch_async(url)
    soup = BeautifulSoup(request,'html5lib')
    try:
        headline = soup.article.h1.text
    except:
        return
    print('------------------')
    print('title ',headline)

    imgBaseUrl = 'http://economist-archive.com'
    imgUrls = []
    for img in soup.article.find_all('img'):
        url = img['src']
        imgUrls.append(url)
        img['src'] = imgBaseUrl + '/' + url.split('/')[-1]

    await asyncio.gather(*[save(url) for url in imgUrls])

async def parseEdition(url):
    request = await fetch_async(url)
    baseUrl = 'http://www.economist.com'
    suffix = "/print"
    urls = []
    soup = BeautifulSoup(request,'html5lib')
    for item in soup.body.select('.main-content .list__item'):
        for child in item.children:
            if child['class']:
                sectionName = child['class'][0]
                if sectionName == 'list__title':
                    print('sec ',child.text)
                else:
                    urls.append(baseUrl + child['href'] + suffix)
        print('---') 

    return urls

async def fetchEdition(rootUrl):
    u = await parseEdition(rootUrl)
    return u

async def parseAnEdition(rootUrl):
    urls = await fetchEdition(rootUrl)
    await asyncio.gather(*[parseArticle(url) for url in urls])

def run():
    rootUrl = 'http://www.economist.com/printedition/2017-02-18'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(parseAnEdition(rootUrl))

if __name__ == '__main__':
    run()