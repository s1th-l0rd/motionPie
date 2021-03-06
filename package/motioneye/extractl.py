
# Copyright (c) 2015 Calin Crisan
# This file is part of motionPie.
#
# motionEye is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>. 

import logging
import os.path

from config import additional_config


MOTIONEYE_CONF = '/data/etc/motioneye.conf'
DATE_CONF = '/data/etc/date.conf'


def _get_motioneye_settings():
    port = 80
    motion_binary = '/usr/bin/motion'

    if os.path.exists(MOTIONEYE_CONF):
        logging.debug('reading motioneye settings from %s' % MOTIONEYE_CONF)

        with open(MOTIONEYE_CONF) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    name, value = line.split(' ', 1)

                except:
                    continue

                if name == 'port':
                    port = int(value)
                
                elif name == 'motion_binary':
                    motion_binary = value

    s = {
        'port': port,
        'motionBinary': motion_binary
    }
    
    logging.debug('motioneye settings: port=%(port)s, motion_binary=%(motionBinary)s' % s)

    return s


def _set_motioneye_settings(s):
    s = dict(s)
    s.setdefault('port', 80)
    s.setdefault('motionBinary', '/usr/bin/motion')
    
    logging.debug('writing motioneye settings to %s: ' % MOTIONEYE_CONF +
            'port=%(port)s, motion_binary=%(motionBinary)s' % s)

    lines = []
    if os.path.exists(MOTIONEYE_CONF):
        with open(MOTIONEYE_CONF) as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
    
            try:
                name, _ = line.split(' ', 2)
    
            except:
                continue
    
            if name == 'port':
                lines[i] = 'port %s' % s.pop('port')
    
            elif name == 'motion_binary':
                lines[i] = 'motion_binary %s' % s.pop('motionBinary')
    
    if 'port' in s:
        lines.append('port %s' % s.pop('port'))

    if 'motionBinary' in s:
        lines.append('motion_binary %s' % s.pop('motionBinary'))

    with open(MOTIONEYE_CONF, 'w') as f:
        for line in lines:
            if not line.strip():
                continue
            if not line.endswith('\n'):
                line += '\n'
            f.write(line)


def _get_date_settings():
    date_method = 'http'
    date_host = 'google.com'
    date_timeout = 10
    date_interval = 900

    if os.path.exists(DATE_CONF):
        logging.debug('reading date settings from %s' % DATE_CONF)
        
        with open(DATE_CONF) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                comment = False
                if line.startswith('#'):
                    line = line.strip('#')
                    comment = True
                
                if comment:
                    continue

                try:
                    name, value = line.split('=')
                    value = value.strip('"').strip("'")

                except:
                    continue

                if name == 'date_method':
                    date_method = value

                elif name == 'date_host':
                    date_host = value

                elif name == 'date_timeout':
                    date_timeout = int(value)

                elif name == 'date_interval':
                    date_interval = int(value)

    s = {
        'dateMethod': date_method,
        'dateHost': date_host,
        'dateTimeout': date_timeout,
        'dateInterval': date_interval
    }
    
    logging.debug('date settings: method=%(dateMethod)s, host=%(dateHost)s, timeout=%(dateTimeout)s, interval=%(dateInterval)s' % s)
    
    return s


def _set_date_settings(s):
    s.setdefault('dateMethod', 'http')
    s.setdefault('dateHost', 'google.com')
    s.setdefault('dateTimeout', 10)
    s.setdefault('dateInterval', 900)

    logging.debug('writing date settings to %s: ' % DATE_CONF +
            'method=%(dateMethod)s, host=%(dateHost)s, timeout=%(dateTimeout)s, interval=%(dateInterval)s' % s)

    with open(DATE_CONF, 'w') as f:
        f.write('date_method=%s\n' % s['dateMethod'])
        f.write('date_host=%s\n' % s['dateHost'])
        f.write('date_timeout=%s\n' % s['dateTimeout'])
        f.write('date_interval=%s\n' % s['dateInterval'])


@additional_config
def extraMotionEyeSeparator():
    return {
        'type': 'separator',
        'section': 'expertSettings',
        'advanced': True
    }


@additional_config
def port():
    return {
        'label': 'HTTP Port',
        'description': 'sets the port on which motionEye HTTP server listens',
        'type': 'number',
        'min': 1,
        'max': 65535,
        'section': 'expertSettings',
        'advanced': True,
        'reboot': True,
        'required': True,
        'get': _get_motioneye_settings,
        'set': _set_motioneye_settings,
        'get_set_dict': True
    }


@additional_config
def motionBinary():
    return {
        'label': 'Motion Binary',
        'description': 'sets the path to the motion binary',
        'type': 'str',
        'section': 'expertSettings',
        'advanced': True,
        'reboot': True,
        'required': True,
        'get': _get_motioneye_settings,
        'set': _set_motioneye_settings,
        'get_set_dict': True
    }


@additional_config
def dateMethod():
    return {
        'label': 'Date Method',
        'description': 'decides whether NTP or HTTP is used for setting and updating the system date',
        'type': 'choices',
        'choices': [('http', 'HTTP'), ('ntp', 'NTP')],
        'section': 'expertSettings',
        'advanced': True,
        'reboot': True,
        'required': True,
        'get': _get_date_settings,
        'set': _set_date_settings,
        'get_set_dict': True
    }


@additional_config
def dateHost():
    return {
        'label': 'Date HTTP Host',
        'description': 'sets the hostname or IP address to which the HTTP request will be made',
        'type': 'str',
        'section': 'expertSettings',
        'advanced': True,
        'reboot': True,
        'required': True,
        'depends': ['dateMethod==http'],
        'get': _get_date_settings,
        'set': _set_date_settings,
        'get_set_dict': True
    }


@additional_config
def dateTimeout():
    return {
        'label': 'Date Updating Timeout',
        'description': 'sets the timeout for the HTTP request',
        'type': 'number',
        'min': 1,
        'max': 3600,
        'unit': 's',
        'section': 'expertSettings',
        'advanced': True,
        'reboot': True,
        'required': True,
        'depends': ['dateMethod==http'],
        'get': _get_date_settings,
        'set': _set_date_settings,
        'get_set_dict': True
    }


@additional_config
def dateInterval():
    return {
        'label': 'Date Updating Interval',
        'description': 'sets the interval between system date updates',
        'type': 'number',
        'min': 10,
        'max': 86400,
        'unit': 's',
        'section': 'expertSettings',
        'advanced': True,
        'reboot': True,
        'required': True,
        'depends': ['dateMethod==http'],
        'get': _get_date_settings,
        'set': _set_date_settings,
        'get_set_dict': True
    }
