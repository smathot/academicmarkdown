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

def DOI(s):
	
	"""
	Creates hyperlinks from DOI references.
	
	Arguments:
	s		--	A unicode string.
	
	Returns:
	A unicode string with all DOIs changed into hyperlinks.
	"""
	
	regexp = ur'(doi:10[.][0-9]{4,}[^\s"/<>]*/[^\s"<>]+)'
	for i in re.finditer(regexp, s, re.M):
		doi = i.group()
		s = s.replace(doi, u'<a href="http://dx.doi.org/%s">%s</a>' % \
			(doi[4:], doi))
	return s