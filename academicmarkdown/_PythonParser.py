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

class PythonParser(YAMLParser):

	"""
	The `python` block embeds the output (i.e. whatever is printed to stdout)
	of a Python script into your document. For example, the following block
	embeds the docstring of the `PythonParser` class (i.e. what you're reading
	now):

		%--
		python: |
		 import inspect
		 from academicmarkdown import PythonParser
		 print inspect.getdoc(PythonParser)
		--%

	Note that the `|` symbol is YAML syntax, and allows you to have a multiline
	string.
	"""

	def __init__(self, verbose=False):

		"""See YAMLParser.__init__()."""

		super(PythonParser, self).__init__(_object=u'python', verbose=verbose)

	def parseObject(self, md, _yaml, d):

		"""See YAMLParser.parseObject()."""

		if not isinstance(d, basestring):
			return u'Expecting a string, not "%s"' % d

		import sys
		from StringIO import StringIO
		self.msg(u'Python: %s' % d)
		buffer = StringIO()
		sys.stdout = buffer
		exec('#-*- coding:utf-8 -*-\n%s' % safe_encode(d))
		sys.stdout = sys.__stdout__
		output = buffer.getvalue()
		self.msg(u'Returns: %s' % output)
		return md.replace(_yaml, output)
