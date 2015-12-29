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
"""Color nicks"""
import hexchat


__module_name__ = 'nickcolor'
__module_author__ = 'bd808'
__module_version__ = '0.0.1'
__module_description__ = 'Color nicks'


events = (
    'Channel Action',
    'Channel Action Highlight',
    'Channel Message',
    'Channel Msg Hilight',
)


def clean_nick(nick):
    return nick.lower().rstrip('`_').split('|', 2)[0].split('{', 2)[0].split('[', 2)[0]


def color_nick(nick):
    nick = hexchat.strip(nick)
    return '\003{:02d}{}'.format(1 + hash(clean_nick(nick)) % 15, nick)


def on_print_attrs(word, word_eol, userdata, attributes):
    if word[0].startswith('\003'):
        return hexchat.EAT_NONE
    word[0] = color_nick(word[0])
    hexchat.emit_print(userdata, *word, time=attributes.time)
    return hexchat.EAT_ALL


# Install plugin
for event in events:
    hexchat.hook_print_attrs(event, on_print_attrs, event,
        priority=hexchat.PRI_HIGHEST)
hexchat.prnt('{0} {1} by {2} loaded.'.format(
    __module_name__, __module_version__, __module_author__))
