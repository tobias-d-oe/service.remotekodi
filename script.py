#!/usr/bin/python

import os
import sys
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import json
import urllib
import httplib

__addon__ = xbmcaddon.Addon()
__addonID__ = __addon__.getAddonInfo('id')
__addonDir__            = __addon__.getAddonInfo("path")
__settings__   = xbmcaddon.Addon(id='service.remotekodi')
__addonname__ = __addon__.getAddonInfo('name')
__version__ = __addon__.getAddonInfo('version')
__path__ = __addon__.getAddonInfo('path')
__LS__ = __addon__.getLocalizedString
__icon__ = xbmc.translatePath(os.path.join(__path__, 'icon.png'))

WINDOW                  = xbmcgui.Window( 10000 )





################################################
# 
################################################
def parameters_string_to_dict(parameters):
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict



################################################
# 
################################################
def send_json_command_http(xbmc_host, xbmc_port, method, params=None, id=1, username='', password=''):
    command = {'jsonrpc': '2.0', 'method': method, 'id': id}
    if params is not None:
        command['params'] = params
        
    writeLog('Send JSON command to: %s' % (xbmc_host), level=xbmc.LOGNOTICE)
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




################################################
# 
################################################
def channel_switch_json_command(xbmc_host, xbmc_port, channelid):
    command = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "Player.Open",
        "params": {"item": {"channelid": channelid}}
        }    
        
    writeLog('Switch channel to %s on %s' % (channelid,xbmc_host), level=xbmc.LOGNOTICE)
    payload = json.dumps(command, ensure_ascii=False)
    payload.encode('utf-8')
        
    headers = {'Content-Type': 'application/json-rpc; charset=utf-8'}

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

################################################
# Gather current remote player ID
################################################
def currentremoteplayer(xbmc_host, xbmc_port):
    query = {
            "jsonrpc": "2.0",
            "method": "Player.GetActivePlayers",
            "id": 1
            }
    payload = json.dumps(query, ensure_ascii=False)
    payload.encode('utf-8')

    headers = {'Content-Type': 'application/json-rpc; charset=utf-8'}

    conn = httplib.HTTPConnection(xbmc_host, xbmc_port)
    conn.request('POST', '/jsonrpc', payload, headers)

    response = conn.getresponse()
    data = None
    if response.status == 200:
        data = response.read()

    conn.close()

    if data is not None:
        res = json.loads(data)
        try:
          return res['result'][0]['playerid']
        except:
          writeLog('Nothing playing....', level=xbmc.LOGNOTICE)

          for x in range(1, 5):
              kodiisenabled = __settings__.getSetting("kodienable.%s" % (str(x)))
              if kodiisenabled == "true":
                kodiip = __settings__.getSetting("kodiip.%s" % (str(x)))
                if xbmc_host == kodiip:
                  remotekodiname = __settings__.getSetting("kodiname.%s" % (str(x)))
        

          notifyheader="Remote Kodi PVR Info"
          notifymsg="No active Stream on Kodi: %s" % (remotekodiname)
          xbmc.executebuiltin('XBMC.Notification('+notifyheader+', '+notifymsg+' ,4000,'+__icon__+')')

          raise SystemExit
    else:
        return None

################################################
# Gather current remote player Type (1->Video,2->Audio)
################################################
def get_remote_player_type(xbmc_host, xbmc_port, playerid):
    query = {
            "jsonrpc": "2.0",
            "method": "Player.GetItem",
            "id": 1,
            "params": { "playerid" : playerid, "properties":["title", "album", "artist", "season", "episode", "showtitle", "tvshowid", "description"]}
            }

    payload = json.dumps(query, ensure_ascii=False)
    payload.encode('utf-8')

    headers = {'Content-Type': 'application/json-rpc; charset=utf-8'}

    conn = httplib.HTTPConnection(xbmc_host, xbmc_port)
    conn.request('POST', '/jsonrpc', payload, headers)

    response = conn.getresponse()
    data = None
    if response.status == 200:
        data = response.read()

    conn.close()

    if data is not None:
        return json.loads(data)['result']['item']['type']
    else:
        return None

################################################
# Gather what plays at the moment on remote kodi
################################################
def get_remote_player_channel_id(xbmc_host, xbmc_port, playerid):
    query = {
            "jsonrpc": "2.0",
            "method": "Player.GetItem",
            "id": 1,
            "params": { "playerid" : playerid, "properties":["title", "album", "artist", "season", "episode", "showtitle", "tvshowid", "description"]}
            }

    payload = json.dumps(query, ensure_ascii=False)
    payload.encode('utf-8')

    headers = {'Content-Type': 'application/json-rpc; charset=utf-8'}

    conn = httplib.HTTPConnection(xbmc_host, xbmc_port)
    conn.request('POST', '/jsonrpc', payload, headers)

    response = conn.getresponse()
    data = None
    if response.status == 200:
        data = response.read()

    conn.close()

    if data is not None:
        return json.loads(data)['result']['item']
    else:
        return None






################################################
# Gather current player ID
################################################
def currentplayer():
    query = {
            "jsonrpc": "2.0",
            "method": "Player.GetActivePlayers",
            "id": 1
            }
    res = json.loads(xbmc.executeJSONRPC(json.dumps(query, encoding='utf-8')))
    playerid = res['result'][0]['playerid']
    return playerid


################################################
# Gather current player Type (1->Video,2->Audio)
################################################
def get_player_type(playerid):
    query = {
            "jsonrpc": "2.0",
            "method": "Player.GetItem",
            "id": 1,
            "params": { "playerid" : playerid, "properties":["title", "album", "artist", "season", "episode", "showtitle", "tvshowid", "description"]}
            }
    res = json.loads(xbmc.executeJSONRPC(json.dumps(query, encoding='utf-8')))
    result = res['result']['item']['type']
    return result

################################################
# Gather what plays at the moment
################################################
def get_player_channel_id(playerid):
    query = {
            "jsonrpc": "2.0",
            "method": "Player.GetItem",
            "id": 1,
            "params": { "playerid" : playerid, "properties":["title", "album", "artist", "season", "episode", "showtitle", "tvshowid", "description"]}
            }
    res = json.loads(xbmc.executeJSONRPC(json.dumps(query, encoding='utf-8')))
    return res['result']['item']





################################################
# Logging Function
################################################
def writeLog(message, level=xbmc.LOGNOTICE):
        try:
            xbmc.log('[%s %s]: %s' % ( __addonID__,__version__,message.encode('utf-8')), level)
        except Exception:
            xbmc.log('[%s %s]: Fatal: Message could not displayed' % (__addonID__,__version__), xbmc.LOGERROR)

################################################
#                   M A I N
################################################



if len(sys.argv)>=3:
    addon_handle = int(sys.argv[1])
    params = parameters_string_to_dict(sys.argv[2])
    methode = urllib.unquote_plus(params.get('methode', ''))
    #num = urllib.unquote_plus(params.get('num', ''))
elif len(sys.argv)>1:
    params = parameters_string_to_dict(sys.argv[1])
    methode = urllib.unquote_plus(params.get('methode', ''))
    #num = urllib.unquote_plus(params.get('num', ''))
else:
    methode = None

### Stop All Kodis
if methode=='stopall':
  writeLog('STOPALL Kodis', level=xbmc.LOGNOTICE)
  notifyheader="Remote Kodi PVR Info"
  notifymsg="Stopping all Remote Kodis" 
  xbmc.executebuiltin('XBMC.Notification('+notifyheader+', '+notifymsg+' ,4000,'+__icon__+')')
  for x in range(1, 5):
      kodiisenabled = __settings__.getSetting("kodienable.%s" % (str(x)))
      if kodiisenabled == "true":
        kodiip = __settings__.getSetting("kodiip.%s" % (str(x)))
        try:
          send_json_command_http(kodiip, 80, "Player.Stop", params=[1], id=1)
        except:
          pass
### Stop All other Kodis
elif methode=='stopallother':
  writeLog('STOPALLOTHER Kodis', level=xbmc.LOGNOTICE)
  notifyheader="Remote Kodi PVR Info"
  notifymsg="Stopping all other Remote Kodis" 
  xbmc.executebuiltin('XBMC.Notification('+notifyheader+', '+notifymsg+' ,4000,'+__icon__+')')
  localip=xbmc.getIPAddress()
  for x in range(1, 5):
      kodiisenabled = __settings__.getSetting("kodienable.%s" % (str(x)))
      if kodiisenabled == "true":
        kodiip = __settings__.getSetting("kodiip.%s" % (str(x)))
        if localip != kodiip:
          try:
            send_json_command_http(kodiip, 80, "Player.Stop", params=[1], id=1)
          except:
            pass


### Play local stream on all Kodis
elif methode=='playalllocal':
  writeLog('PLAYALLLOCAL Kodis', level=xbmc.LOGNOTICE)
  CurrentPlayer=currentplayer()
  if str(CurrentPlayer)=="1":  
    PlayerType=get_player_type(CurrentPlayer)
    if PlayerType=="channel":
      CurrentChannel=get_player_channel_id(CurrentPlayer)  
      CurrentChannel=CurrentChannel['id']
      
      notifyheader="Remote Kodi PVR Info"
      notifymsg="Start current stream on all Remote Kodis" 
      xbmc.executebuiltin('XBMC.Notification('+notifyheader+', '+notifymsg+' ,4000,'+__icon__+')')
      localip=xbmc.getIPAddress()
      for x in range(1, 5):
        kodiisenabled = __settings__.getSetting("kodienable.%s" % (str(x)))
        if kodiisenabled == "true":
          kodiip = __settings__.getSetting("kodiip.%s" % (str(x)))
          if localip != kodiip:
            params = { 'item': { 'channelid': int(CurrentChannel) } }
            channel_switch_json_command(kodiip, 80, CurrentChannel)

### Send  local stream to remote Kodi
elif methode=='sendlocal':
  writeLog('SENDLOCAL stream to Kodis', level=xbmc.LOGNOTICE)
  CurrentPlayer=currentplayer()
  if str(CurrentPlayer)=="1":  
    PlayerType=get_player_type(CurrentPlayer)
    if PlayerType=="channel":
      CurrentChannel=get_player_channel_id(CurrentPlayer)  
      CurrentChannel=CurrentChannel['id']
      
      localip=xbmc.getIPAddress()
      dialog = xbmcgui.Dialog()
      dialogEntrys=[]
      for x in range(1, 5):
        kodiisenabled = __settings__.getSetting("kodienable.%s" % (str(x)))
        if kodiisenabled == "true":
          kodiip = __settings__.getSetting("kodiip.%s" % (str(x)))
          if localip != kodiip:
	    dialogEntrys.append(__settings__.getSetting("kodiname.%s" % (str(x))))
      ret = dialog.select("Sende Stream an Kodi:",dialogEntrys)

      num=0
      for x in range(1, 5):
        kodiisenabled = __settings__.getSetting("kodienable.%s" % (str(x)))
        if kodiisenabled == "true":
          kodiip = __settings__.getSetting("kodiip.%s" % (str(x)))
          if localip != kodiip:
            if ret == num:
              params = { 'item': { 'channelid': int(CurrentChannel) } }
              channel_switch_json_command(__settings__.getSetting("kodiip.%s" % (str(x))), 80, CurrentChannel)
              num += 1
            else:
              num += 1

### get remote stream to local Kodi
elif methode=='fetchremote':
  writeLog('FETCHREMOTE stream from Kodi', level=xbmc.LOGNOTICE)
  localip=xbmc.getIPAddress()
  dialog = xbmcgui.Dialog()
  dialogEntrys=[]
  for x in range(1, 5):
    kodiisenabled = __settings__.getSetting("kodienable.%s" % (str(x)))
    if kodiisenabled == "true":
      kodiip = __settings__.getSetting("kodiip.%s" % (str(x)))
      if localip != kodiip:
        dialogEntrys.append(__settings__.getSetting("kodiname.%s" % (str(x))))
  ret = dialog.select("Hole Stream von Kodi:",dialogEntrys)

  num=0
  for x in range(1, 5):
    kodiisenabled = __settings__.getSetting("kodienable.%s" % (str(x)))
    if kodiisenabled == "true":
      kodiip = __settings__.getSetting("kodiip.%s" % (str(x)))
      if localip != kodiip:
        if ret == num:
          remotekodiip=kodiip
          num += 1
        else:
          num += 1
  CurrentRemotePlayer=currentremoteplayer(remotekodiip,80)
  if str(CurrentRemotePlayer)=="1":  
    PlayerType=get_remote_player_type(remotekodiip,80,CurrentRemotePlayer)
    if PlayerType=="channel":
      CurrentRemoteChannel=get_remote_player_channel_id(remotekodiip,80,CurrentRemotePlayer)  
      CurrentChannel=CurrentRemoteChannel['id']
      params = { 'item': { 'channelid': int(CurrentChannel) } }
      channel_switch_json_command("127.0.0.1", 80, CurrentChannel)



elif methode=='main':
  writeLog('MAIN Menu', level=xbmc.LOGNOTICE)
  dialog = xbmcgui.Dialog()
  dialogEntrys=["Stoppe Stream auf allen Kodis","Stoppe Stream auf allen anderen Kodis","Starte Stream auf allen Kodis","Starte Stream auf bestimmtem Kodi","Hole Stream von Remote Kodi" ]
  ret = dialog.select("Remote Kodi",dialogEntrys)
  if ret==0:
    xbmc.executebuiltin('XBMC.RunScript(service.remotekodi,"?methode=stopall")')
  if ret==1:
    xbmc.executebuiltin('XBMC.RunScript(service.remotekodi,"?methode=stopallother")')
  if ret==2:
    xbmc.executebuiltin('XBMC.RunScript(service.remotekodi,"?methode=playalllocal")')
  if ret==3:
    xbmc.executebuiltin('XBMC.RunScript(service.remotekodi,"?methode=sendlocal")')
  if ret==4:
    xbmc.executebuiltin('XBMC.RunScript(service.remotekodi,"?methode=fetchremote")')
  

#else:
#  RezapLast=WINDOW.getProperty('ReZap.Last.1')

