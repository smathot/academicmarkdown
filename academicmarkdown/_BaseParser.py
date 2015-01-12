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
import yaml
from academicmarkdown.py3compat import *

class BaseParser(object):

	def __init__(self, verbose=False):

		"""
		Constructor.

		Keyword arguments:
		verbose		--	Indicates whether verbose output should be generated.
						(default=False)
		"""

		self.verbose = verbose

	def parse(self, md):

		"""
		Parses a MarkDown text.

		Arguments:
		md		--	The Markdown text.

		Returns:
		The parsed Markdown text.
		"""

		raise Exception(u'BaseParser.parse() should be overridden.')

	def msg(self, msg):

		"""
		Print output in verbose mode.

		Arguments:
		msg		--	The message to print.
		"""

		if self.verbose:
			print(safe_encode(u'[%s] %s' % (self.__class__.__name__, msg),
				enc=u'ascii', errors=u'ignore'))

	def getPath(self, path):

		"""
		Checks whether a path is present in the `srcFolder` and if so fixes it.
		URLs are accepted as valid paths.

		Arguments:
		path		--	A path.

		Returns:
		A path.
		"""

		import os
		from academicmarkdown import build
		if path.startswith(u'http://'):
			return path
		for buildPath in build.path:
			_path = os.path.join(buildPath, path)
			if os.path.exists(_path):
				return _path
		if not os.path.exists(path):
			raise Exception(u'Cannot find file %s' % path)
		return path
