#coding=utf-8
from urllib import request
from urllib.request import urlretrieve
import re
def getUrlList(page):
    req=request.urlopen('http://www.budejie.com/video/%d' %page)
    req.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36')
    html=res.read()
    res=r'data-mp4="(.*?)">'
    urllist=re.findall(res,html)
    for url in urllist:
        urlretrieve(url,'mp4/%s.mp4' %url.split('/')[-1])

for page in range(1000):
    getUrlList(page+1)
