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
from academicmarkdown.py3compat import *
import subprocess
import shlex

class ExecParser(YAMLParser):

	"""
	The `exec` block inserts the return value of an external command in the
	text. For example, the following block embeds something like
	'Generated on 10/18/2013':

		%-- exec: "date +'Generated on %x'" --%
	"""

	def __init__(self, verbose=False):

		"""See YAMLParser.__init__()."""

		super(ExecParser, self).__init__(_object=u'exec', verbose=verbose)

	def parseObject(self, md, _yaml, d):

		"""See YAMLParser.parseObject()."""

		if not isinstance(d, basestring):
			return u'Expecting a string, not "%s"' % d
		self.msg(u'Command: %s' % d)
		if not py3:
			d = safe_encode(d)
		output = safe_decode(subprocess.check_output(shlex.split(d)))
		self.msg(u'Returns: %s' % output)
		return md.replace(_yaml, output)
