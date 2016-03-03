# -*- coding: utf-8 -*-
#
# PBFirstkill plugin for BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2015 PtitBigorneau - www.ptitbigorneau.fr
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

__author__  = 'PtitBigorneau www.ptitbigorneau.fr'
__version__ = '1.6'

import b3
import b3.plugin
import b3.events
from b3.functions import getCmd

class PbfirstkillPlugin(b3.plugin.Plugin):
    
    _adminPlugin = None
    _kill = 0
    _tk = 0
    _hs = 0
    _fkonoff = True
    _tkonoff = True
    _hsonoff = False
	
    def onLoadConfig(self):

        self._fkonoff = self.getSetting('settings', 'fkonoff', b3.BOOLEAN, self._fkonoff)
        self._tkonoff = self.getSetting('settings', 'tkonoff', b3.BOOLEAN, self._tkonoff)
        self._hsonoff = self.getSetting('settings', 'hsonoff', b3.BOOLEAN, self._hsonoff)

    def onStartup(self):

        self._adminPlugin = self.console.getPlugin('admin')
        
        if not self._adminPlugin:

            self.error('Could not find admin plugin')
            return False
        
        if 'commands' in self.config.sections():
            for cmd in self.config.options('commands'):
                level = self.config.get('commands', cmd)
                sp = cmd.split('-')
                alias = None
                if len(sp) == 2:
                    cmd, alias = sp

                func = getCmd(self, cmd)
                if func:
                    self._adminPlugin.registerCommand(self, cmd, level, func, alias)

        if self.console.gameName not in ('iourt41', 'iourt42', 'iourt43'):
		
            self.debug('cmd !firsths is available only in UrbanTerror')
            self._adminPlugin.unregisterCommand('firsths')
            self._hsonoff = False

        self.registerEvent('EVT_GAME_MAP_CHANGE', self.onMapChange)			
        self.registerEvent('EVT_CLIENT_KILL', self.onClientKill)
        self.registerEvent('EVT_CLIENT_KILL_TEAM', self.onClientKillTeam)

    def onMapChange(self, event):
        
        self._kill =0
        self._tk =0
        self._hs =0

    def onClientKill(self, event):

        self._kill += 1
            
        client = event.client
        target = event.target
            
        if self.console.gameName in ('iourt41', 'iourt42', 'iourt43'):
            
            weapon = event.data[1]
            hitlocation = event.data[2]
            
        else:
                
            weapon = 99
            hitlocation = 99
            self._hsonoff = "no"
           
        if weapon not in (23, 25):
                
            if self.console.gameName == 'iourt41':

                if hitlocation == "0" or hitlocation == "1":
                    
                    self._hs += 1

            if self.console.gameName in ('iourt42', 'iourt43'):

                if hitlocation == "1" or hitlocation == "2":
                    
                    self._hs += 1

        if self._fkonoff:

            if self._kill == 1:     
                
                if self.console.gameName in ('iourt41', 'iourt42', 'iourt43'):
                        
                    if self._hs == 1 and self._hsonoff:
                            
                        self.console.write('bigtext"^2First Kill ^5By Headshot ^3: %s killed %s"' % (client.exactName, target.exactName))
                        self._hs += 1
                        return
                        
                    else:

                        self.console.write('bigtext"^2First Kill ^3: %s killed %s"' % (client.exactName, target.exactName))

                elif self.console.gameName[:3] == 'cod':

                    self.console.say("^2First Kill ^3: %s killed %s" % (client.exactName, target.exactName))
                    
                else:

                    self.console.saybig("^2First Kill ^3: %s killed %s" % (client.exactName, target.exactName))

        if self._hsonoff:

            if self._kill == 1:

                return

            if self._hs == 1:     
  
                self.console.write('bigtext"^5First Kill ^5By Headshot ^3: %s killed %s"' % (client.exactName, target.exactName))
                self._hs += 1

    def onClientKillTeam(self, event):
	
        if self._tkonoff:
            
            self._tk += 1
            
            client = event.client
            target = event.target

            if self._tk == 1:
          
                if self.console.gameName in ('iourt41', 'iourt42', 'iourt43'):

                    self.console.write('bigtext"^1First TeamKill ^3:%s killed %s"' % (client.exactName, target.exactName))

                elif self.console.gameName[:3] == 'cod':

                    self.console.say("^1First TeamKill ^3:%s killed %s" % (client.exactName, target.exactName))
                
                else:

                    self.console.saybig("^1First TeamKill ^3:%s killed %s" % (client.exactName, target.exactName))
                
    def cmd_firstkill(self, data, client, cmd=None):
        
        """\
        activate / deactivate firstkill
        """
        
        if data:
            
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
        
            if self._fkonoff:

                client.message('firstkill ^2activated')

            if not self._fkonoff:

                client.message('firstkill ^1deactivated')

            client.message('!firstkill <on / off>')
            return

        if input[0] == 'on':

            if not self._fkonoff:

                self._fkonoff = True
                message = '^2activated'

            else:

                client.message('firstkill is already ^2activated') 

                return False

        if input[0] == 'off':

            if self._fkonoff:

                self._fkonoff = False
                message = '^1deactivated'

            else:
                
                client.message('firstkill is already ^1disabled')                

                return False

        client.message('firstkill %s'%(message))

    def cmd_firsttk(self, data, client, cmd=None):
        
        """\
        activate / deactivate first teamkill
        """
        
        if data:
            
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
        
            if self._tkonoff:

                client.message('first teamkill ^2activated')

            if not self._tkonoff:

                client.message('first teamkill ^1deactivated')

            client.message('!firsttk <on / off>')
            return

        if input[0] == 'on':

            if not self._tkonoff:

                self._tkonoff = True
                message = '^2activated'

            else:

                client.message('first teamkill is already ^2activated') 

                return False

        if input[0] == 'off':

            if self._tkonoff:

                self._tkonoff = False
                message = '^1deactivated'

            else:
                
                client.message('first teamkill is already ^1disabled')                

                return False

        client.message('first teamkill %s'%(message))

    def cmd_firsths(self, data, client, cmd=None):
        
        """\
        activate / deactivate first headshot
        """
        
        if self.console.gameName not in ('iourt41', 'iourt42', 'iourt43'):

            client.message("Command is available only in UrbanTerror")          
	
            return		

        if data:
            
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
        
            if self._hsonoff:

                client.message('first headshot ^2activated')

            if not self._hsonoff:

                client.message('first headshot ^1deactivated')

            client.message('!firsths <on / off>')
            return

        if input[0] == 'on':

            if not self._hsonoff:

                self._hsonoff = True
                message = '^2activated'

            else:

                client.message('first headshot is already ^2activated') 

                return False

        if input[0] == 'off':

            if self._hsonoff:

                self._hsonoff = False
                message = '^1deactivated'

            else:
                
                client.message('first headshot is already ^1disabled')

                return False

        client.message('first headshot %s'%(message))