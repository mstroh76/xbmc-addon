#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmcaddon
import xbmcplugin
import xbmcgui
import sys
import urllib, urllib2
import re
import HTMLParser

addon_handle = int(sys.argv[1])

def getVideolist(playlistID):
        xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_DATE)
        xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_LABEL)
        videolist_url = "http://gdata.youtube.com/feeds/api/playlists/" + str(playlistID)
        content = getUrl(videolist_url)
        spl=content.split('<entry>')
        for i in range(1,len(spl),1):
          entry=spl[i]
          match=re.compile("v=(.+?)&amp", re.DOTALL).findall(entry)
          id=match[0]
          match=re.compile("<title type='text'>(.+?)</title>", re.DOTALL).findall(entry)
          title=HTMLParser.HTMLParser().unescape(match[0])
          match=re.compile("<content type='text'>(.+?)</content>", re.DOTALL).findall(entry)
          desc=HTMLParser.HTMLParser().unescape(match[0])
          match=re.compile("<published>(.+?)T", re.DOTALL).findall(entry)
          splDate=match[0].split("-")
          date=splDate[2]+"."+splDate[1]+"."+splDate[0]
          thumb="http://img.youtube.com/vi/"+id+"/0.jpg"
          addLink(title,id,'playVideo',thumb,desc,date)
        xbmcplugin.endOfDirectory(addon_handle)


def getPlaylist():
        xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_DATE)
        xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_LABEL)
        content = getUrl("https://gdata.youtube.com/feeds/api/users/grazerlinuxtage/playlists")
        spl=content.split('<entry>')
        for i in range(1,len(spl),1):
          entry=spl[i]
          match=re.compile("<yt:playlistId>(.+?)</yt:playlistId>", re.DOTALL).findall(entry)
          id=match[0]
          match=re.compile("<title type='text'>(.+?)</title>", re.DOTALL).findall(entry)
          title=match[0]
          desc = title
          match=re.compile("<published>(.+?)T", re.DOTALL).findall(entry)
          splDate=match[0].split("-")
          date=splDate[2]+"."+splDate[1]+"."+splDate[0]
          addFolder(title,id,'showVideolist')
        xbmcplugin.endOfDirectory(addon_handle)

def playVideo(youtubeID):
        fullData = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=" + youtubeID
        listitem = xbmcgui.ListItem(path=fullData)
        return xbmcplugin.setResolvedUrl(addon_handle, True, listitem)

def getUrl(url):
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link

def addFolder(name,url,mode):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png")
        my_addon = xbmcaddon.Addon('plugin.video.grazerlinuxtage')
        liz.setProperty('fanart_image', my_addon.getAddonInfo('fanart'))
        ok=xbmcplugin.addDirectoryItem(handle=addon_handle,url=u,listitem=liz,isFolder=True)
        return ok

def addLink(name,url,mode,iconimage,desc,date):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": desc, "Date": date} )
        liz.setProperty('IsPlayable', 'true')
        my_addon = xbmcaddon.Addon('plugin.video.grazerlinuxtage')
        liz.setProperty('fanart_image', my_addon.getAddonInfo('fanart'))
        ok=xbmcplugin.addDirectoryItem(handle=addon_handle,url=u,listitem=liz)
        return ok

def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

params=parameters_string_to_dict(sys.argv[2])
mode=params.get('mode')
url=params.get('url')
if type(url)==type(str()):
  url=urllib.unquote_plus(url)

if mode == 'playVideo':
    playVideo(url)
elif mode == 'showVideolist':
    getVideolist(url)
else:
    getPlaylist()



