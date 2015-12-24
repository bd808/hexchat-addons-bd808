# -*- coding: utf-8 -*-
# Copyright (c) 2015 Bryan Davis and contributors
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
"""De-empahasize messages from some senders"""
import fnmatch
import hexchat
import sys


__module_name__ = 'mute_senders'
__module_author__ = 'bd808'
__module_version__ = '0.0.1'
__module_description__ = 'De-empahasize messages from some senders'

muted = []
mute_color = '21'

hooks = []
events = {
    'Channel Action': '\035\t• {0} {1}',
    'Channel Action Highlight': '\035\t• {0} {1}',
    'Channel Message': '<{3}{2}{0}>\t{1}',
    'Channel Msg Hilight': '<{3}{2}{0}>\t{1}',
}


def save_config():
    """Save current settings to config file."""
    global muted
    global mute_color
    hexchat.set_pluginpref(__module_name__ + '_muted', ','.join(muted))
    hexchat.set_pluginpref(__module_name__ + '_color', mute_color)


def load_config():
    """Load settings from config file."""
    global muted
    global mute_color
    pref = hexchat.get_pluginpref(__module_name__ + '_muted')
    if pref:
        muted = pref.split(',')
    else:
        muted = []
    pref = hexchat.get_pluginpref(__module_name__ + '_color')
    if pref:
        mute_color = pref


def cmd_mute(word, word_eol, userdata):
    """/MUTE <nick> (shell-style wildcards accepted)
    eg: /MUTE *bot
    Display messaages from muted senders in plain format and muted color.
    See also: /help UNMUTE, /help LMUTE
    """
    global muted
    if len(word) != 2:
        hexchat.command('HELP ' + word[0])
        return hexchat.EAT_ALL
    muted = sorted(set(muted + [word[1]]), key=lambda x: x.strip('*'))
    save_config()
    hexchat.prnt('{0} will be muted.'.format(word[1]))
    return hexchat.EAT_ALL


def cmd_unmute(word, word_eol, userdata):
    """/UNMUTE <index>
    eg: /UNMUTE 0
    Remove a user from the muted senders list.
    See also: /help MUTE, /help LMUTE
    """
    global muted
    if len(word) != 2:
        hexchat.command('HELP ' + word[0])
        return
    idx = int(word[1])
    if idx < 0 or idx >= len(muted):
        hexchat.prnt('Index {0} invalid'.format(idx))
        return hexchat.EAT_ALL
    nick = muted[idx]
    del muted[idx]
    save_config()
    hexchat.prnt('{0} unmuted.'.format(nick))
    return hexchat.EAT_ALL


def cmd_lmute(word, word_eol, userdata):
    """/LMUTE <index>
    eg: /LMUTE
    Show the list of currently muted users
    See also: /help MUTE, /help UNMUTE
    """
    global muted
    hexchat.prnt('Muted nicks:')
    if not muted:
        hexchat.prnt('No muted nicks')
    else:
        hexchat.prnt('\n'.join(
            '{:<3}: {}'.format(i, n) for i, n in enumerate(muted)
        ))
    return hexchat.EAT_ALL


def on_print_attrs(word, word_eol, userdata, attributes):
    """Examine the message and alter the output if the sender is muted.

    :param word: List of message parts
    :param word_eol: Some other list of message parts?
    :param userdata: Name of the event that fired this callback
    :param attributes: Message attributes
    """
    global events
    global mute_color
    global muted
    # nick, text, mode, identified text (highlight)
    word = [(hexchat.strip(word[i]) if len(word) > i else '') for i in range(4)]
    for pat in muted:
        if fnmatch.fnmatch(word[0], pat):
            hexchat.prnt(
                '\003{}'.format(mute_color) + events[userdata].format(*word))
            return hexchat.EAT_ALL
    return hexchat.EAT_NONE


# Install plugin
load_config()
hexchat.hook_command('MUTE', cmd_mute, help=cmd_mute.__doc__)
hexchat.hook_command('UNMUTE', cmd_unmute, help=cmd_unmute.__doc__)
hexchat.hook_command('LMUTE', cmd_lmute, help=cmd_lmute.__doc__)
for event in events.keys():
    hexchat.hook_print_attrs(event, on_print_attrs, event)
hexchat.prnt('{0} {1} by {2} loaded.'.format(
    __module_name__, __module_version__, __module_author__))
