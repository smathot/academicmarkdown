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

from academicmarkdown import YAMLParser
import re

class TOCParser(YAMLParser):
	
	"""
	Interprets table of content command in YAML blocks of this type:
	
	%--
	toc:
	 maxdepth: 1
	 exclude: [Contents, Contact]
	--%
	"""
	
	def __init__(self, verbose=False):
		
		"""See YAMLParser.__init__()."""
		
		super(TOCParser, self).__init__(_object=u'toc', verbose=verbose)
	
	def parseObject(self, md, _yaml, d):
		
		"""See YAMLParser.parseObject()."""
		if u'exclude' not in d:
			d[u'exclude'] = []
		if u'maxdepth' not in d:
			d[u'maxdepth'] = 3			
		if u'mindepth' not in d:
			d[u'mindepth'] = 1		
		headers = []
		for i in re.finditer(r'^#(.*)', md, re.M):
			h = i.group()		
			if h.startswith(u'####'):
				level = 4
			elif h.startswith(u'###'):
				level = 3
			elif h.startswith(u'##'):
				level = 2
			elif h.startswith(u'#'):
				level = 1
			if level not in range(d[u'mindepth'], d[u'maxdepth']+1):
				continue
			label = h[level:].strip()
			# IDs should be lowercase alphanumeric strings with all spaces
			# replaced by dashes.
			_id = re.sub(ur'\W+', u' ', label).lower().replace(u' ', u'-')
			if label not in d[u'exclude']:
				headers.append( (level, h, label, _id) )
				self.msg(u'%s {#%s} (%d)' % (h, _id, level))

		_md = u'\n'
		for level, h, label, _id in headers:
			_md += u'\t' * (level-d[u'mindepth']) # Indent
			_md += u'- [%s](#%s)\n' % (label, _id)
		_md += u'\n'
		return md.replace(_yaml, _md)