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

_globals = {}
img_nr = 0

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
		
		global img_nr

		if not isinstance(d, basestring):
			return u'Expecting a string, not "%s"' % d

		import sys
		try:
			from io import StringIO # Py 3
		except ImportError:
			from StringIO import StringIO # Py 2
		img = False
		code = d
		if d.endswith('\nplt.show()\n'):
			d = d[:-len('\nplt.show()\n')]
			img_nr += 1
			d = 'from matplotlib import pyplot as plt\nplt.clf()\n{}\nplt.savefig("img/{}.png")\n'.format(
				d,
				img_nr
			)
			img = True
		self.msg(u'Python: %s' % d)
		buffer = StringIO()
		sys.stdout = buffer
		if safe_str(d).startswith('# should-raise\n'):
			code = code.replace('# should-raise\n', '')
			try:
				exec('#-*- coding:utf-8 -*-\n%s' % safe_str(d), _globals)
			except Exception as e:
				print('{0}: {1}'.format(e.__class__.__name__, e))
				# import traceback
				# traceback.print_exc(file=buffer, limit=1)
			else:
				raise ValueError('Code should raise exception but didn\t')
		else:
			exec('#-*- coding:utf-8 -*-\n%s' % safe_str(d), _globals)
		sys.stdout = sys.__stdout__
		output = buffer.getvalue()
		self.msg(u'Returns: %s' % output)
		s = u"""
~~~ .python
%s
~~~
""" % safe_str(code)

		if output:
			s += """
__Output:__

~~~ .text
%s
~~~
""" % output
		if img:
			s += '\n![](/img/{}.png)\n'.format(img_nr)
		return md.replace(_yaml, s)
