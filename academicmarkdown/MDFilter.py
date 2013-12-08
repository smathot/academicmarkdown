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

import re

def autoItalics(md):
	
	"""
	Automatically italicizes certain expressions. For example, 'p = .05',
	becomes '*p* = .05'.
	
	Arguments:
	md		--	A Markdown string.
	
	Returns:
	A processed Markdown string.
	"""
	
	# M, SE, SD, p, r
	regexp = ur'(?P<key>(M|p|r|SE|SD)) *(?P<opr>[=><]) *(?P<val>-?\d*\.?\d*)'
	for i in re.finditer(regexp, md, re.M):
		old = i.group(0)
		new = u'*%s* %s %s' % (i.group('key'), i.group('opr'), \
			i.group('val'))
		md = md.replace(old, new)
		
	# T tests
	regexp = ur't\((?P<df>\d*\.?\d*)\) *(?P<opr>[=><]) *(?P<val>-?\d*\.?\d*)'
	for i in re.finditer(regexp, md, re.M):
		old = i.group(0)
		new = u'*t*(%s) %s %s' % (i.group('df'), i.group('opr'), \
			i.group('val'))
		md = md.replace(old, new)
		
	# F tests
	regexp = ur'F\((?P<df1>\d*\.?\d*),(?P<df2>\d*\.?\d*)\) *(?P<opr>[=><]) *(?P<val>-?\d*\.?\d*)'
	for i in re.finditer(regexp, md, re.M):
		old = i.group(0)
		new = u'*F*(%s,%s) %s %s' % (i.group('df1'), i.group('df2'), \
			i.group('opr'), i.group('val'))
		md = md.replace(old, new)
		
	return md

def magicVars(md):
	
	"""
	Replace magic variables, such as %wc%.
	
	Arguments:
	md		--	A Markdown string.
	
	Returns:
	A processed Markdown string.
	"""

	md = md.replace(u'%wc%', u'%s' % len(md.split()))
	md = md.replace(u'%cc%', u'%s' % len(md))
	return md
	
def pageBreak(md):
	
	"""
	Converts '~' paragraphs to HTML5 page breaks.
	
	Arguments:
	md		--	A Markdown string.
	
	Returns:
	A processed Markdown string.
	"""
	
	return md.replace(u'\n~\n', \
		u'\n<div style=\'page-break-before:always;\'></div>\n')