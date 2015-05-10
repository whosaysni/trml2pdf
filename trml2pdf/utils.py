# coding: utf-8
# trml2pdf - An RML to PDF converter
# Copyright (C) 2003, Fabien Pinckaers, UCL, FSA
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import re
import reportlab


# length units table
LENGTH_UNITS = [
    (re.compile('^(-?[0-9\.]+)\s*in$'), reportlab.lib.units.inch),
    (re.compile('^(-?[0-9\.]+)\s*cm$'), reportlab.lib.units.cm),  
    (re.compile('^(-?[0-9\.]+)\s*mm$'), reportlab.lib.units.mm),
    (re.compile('^(-?[0-9\.]+)\s*$'), 1)
]


def text_get(node):
    """Extract text value from TEXT_NODE children for given node.
    """
    rc = ''
    for node in node.childNodes:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc


def unit_get(size_string):
    """Converts possibly unit-suffixed string into pt.
    """
    for pattern, multiplier in LENGTH_UNITS:
        res = pattern.search(size_string, 0)
        if res:
            return multiplier*float(res.group(1))
    return False


def tuple_int_get(node, attr_name, default=None):
    """Converts attribute value of given node/attr_name into a list of integers.
    """
    if not node.hasAttribute(attr_name):
        return default
    # XXX 0-prefixed value will be parsed as octal. XXX
    res = [int(x) for x in node.getAttribute(attr_name).split(',')]
    return res


def bool_get(value):
    """Converts text value into bool value.
    """
    return (str(value)=="1") or (value.lower()=='yes')


def attr_get(node, attrs, dict={}):
    """Correct attribute values for given node/attrs, applying conversion defined in dict.
    """
    res = {}
    for name in attrs:
        if node.hasAttribute(name):
            res[name] =  unit_get(node.getAttribute(name))
    for key in dict:
        if node.hasAttribute(key):
            if dict[key]=='str':
                res[key] = str(node.getAttribute(key))
            elif dict[key]=='bool':
                res[key] = bool_get(node.getAttribute(key))
            elif dict[key]=='int':
                res[key] = int(node.getAttribute(key))
    return res
