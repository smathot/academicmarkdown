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
import subprocess
import shlex

class WcParser(YAMLParser):
	
	"""
	Interprets word-count commands in YAML blocks of this type:
	
	%--	wc: document.md --%
	"""
	
	def __init__(self, verbose=False):
		
		"""See YAMLParser.__init__()."""
		
		super(WcParser, self).__init__(_object=u'wc', verbose=verbose)
	
	def parseObject(self, md, _yaml, d):
		
		"""See YAMLParser.parseObject()."""
		
		if not isinstance(d, basestring):
			return u'Expecting a string, not "%s"' % d
		s = open(self.getPath(d)).read().decode(u'utf-8')
		wc = unicode(len(s.split()))		
		self.msg(u'Word count: %s words in %s' % (wc, d))
		return md.replace(_yaml, wc)
