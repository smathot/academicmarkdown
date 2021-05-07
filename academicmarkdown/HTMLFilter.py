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

def citationGlue(s):

	"""
	Glues citations together to allow sorting, like so:

		[@B]+[@A]

	This will put '@B' before '@A'.

	Returns:
	A unicode string with all citations glued.
	"""

	regexp = \
		r'[\]\)]</span>\+<span class="citation" data-cites="[\w +]+">[\[\(]'
	for i in re.finditer(regexp, s, re.M):
		cite = i.group()
		s = s.replace(i.group(), u'')
	return s

def DOI(s):

	"""
	Creates hyperlinks from DOI references.

	Arguments:
	s		--	A unicode string.

	Returns:
	A unicode string with all DOIs changed into hyperlinks.
	"""

	regexp = r'(doi:10[.][0-9]{4,}[^\s"/<>]*/[^\s"<>]+)'
	for i in re.finditer(regexp, s, re.M):
		doi = i.group()
		s = s.replace(doi, u'<a href="http://dx.doi.org/%s">%s</a>' % \
			(doi[4:], doi))
	return s

def headerIndent(s, depth=1, minLevel=1, maxLevel=6):

	"""
	Makes all headers jump down one level. For example <H1> becomes <H2>, etc.

	Arguments:
	s		--	A unicode string.

	Keyword arguments:
	depth		--	The depth of the extra indentation. For example, a depth of
					2 means that <h2> becomes <h4). (default=1)
	minLevel	--	The minimum header level to process. (default=1)
	maxLevel	--	The maximum header level to process. (default=6)

	Returns:
	A unicode string with indented headers.
	"""

	for i in range(maxLevel, minLevel-1, -1):
		s = s.replace(u'<h%d' % i, u'<h%d' % (i+depth)) \
			.replace(u'<H%d' % i, u'<H%d' % (i+depth)) \
			.replace(u'</h%d>' % i, u'</h%d>' % (i+depth)) \
			.replace(u'</H%d>' % i, u'</H%d>' % (i+depth))
	return s

def quote(s):
	
	s = s.replace('<p>—', '<p><span class="quote-dash">&#x2015;</span>')
	s = s.replace('<br />\n—', '<br />\n<span class="quote-dash">&#x2015;</span>')
	return s
