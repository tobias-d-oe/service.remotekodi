'''
    Remotekodi PVR Info

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import platform
import xbmc
import xbmcgui
import xbmcaddon
import sys
import os
import re
import telnetlib
import urllib2
import json


__scriptname__ = sys.modules[ "__main__" ].__scriptname__
__settings__ = sys.modules[ "__main__" ].__settings__
__cwd__ = sys.modules[ "__main__" ].__cwd__
__icon__ = sys.modules[ "__main__" ].__icon__


__addon__     = xbmcaddon.Addon()
__addonID__   = __addon__.getAddonInfo('id')
__addonname__ = __addon__.getAddonInfo('name')
__version__   = __addon__.getAddonInfo('version')
__path__      = __addon__.getAddonInfo('path')
__LS__        = __addon__.getLocalizedString
__icon__      = xbmc.translatePath(os.path.join(__path__, 'icon.png'))




def writeLog(message, level=xbmc.LOGNOTICE):
        xbmc.log('[%s %s]: %s' % (__addonID__, __version__,  message.encode('utf-8')), level)




def remotekodi_active():
    if xbmcgui.Window(10000).getProperty('kodi.1.channel') == "" and xbmcgui.Window(10000).getProperty('kodi.2.channel') == "" and xbmcgui.Window(10000).getProperty('kodi.3.channel') == "" and xbmcgui.Window(10000).getProperty('kodi.4.channel') == "":
      xbmcgui.Window(10000).clearProperty('RemoteKodi.Active')
      writeLog('Remotekodi active        : False', level=xbmc.LOGDEBUG)

    else:
      xbmcgui.Window(10000).setProperty('RemoteKodi.Active', "True")  
      writeLog('Remotekodi active        : True', level=xbmc.LOGDEBUG)

  

def remotekodi_fetch(ip, isenabled, displayname, nr):
  import urllib2
  import urllib 

  if isenabled == "true":
    url = 'http://' + str(ip) + '/jsonrpc'
    data = json.dumps({"jsonrpc": "2.0", "method": "Player.GetItem", "params": { "properties": ["title", "album", "artist", "season", "episode", "duration", "showtitle", "tvshowid", "thumbnail", "file", "fanart", "streamdetails"], "playerid": 1 }, "id": "VideoGetItem"})
  
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('Content-Length', len(data))
    f = urllib2.urlopen(req, data)
    response = f.read()
    f.close()
    json_response = json.loads(response)
  
    label=json_response['result']['item']['label']
    title=json_response['result']['item']['title']
    thumbnail=json_response['result']['item']['thumbnail']
  
    if label != "":
      thumbnail=re.sub(r'^image://', '', thumbnail)
      thumbnail=re.sub(r'/$', '', thumbnail)
      thumbnail=urllib.unquote(thumbnail)

      writeLog('Set Label kodi.%s.channel     : %s' % (nr,label), level=xbmc.LOGDEBUG)
      xbmcgui.Window(10000).setProperty("kodi.%s.channel" % (nr), label)
      writeLog('Set Label kodi.%s.channellogo : %s' % (nr,thumbnail), level=xbmc.LOGDEBUG)
      xbmcgui.Window(10000).setProperty("kodi.%s.channellogo" % (nr), thumbnail)
      writeLog('Set Label kodi.%s.title       : %s' % (nr,title), level=xbmc.LOGDEBUG)
      xbmcgui.Window(10000).setProperty("kodi.%s.title" % (nr), title)
      writeLog('Set Label kodi.%s.kodiname    : %s' % (nr,displayname), level=xbmc.LOGDEBUG)
      xbmcgui.Window(10000).setProperty("kodi.%s.kodiname" % (nr), displayname)
    else:
      writeLog('Cleaning Property for Kodi : %s' % (displayname), level=xbmc.LOGDEBUG)
      xbmcgui.Window(10000).clearProperty('kodi.%s.channel' % (nr))
      xbmcgui.Window(10000).clearProperty('kodi.%s.channellogo' % (nr))
      xbmcgui.Window(10000).clearProperty('kodi.%s.title' % (nr))
      xbmcgui.Window(10000).clearProperty('kodi.%s.kodiname' % (nr))
  else:
    writeLog('Cleaning Property for Kodi : %s' % (displayname), level=xbmc.LOGDEBUG)
    xbmcgui.Window(10000).clearProperty('kodi.%s.channel' % (nr))
    xbmcgui.Window(10000).clearProperty('kodi.%s.channellogo' % (nr))
    xbmcgui.Window(10000).clearProperty('kodi.%s.title' % (nr))
    xbmcgui.Window(10000).clearProperty('kodi.%s.kodiname' % (nr))



def send_json_command(xbmc_host, xbmc_port, method, params=None, id=1, username='', password=''):
    command = {'jsonrpc': '2.0', 'method': method, 'id': id}
        
    if params is not None:
        command['params'] = params
        
    payload = json.dumps(command, ensure_ascii=False)
    payload.encode('utf-8')
        
    headers = {'Content-Type': 'application/json-rpc; charset=utf-8'}

    if password != '':
        userpass = base64.encodestring('%s:%s' % (username, password))[:-1]
        headers['Authorization'] = 'Basic %s' % userpass
        
    conn = httplib.HTTPConnection(xbmc_host, xbmc_port)
    conn.request('POST', '/jsonrpc', payload, headers)

    response = conn.getresponse()
    data = None
    if response.status == 200:
        data = response.read()
            
    conn.close()
        
    if data is not None:
        return json.loads(data)
    else:
        return None




#
#def stop_all_kodi():
#    
#    # Kodi Kuhstall
#    try:
#      send_json_command("192.168.0.70", 80, "Player.Stop", params=[1], id=1)
#    except:
#      pass
#    
#    # Kodi Kueche
#    try:
#      send_json_command("192.168.0.71", 80, "Player.Stop", params=[1], id=1)
#    except:
#      pass
#    # Kodi SZ
#    try:
#      send_json_command("192.168.0.72", 80, "Player.Stop", params=[1], id=1)
#    except:
#      pass
#    


def remotekodi_stop(ip, isenabled, displayname):
  import urllib2
  import urllib 

  if isenabled == "true":
    url = 'http://' + str(ip) + '/jsonrpc'
    data = json.dumps({"jsonrpc": "2.0", "method": "Player.Stop", "params": [1], "id": 1})
  
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('Content-Length', len(data))
    f = urllib2.urlopen(req, data)
    response = f.read()
    f.close()

def play_local_on_all(ip, isenabled, displayname):
  import urllib2
  import urllib 

  if isenabled == "true":
    url = 'http://' + str(ip) + '/jsonrpc'
    data = json.dumps({"jsonrpc": "2.0", "method": "Player.Stop", "params": [1], "id": 1})
  
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('Content-Length', len(data))
    f = urllib2.urlopen(req, data)
    response = f.read()
    f.close()

 
