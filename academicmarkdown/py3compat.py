# -*- coding: utf-8 -*-

"""
This file is part of zoteromarkdown.

zoteromarkdown is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

zoteromarkdown is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with zoteromarkdown.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys

if sys.version_info >= (3,0,0):
	py3 = True
	basestring = str
else:
	bytes = str
	str = unicode
	py3 = False

def safe_decode(s, enc='utf-8', errors='strict'):
	if isinstance(s, str):
		return s
	return s.decode(enc, errors)

def safe_encode(s, enc='utf-8', errors='strict'):
	if isinstance(s, bytes):
		return s
	return s.encode(enc, errors)

__all__ = ['py3', 'safe_decode', 'safe_encode']
if not py3:
	__all__ += ['str', 'bytes']
else:
	__all__ += ['basestring']
