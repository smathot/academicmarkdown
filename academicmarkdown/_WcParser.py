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

from academicmarkdown.py3compat import *
from academicmarkdown import YAMLParser
import subprocess
import shlex

class WcParser(YAMLParser):

	"""
	The `wc` block insert the word count for a particular document. This is
	convenient if you have split the text across multiple documents, and want to
	have a separate word count for each document.

		%-- wc: method-section.md --%
	"""

	def __init__(self, verbose=False):

		"""See YAMLParser.__init__()."""

		super(WcParser, self).__init__(_object=u'wc', verbose=verbose)

	def parseObject(self, md, _yaml, d):

		"""See YAMLParser.parseObject()."""

		if not isinstance(d, str):
			return u'Expecting a string, not "%s"' % d
		s = safe_decode(open(self.getPath(d)).read())
		wc = str(len(s.split()))
		self.msg(u'Word count: %s words in %s' % (wc, d))
		return md.replace(_yaml, wc)
