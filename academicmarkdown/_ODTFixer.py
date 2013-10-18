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

import zipfile
from academicmarkdown import BaseParser
import re

class ODTFixer(BaseParser):
	
	def __init__(self, verbose=False):
		
		super(ODTFixer, self).__init__(verbose=verbose)
		
	def fix(self, path):
		
		self.msg(u'Fixing %s' % path)		
		self.msg(u'Reading ...')
		archive = zipfile.ZipFile(path, 'a')
		content = archive.read(u'content.xml').decode(u'utf-8')		
		# Style information is embedded as HTML comments, like so:
		# <!--odt-style="Style"-->. The style needs to be extracted and placed
		# into the <text:p text:style-name="Style"> tags that open a paragraph.
		# We also need to take into account that '<', '>'. and '"' characters
		# have been HTML-ized by pandoc.
		lines = []
		for line in content.split('\n'):
			for toStyle in re.findall( \
				ur'&lt;!--odt-style=&quot;(\w+)&quot;--&gt;', line):
				for fromStyle in re.findall( \
					ur'<text:p text:style-name="(\w+)">', line):
					line = line.replace(fromStyle, toStyle)
				line = line.replace(u'&lt;!--odt-style=&quot;%s&quot;--&gt;' \
					% toStyle, u'')
				self.msg(u'Changing style "%s" to "%s"' % (fromStyle, toStyle))
			lines.append(line)
		content = u'\n'.join(lines)
		
		#print content
		self.msg(u'Writing ...')
		archive.writestr('content.xml', content.encode(u'utf-8'))
		archive.close()
		self.msg(u'Done')