#coding=utf-8
import urllib,urllib2
import re
def getUrlList(page):
    req=urllib2.Request('http://www.budejie.com/video/%d' %page)
    req.add_header('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36')
    res=urllib2.urlopen(req)
    html=res.read()
    res=r'data-mp4="(.*?)">'
    urllist=re.findall(res,html)
    for url in urllist:
        urllib.urlretrieve(url,'mp4/%s.mp4' %url.split('/')[-1])

for page in xrange(1000):
    getUrlList(page+1)