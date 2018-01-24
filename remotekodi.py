'''
    RemoteKodi PVR Status for XBMC
    Copyright (C) 2017 TDOe

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
import xbmc,xbmcplugin,xbmcgui,xbmcaddon
import time
import os

__settings__   = xbmcaddon.Addon(id='service.remotekodi')
__cwd__        = __settings__.getAddonInfo('path')
__icon__       = os.path.join(__cwd__,"icon.png")
__scriptname__ = "Remotekodi PVR Info"

BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'lib' ) )
sys.path.append (BASE_RESOURCE_PATH)

from settings import *
from remkodi import *

global g_failedConnectionNotified


def initGlobals():
  global g_failedConnectionNotified

  g_failedConnectionNotified = False   
  settings_initGlobals()

def process_RemoteKodi():
  while not xbmc.abortRequested:
    fetchRemoteKodi()
    for i in range(1,30):
      time.sleep(1)
      if xbmc.abortRequested:
        break

def fetchRemoteKodi():
  global g_failedConnectionNotified
  
  while not xbmc.abortRequested:
    try:
      kodiip = __settings__.getSetting("kodiipwz")
      kodiisenabled = __settings__.getSetting("kodienablewz")   
      kodidisplayname = __settings__.getSetting("kodinamewz") 
      ret = remotekodi_fetch(kodiip, kodiisenabled, kodidisplayname)
    except:
      writeLog('Kodi %s not online, cleaning Property' % (kodidisplayname), level=xbmc.LOGDEBUG)
      xbmcgui.Window(10000).clearProperty('%s.channel' % (kodidisplayname))
      xbmcgui.Window(10000).clearProperty('%s.channellogo' % (kodidisplayname))
      xbmcgui.Window(10000).clearProperty('%s.title' % (kodidisplayname))
      xbmcgui.Window(10000).clearProperty('%s.kodiname' % (kodidisplayname))


    try:
      kodiip = __settings__.getSetting("kodiipsz")
      kodiisenabled = __settings__.getSetting("kodienablesz")   
      kodidisplayname = __settings__.getSetting("kodinamesz") 
      ret = remotekodi_fetch(kodiip, kodiisenabled, kodidisplayname)
    except:
      writeLog('Kodi %s not online, cleaning Property' % (kodidisplayname), level=xbmc.LOGDEBUG)
      xbmcgui.Window(10000).clearProperty('%s.channel' % (kodidisplayname))
      xbmcgui.Window(10000).clearProperty('%s.channellogo' % (kodidisplayname))
      xbmcgui.Window(10000).clearProperty('%s.title' % (kodidisplayname))
      xbmcgui.Window(10000).clearProperty('%s.kodiname' % (kodidisplayname))


    try:
      kodiip = __settings__.getSetting("kodiipkueche")
      kodiisenabled = __settings__.getSetting("kodienablekueche")   
      kodidisplayname = __settings__.getSetting("kodinamekueche") 
      ret = remotekodi_fetch(kodiip, kodiisenabled, kodidisplayname)
    except:
      writeLog('Kodi %s not online, cleaning Property' % (kodidisplayname), level=xbmc.LOGDEBUG)
      xbmcgui.Window(10000).clearProperty('%s.channel' % (kodidisplayname))
      xbmcgui.Window(10000).clearProperty('%s.channellogo' % (kodidisplayname))
      xbmcgui.Window(10000).clearProperty('%s.title' % (kodidisplayname))
      xbmcgui.Window(10000).clearProperty('%s.kodiname' % (kodidisplayname))

    try:
      kodiip = __settings__.getSetting("kodiipbad")
      kodiisenabled = __settings__.getSetting("kodienablebad")   
      kodidisplayname = __settings__.getSetting("kodinamebad") 
      ret = remotekodi_fetch(kodiip, kodiisenabled, kodidisplayname)
    except:
      writeLog('Kodi %s not online, cleaning Property' % (kodidisplayname), level=xbmc.LOGDEBUG)
      xbmcgui.Window(10000).clearProperty('%s.channel' % (kodidisplayname))
      xbmcgui.Window(10000).clearProperty('%s.channellogo' % (kodidisplayname))
      xbmcgui.Window(10000).clearProperty('%s.title' % (kodidisplayname))
      xbmcgui.Window(10000).clearProperty('%s.kodiname' % (kodidisplayname))

    remotekodi_active()



    g_failedConnectionNotified = True
    break
  return True

#MAIN - entry point
initGlobals()

#main loop
while not xbmc.abortRequested:
  #settings_setup()
  process_RemoteKodi()

