#!/usr/bin/python
# -*- coding: utf-8 -*-
import xbmcaddon
import xbmcplugin
import xbmcgui
import sys
import urllib, urllib2
import re
import HTMLParser
import json

addon_handle = int(sys.argv[1])
YOUTUBE_API_KEY = 'AIzaSyCaIdMLBX3t5GOcGGT5eylioJf0u_7m-Xo'
YOUTUBE_CHANNEL_ID = 'UCSu2KcsxpEPSDru1LlTkpGQ'

def getVideolist(playlistID):
        xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_DATE)
        xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_LABEL)
        videolist_url='https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=%s&maxResults=50&key=%s'%(playlistID,YOUTUBE_API_KEY)
        #https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=PLWHx0EvwLLUFBeI_t8RDyyCxZirzoK4ua&maxResults=50&key=AIzaSyCaIdMLBX3t5GOcGGT5eylioJf0u_7m-Xo
        
        content = getUrl(videolist_url)
        decoded_data=json.loads(content)
        for Index in range(0, len(decoded_data['items'])):
          id=decoded_data['items'][Index]['snippet']['resourceId']['videoId']
          title=decoded_data['items'][Index]['snippet']['title']
          desc=decoded_data['items'][Index]['snippet']['description']
          thumb=decoded_data['items'][Index]['snippet']['thumbnails']['high']['url']
          dategoogle=decoded_data['items'][Index]['snippet']['publishedAt']
          match=re.compile('(.+?)-(.+?)-(.+?)T(.+?):(.+?):(.+?)\.(.+?)Z', re.DOTALL).findall(dategoogle)
          date=match[0][2] + '.' + match[0][1] + '.' + match[0][0] 
          addLink(title,id,'playVideo',thumb,desc,date)
        xbmcplugin.endOfDirectory(addon_handle)

def getPlaylist():
        xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_DATE)
        xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_LABEL)
        req_url='https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId=%s&maxResults=50&key=%s'%(YOUTUBE_CHANNEL_ID,YOUTUBE_API_KEY)
        
        content = getUrl(req_url)
        decoded_data=json.loads(content)
        for Index in range(0, len(decoded_data['items'])):
          id=decoded_data['items'][Index]['id']
          title=decoded_data['items'][Index]['snippet']['title']
          desc=decoded_data['items'][Index]['snippet']['description']
          dategoogle=decoded_data['items'][Index]['snippet']['publishedAt']
          addFolder(title,id,'showVideolist')
        xbmcplugin.endOfDirectory(addon_handle)

def playVideo(youtubeVideoID):
        fullData = "plugin://plugin.video.youtube/play/?video_id=" + youtubeVideoID
        listitem = xbmcgui.ListItem(path=fullData)
        listitem.setProperty('IsPlayable', 'true')
        return xbmcplugin.setResolvedUrl(addon_handle, True, listitem)

def getUrl(url):
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link
        #return link.decode('utf-8')

def addFolder(name,url,mode):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png")
        my_addon = xbmcaddon.Addon('plugin.video.grazerlinuxtage')
        liz.setProperty('fanart_image', my_addon.getAddonInfo('fanart'))
        ok=xbmcplugin.addDirectoryItem(handle=addon_handle,url=u,listitem=liz,isFolder=True)
        return ok

def addLinkDirect(name,url,mode,iconimage,desc,date):
        u='plugin://plugin.video.youtube/play/?video_id='+url
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": desc, "Date": date} )
        liz.setProperty('IsPlayable', 'true')
        ok=xbmcplugin.addDirectoryItem(handle=addon_handle,url=u,listitem=liz)
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
