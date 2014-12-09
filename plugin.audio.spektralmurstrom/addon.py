#!/usr/bin/python
# -*- coding: utf-8 -*-
from xbmcswift2 import Plugin
import urllib2
import urllib
import re
import HTMLParser

plugin = Plugin()

@plugin.route('/')
def index():
    items = [
        {'label': 'mur.strom', 
         'thumbnail': 'http://murstrom.at/wp-content/uploads/2012/11/murstorm_logo_transp3.png', 
         'path': plugin.url_for('get_podcasts', potcast_url='murstrom.at')
        },
        {'label': 'Spektral',
         'thumbnail': 'http://spektral.at/wp-content/uploads/podcasts/spektral_logo.png',  
         'path': plugin.url_for('get_podcasts', potcast_url='spektral.at')
        },
    ]
    return items

def monthToNum(date):
  return{
        'Jan' : "01",
        'Feb' : "02",
        'Mar' : "03",
        'Apr' : "04",
        'May' : "05",
        'Jun' : "06",
        'Jul' : "07",
        'Aug' : "08",
        'Sep' : "09", 
        'Oct' : "10",
        'Nov' : "11",
        'Dec' : "12"
  }[date]

def getUrl(url):
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link


@plugin.route('/get_podcasts/<potcast_url>/')
def get_podcasts(potcast_url):
    #content = getUrl("http://spektral.at/feed/podcast")
    #content = getUrl("http://murstrom.at/feed/podcast")
    content = getUrl('http://%s/feed/podcast' % potcast_url)
    items = []
    spl=content.split('<item>')
    for i in range(1,len(spl),1):
      entry=spl[i]
      match=re.compile("<enclosure url=\"(.+?)\" length", re.DOTALL).findall(entry)
      url=match[0]
      match=re.compile("length=\"(.+?)\" type=", re.DOTALL).findall(entry)
      size=match[0]
      match=re.compile("<itunes:author>(.+?)</itunes:author>", re.DOTALL).findall(entry)
      autor = HTMLParser.HTMLParser().unescape(match[0])
      match=re.compile("<itunes:duration>(.+?)</itunes:duration>", re.DOTALL).findall(entry)
      duration=0
      if len(match) > 0 :
        splDuration=match[0].split(":")
        if len(splDuration) == 3 :
          duration=int(splDuration[0])*3600+int(splDuration[1])*60+int(splDuration[2])
        elif len(splDuration) == 2 :
          duration=int(splDuration[0])*60+int(splDuration[1])
        elif len(splDuration) == 1 :
          duration=int(splDuration[0])
      match=re.compile("<title>(.+?)</title>", re.DOTALL).findall(entry)
      title=urllib2.unquote(match[0]).decode('utf8')
      title=HTMLParser.HTMLParser().unescape(title)
      match=re.compile("SP(.+?) ", re.DOTALL).findall(title)
      if len(match) > 0 :
        number = match[0]
      else:
        number = 0
      #Date format: Tue, 02 Sep 2014 14:36:12 +0000
      match=re.compile("<pubDate>(.+?)</pubDate>", re.DOTALL).findall(entry)
      splDate=match[0].split(" ")
      monthnum = monthToNum(splDate[2])
      date=splDate[1]+"."+monthnum+"."+splDate[3]
      year = splDate[3]
#      match=re.compile("<itunes:summary>(.+?)</itunes:summary>", re.DOTALL).findall(entry)
      match=re.compile("<itunes:subtitle>(.+?)</itunes:subtitle>", re.DOTALL).findall(entry)
      comment=urllib2.unquote(match[0]).decode('utf8')
      comment=HTMLParser.HTMLParser().unescape(comment)
      items.append({
        'label': title,
        'info': {
          'comment': comment,
          'date': date, 
          'year': year,  
          'genre': 'Podcast',
          'size': size,
          'duration': duration,
          'tracknumber': number,
          'artist': autor,
          'album': potcast_url,
        },
        'path': url,
        'is_playable': True,
      })
    return plugin.finish(items) 


if __name__ == '__main__':
    plugin.run()
