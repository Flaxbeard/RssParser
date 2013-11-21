import feedparser
import socket
import urllib2
import os
feeds = [
    ("NYT","the New York Times - Africa","NYT-Africa","http://www.nytimes.com/services/xml/rss/nyt/Africa.xml"),
    ("NYT","the New York Times - Asia and the Pacific","NYT-Asia/Pacific","http://www.nytimes.com/services/xml/rss/nyt/AsiaPacific.xml"),
    ("NYT","the New York Times - Europe","NYT-Europe","http://www.nytimes.com/services/xml/rss/nyt/Europe.xml"),
    ("NYT","the New York Times - Middle East","NYT-Middle East","http://www.nytimes.com/services/xml/rss/nyt/MiddleEast.xml"),
    ("NYT","the New York Times - US","NYT-US","http://rss.nytimes.com/services/xml/rss/nyt/US.xml"),
    ("BBC","the BBC - World","BBC-World","http://feeds.bbci.co.uk/news/world/rss.xml")
    
    ]
timeout = 120
socket.setdefaulttimeout(timeout)
for (feed_type, feed_name, feed_abv, feed_url) in feeds:
    d = feedparser.parse(feed_url)
    newArticles = 0
    print "Checking " + feed_name
    for s in d.entries:

        
        import urllib2
        thingy = 0
        if (feed_type == "NYT"):
            thingy = s.link.index('?partner')
        if (feed_type == "BBC"):
            bad = s.link.find('sport')
            if not(bad == -1):
                continue
            bad = s.title.find('video:')
            if not(bad == -1):
                continue
            thingy = s.link.find('#sa')
        filetitle = s.title[0:50]
        keepcharacters = (' ','.','_','-')
        filetitle =  "".join(c for c in filetitle if c.isalnum() or c in keepcharacters).rstrip()
        if not os.path.exists('extemp/' + feed_abv +'/' + filetitle + '.html'):
            if (feed_type == "NYT"):
                url = s.link[0:thingy] + "?pagewanted=all"
                usock = urllib2.build_opener(urllib2.HTTPCookieProcessor).open(url)
                if not os.path.exists('extemp/' + feed_abv):
                    os.makedirs('extemp/' + feed_abv)
                output = open('extemp/' + feed_abv +'/' + filetitle + '.html','wb')
                test = usock.read()
                doarticle = 'false'
                hstart = test.find('<body')
                if hstart == -1:
                    hstart = 0
                    doarticle = 'true'
                spos = test.find('<div id="abColumn"')
                if spos == -1:
                    spos = test.find('div id="aCol"')
                epos = test.find('<!--close abColumn')
                if epos == -1:
                    epos = test.find('<!-- end aCol')
                if doarticle == 'false':
                    output.write(test[0:hstart] + "<body>" + test[spos:epos] + "</body></html>")
                else:
                    output.write(test)
            elif (feed_type == "BBC"):
                url = s.link[0:thingy] + "?print=true"
                usock = urllib2.build_opener(urllib2.HTTPCookieProcessor).open(url)
                if not os.path.exists('extemp/' + feed_abv):
                    os.makedirs('extemp/' + feed_abv)
                output = open('extemp/' + feed_abv +'/' + filetitle + '.html','wb')
                test = usock.read()
                output.write(test)
            newArticles = newArticles + 1
    print str(newArticles) + " new articles found." + "\n"

                


