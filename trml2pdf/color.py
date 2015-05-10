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
from reportlab.lib.colors import getAllNamedColors


# '(rrr, ggg, bbb)' format (where rrr/ggg/bbbb are digits of 0-255)
regex_t = re.compile('\(([0-9\.]*),([0-9\.]*),([0-9\.]*)\)')
# '#RRGGBB format (where RR/GG/BB are hexdigits of 00-FF)
regex_h = re.compile('#([0-9a-zA-Z][0-9a-zA-Z])([0-9a-zA-Z][0-9a-zA-Z])([0-9a-zA-Z][0-9a-zA-Z])')


def get(col_str, named_colors=getAllNamedColors()):
    """Looks up a color from given col_str.
    """
    if col_str in named_colors.keys():
        return named_colors[col_str]
    # try (rrr, ggg, bbb) format
    res = regex_t.search(col_str, 0)
    if res:
        return (float(res.group(1)),float(res.group(2)),float(res.group(3)))
    # try #RRGGBB format
    res = regex_h.search(col_str, 0)
    if res:
        return tuple([ float(int(res.group(i),16))/255 for i in range(1,4)])
    # Returns red on lookup failure.
    return colors.red
