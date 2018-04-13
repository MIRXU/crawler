#coding=utf-8
import urllib
import re
import MySQLdb
sorts={
    1:'玄幻魔法',
    2:'武侠修真',
    3:'纯爱耽美',
    4:'都市言情',
    5:'职场校园',
    6:'穿越重生',
    7:'历史军事',
    8:'网游动漫',
    9:'恐怖灵异',
    10:'科幻小说',
    11:'美文名著',
    12:'热门推荐',
}
class sql(object):
    conn=MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='root',
        db='naveltest',
        charset='utf8'
    )
    def addnovel(self,sort,sortname,name,imgurl,description,staus,author):
        cur=self.conn.cursor()
        cur.execute('insert into novel(sort,sortname,name,imgurl,description,staus,author) values (%s,"%s","%s","%s","%s","%s","%s")' %(sort,sortname,name,imgurl,description,staus,author))
        lastrowid=cur.lastrowid
        cur.close()
        self.conn.commit()
        return lastrowid
    def addchapter(self,novelid,title,content):
        cur = self.conn.cursor()
        cur.execute(
            'insert into book(novelid,title,content) values (%s,"%s","%s")' %(novelid, title, content))
        cur.close()
        self.conn.commit()
mysql=sql()
def getChpterContent(url,title,lastrowid):
    html = urllib.urlopen(url).read().decode('gbk').encode('utf-8')
    reg = r'<script type="text/javascript">style5\(\);</script>(.*?)<script type="text/javascript">style6\(\);</script>'
    content=re.findall(reg,html,re.S)[0];
    mysql.addchapter(lastrowid,title,content)
    # print content
def getContent(url,lastrowid):
    html = urllib.urlopen(url).read().decode('gbk').encode('utf-8')
    reg = r'<DIV class="clearfix dirconone">(.*?)</DIV>'
    # reg = r'<li><a href="(.*?)" title=".*?">(.*?)</a></li>'
    # chapterInfo=re.findall(reg,html,re.S)
    chapterInfo=re.findall(reg,html,re.S)
    reg = r'<li><a href="(.*?)" title=".*?">(.*?)</a></li>'
    chapterInfo = re.findall(reg, chapterInfo[0], re.S)
    # print chapterInfo
    for url,title in chapterInfo:
        # print url,title
        getChpterContent(url,title,lastrowid)
        # break
def getOneBook(url,sortid,sortname):
    html = urllib.urlopen(url).read().decode('gbk').encode('utf-8')
    reg = r'<meta property="og:novel:book_name" content="(.*?)"/>'
    book_name = re.findall(reg, html)[0]
    reg = r'<meta property="og:description" content="(.*?)"/>'
    description = re.findall(reg, html,re.S)[0]
    reg = r'<meta property="og:image" content="(.*?)"/>'
    image = re.findall(reg, html, re.S)[0]
    reg = r'<meta property="og:novel:category" content="(.*?)"/>'
    category = re.findall(reg, html)[0]
    reg = r'<meta property="og:novel:author" content="(.*?)"/>'
    author = re.findall(reg, html)[0]
    reg = r'<meta property="og:novel:status" content="(.*?)"/>'
    status = re.findall(reg, html)[0]
    reg = r'<meta property="og:novel:latest_chapter_name" content="(.*?)"/>'
    latest_chapter_name = re.findall(reg, html)[0]
    reg = r'<meta property="og:novel:latest_chapter_url" content="(.*?)"/>'
    latest_chapter_url = re.findall(reg, html)[0]
    reg = r'<a href="(.*?)" class="reader"'
    chapterUrl = re.findall(reg, html)[0]
    # print book_name,description,image,category,author,status,latest_chapter_name,latest_chapter_url
    lastrowid=mysql.addnovel(sortid,sortname,book_name,image,description,status,author)
    # print chapterUrl
    getContent(chapterUrl,lastrowid)

def getAllBook(sortid,sortname,i):
    html=urllib.urlopen('http://www.quanshuwang.com/list/%d_%d.html' %(sortid,i)).read().decode('gbk').encode('utf-8')
    reg=r'<a target="_blank" href="(.*?)" class="l mr10">'
    booksurl=re.findall(reg,html)
    print booksurl
    for url in booksurl:
        getOneBook(url,sortid,sortname)
        # break



for sort in sorts.items():
    for i in range(1,100):
        getAllBook(sort[0],sort[1],i)
    # break