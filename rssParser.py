import feedparser
import socket
import urllib2
import os
import time
import pdfkit
from xhtml2pdf import pisa
#tuple of tuples (tupleception!)
#(Formatting code, name (only shown in python script), folder name, link)
feeds = [
    ("NYT","the New York Times - Africa","NYT-Africa","http://www.nytimes.com/services/xml/rss/nyt/Africa.xml"),
    ("NYT","the New York Times - Asia&Pacific","NYT-Asia&Pacific","http://www.nytimes.com/services/xml/rss/nyt/AsiaPacific.xml"),
    ("NYT","the New York Times - Europe","NYT-Europe","http://www.nytimes.com/services/xml/rss/nyt/Europe.xml"),
    ("NYT","the New York Times - Middle East","NYT-Middle East","http://www.nytimes.com/services/xml/rss/nyt/MiddleEast.xml"),
    ("NYT","the New York Times - US","NYT-US","http://rss.nytimes.com/services/xml/rss/nyt/US.xml"),
    ("NYT","the New York Times - Politics","NYT-Politics","http://www.nytimes.com/services/xml/rss/nyt/Politics.xml"),
    ("BBC","the BBC - World","BBC-World","http://feeds.bbci.co.uk/news/world/rss.xml"),
    ("BBC","the BBC - US/Canada","BBC-US&Canada","http://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml"),
    ("HuffPost","the Huffington Post - World","HuffPost-World","http://www.huffingtonpost.com/feeds/verticals/world/index.xml"),
    ("HuffPost","the Huffington Post - Politics","HuffPost-Politics","http://www.huffingtonpost.com/feeds/verticals/politics/index.xml"),
    ("AlJazeera","Al Jazeera","Al Jazeera","http://www.aljazeera.com/Services/Rss/?PostingId=2007731105943979989"),
    ("RT","the Russian Times","Russian Times","http://rt.com/rss/")
    
    
    
    ]
timeout = 120
socket.setdefaulttimeout(timeout)#For every feed...
while True:
    for (feed_type, feed_name, feed_abv, feed_url) in feeds:
        d = feedparser.parse(feed_url)
        newArticles = 0
        print "Checking " + feed_name
        #For every feed item
        for s in d.entries:
            
            try:
                import urllib2
                thingy = 0
                #Remove stupid url additions (usually rss referral analytics things)
                if (feed_type == "AlJazeera" or feed_type == "RT"): #Feeds w/o additions (good job guys)
                    thingy = len(s.link)
                if (feed_type == "NYT"):
                    thingy = s.link.index('?partner')
                if (feed_type == "HuffPost"):
                    thingy = s.link.index('?utm')
                if (feed_type == "BBC"):
                    bad = s.link.find('sport')
                    if not(bad == -1):
                        continue
                    bad = s.title.find('video:')
                    if not(bad == -1):
                        continue
                    thingy = s.link.find('#sa')
                #truncates title to first 50 letters
                filetitle = s.title[0:50]
                #remove bad characters
                keepcharacters = (' ','.','_','-')
                filetitle =  "".join(c for c in filetitle if c.isalnum() or c in keepcharacters).rstrip()
                #checks if article has been downloaded
                if not os.path.exists('extemp/' + feed_abv +'/' + filetitle + '.html'):
                    #New York Times formatting code
                    if (feed_type == "NYT"):
                        #all pages on one page
                        url = s.link[0:thingy] + "?pagewanted=all"
                        #open url
                        usock = urllib2.build_opener(urllib2.HTTPCookieProcessor).open(url)
                        #create directory
                        if not os.path.exists('extemp/' + feed_abv):
                            os.makedirs('extemp/' + feed_abv)
                        output = open('extemp/' + feed_abv +'/' + filetitle + '.html','wb')
                        temp = open('temp.html','wb')
                        test = usock.read()
                        doarticle = 'false'
                        hstart = test.find('<body')
                        #remove ads and stuff
                        if hstart == -1:
                            hstart = 0
                            doarticle = 'true'
                        spos = test.find('<div id="abColumn"')
                        if spos == -1:
                            spos = test.find('div id="aCol"')
                        epos = test.find('<!--close abColumn')
                        if epos == -1:
                            epos = test.find('<!-- end aCol')
                        #save page
                        print url
                        

                        if doarticle == 'false':
                            #known NYT format (normal article, The Lede)
                            output.write(test[0:hstart] + "<body>" + test[spos:epos] + "</body></html>")
                            temp.write(test)
                        else:
                            #unknown format
                            output.write(test)
                            temp.write(test)
                        #pdfkit.from_file('temp.html', filetitle + '.pdf')
                        
                    #BBC formatting code
                    elif (feed_type == "BBC"):
                        #print mode
                        url = s.link[0:thingy] + "?print=true"
                        #open url
                        usock = urllib2.build_opener(urllib2.HTTPCookieProcessor).open(url)
                        #create directory
                        if not os.path.exists('extemp/' + feed_abv):
                            os.makedirs('extemp/' + feed_abv)
                        #save page
                        output = open('extemp/' + feed_abv +'/' + filetitle + '.html','wb')
                        test = usock.read()
                        output.write(test)
                    #Russian Times formatting code
                    elif (feed_type == "RT"):
                        #print mode
                        url = s.link[0:thingy]
                        #open url
                        usock = urllib2.build_opener(urllib2.HTTPCookieProcessor).open(url)
                        #create directory
                        if not os.path.exists('extemp/' + feed_abv):
                            os.makedirs('extemp/' + feed_abv)
                        #save page
                        output = open('extemp/' + feed_abv +'/' + filetitle + '.html','wb')
                        test = usock.read()
                        output.write(test)
                    #Huffington Post formatting code
                    elif (feed_type == "HuffPost"):
                        #print mode
                        url = s.link[0:thingy] + "?view=print"
                        #open url
                        usock = urllib2.build_opener(urllib2.HTTPCookieProcessor).open(url)
                        #create directory
                        if not os.path.exists('extemp/' + feed_abv):
                            os.makedirs('extemp/' + feed_abv)
                        #save page
                        output = open('extemp/' + feed_abv +'/' + filetitle + '.html','wb')
                        test = usock.read()
                        output.write(test)
                    #Al Jazeera formatting code
                    elif (feed_type == "AlJazeera"):
                        #print mode
                        url = s.link[0:thingy]
                        #open url
                        usock = urllib2.build_opener(urllib2.HTTPCookieProcessor).open(url)
                        #create directory
                        if not os.path.exists('extemp/' + feed_abv):
                            os.makedirs('extemp/' + feed_abv)
                        #save page
                        output = open('extemp/' + feed_abv +'/' + filetitle + '.html','wb')
                        test = usock.read()
                        output.write(test)
                    
                    newArticles = newArticles + 1
            except:
                pass
        print str(newArticles) + " new articles found." + "\n"
    print "All feeds parsed, waiting 30 minutes..."
    time.sleep(1800)

                


