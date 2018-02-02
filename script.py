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
        
    writeLog('DEBUG in send_json_command_http params: %s' % (command['params']), level=xbmc.LOGNOTICE)
    writeLog('DEBUG in send_json_command_http command: %s' % (command), level=xbmc.LOGNOTICE)
    payload = json.dumps(command, ensure_ascii=False)
    payload.encode('utf-8')
        
    writeLog('DEBUG in send_json_command_http PAYLOAD: %s' % (payload), level=xbmc.LOGNOTICE)
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
        writeLog('DEBUG have sent res is: %s' % (json.loads(data)), level=xbmc.LOGNOTICE)
        return json.loads(data)
    else:
        return None




################################################
# 
################################################
def channel_switch_json_command(xbmc_host, xbmc_port, channelid):
    #command = {'jsonrpc': '2.0', 'method': method, 'id': id}
    command = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "Player.Open",
        "params": {"item": {"channelid": channelid}}
        }    
        
    writeLog('DEBUG in channel_switch_json_command params: %s' % (command['params']), level=xbmc.LOGNOTICE)
    writeLog('DEBUG in channel_switch_json_command command: %s' % (command), level=xbmc.LOGNOTICE)
    payload = json.dumps(command, ensure_ascii=False)
    payload.encode('utf-8')
        
    writeLog('DEBUG in channel_switch_json_command PAYLOAD: %s' % (payload), level=xbmc.LOGNOTICE)
    headers = {'Content-Type': 'application/json-rpc; charset=utf-8'}

    conn = httplib.HTTPConnection(xbmc_host, xbmc_port)
    conn.request('POST', '/jsonrpc', payload, headers)

    response = conn.getresponse()
    data = None
    if response.status == 200:
        data = response.read()
            
    conn.close()
        
    if data is not None:
        writeLog('DEBUG have sent res is: %s' % (json.loads(data)), level=xbmc.LOGNOTICE)
        return json.loads(data)
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
  writeLog('DEBUG in STOPALL', level=xbmc.LOGNOTICE)
  notifyheader="Remote Kodi PVR Info"
  notifymsg="Stopping all Remote Kodis" 
  xbmc.executebuiltin('XBMC.Notification('+notifyheader+', '+notifymsg+' ,4000,'+__icon__+')')
  for x in range(1, 4):
      kodiisenabled = __settings__.getSetting("kodienable.%s" % (str(x)))
      writeLog('DEBUG in for loop %s : isenabled: %s' % (str(x),kodiisenabled), level=xbmc.LOGNOTICE)
      if kodiisenabled == "true":
        kodiip = __settings__.getSetting("kodiip.%s" % (str(x)))
        writeLog('DEBUG stop=True for: %s' % (str(kodiip)), level=xbmc.LOGNOTICE)
        try:
          send_json_command_http(kodiip, 80, "Player.Stop", params=[1], id=1)
        except:
          pass

### Play local stream on all Kodis
elif methode=='playalllocal':
  writeLog('DEBUG in PLAY ALL LOCAL', level=xbmc.LOGNOTICE)
  CurrentPlayer=currentplayer()
  writeLog('DEBUG in PLAY Current %s' % (str(CurrentPlayer)), level=xbmc.LOGNOTICE)
  if str(CurrentPlayer)=="1":  
    PlayerType=get_player_type(CurrentPlayer)
    writeLog('DEBUG in PLAY Type %s' % (str(PlayerType)), level=xbmc.LOGNOTICE)
    if PlayerType=="channel":
      CurrentChannel=get_player_channel_id(CurrentPlayer)  
      CurrentChannel=CurrentChannel['id']
      writeLog('DEBUG in PLAY Channel %s' % (str(CurrentChannel)), level=xbmc.LOGNOTICE)
      
      notifyheader="Remote Kodi PVR Info"
      notifymsg="Start current stream on all Remote Kodis" 
      xbmc.executebuiltin('XBMC.Notification('+notifyheader+', '+notifymsg+' ,4000,'+__icon__+')')
      for x in range(1, 4):
        kodiisenabled = __settings__.getSetting("kodienable.%s" % (str(x)))
        writeLog('DEBUG in PLAY for loop %s' % (str(x)), level=xbmc.LOGNOTICE)
        if kodiisenabled == "true":
          kodiip = __settings__.getSetting("kodiip.%s" % (str(x)))
          writeLog('DEBUG enable=True for: %s' % (str(kodiip)), level=xbmc.LOGNOTICE)
          params = { 'item': { 'channelid': int(CurrentChannel) } }
          channel_switch_json_command(kodiip, 80, CurrentChannel)
else:
  RezapLast=WINDOW.getProperty('ReZap.Last.1')

