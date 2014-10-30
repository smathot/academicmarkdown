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

from academicmarkdown import YAMLParser, MDFilter
from academicmarkdown.constants import *
import os

class ConstantParser(YAMLParser):

	"""
	The `constant` block allows you to define constants. For example, if you
	define MyConstant1 (as below), all occurrences of "%MyConstant1" in the text
	will be replcated by "You can refer to this as %MyConstant1".

		%--
		constant:
			MyConstant1:	"You can refer to this as %MyConstant1"
			MyConstant2:	"You can refer to this as %MyConstant2"
		--%
	"""

	def __init__(self, verbose=False):

		"""See YAMLParser.__init__()."""

		super(ConstantParser, self).__init__(_object=u'constant',
			verbose=verbose)

	def parseObject(self, md, _yaml, d):

		"""See YAMLParser.parseObject()."""

		# Remove the YAML block
		md = md.replace(_yaml, u'')
		for key, val in d.items():
			self.msg(key)
			md = md.replace(u'%%%s' % key, val.strip())
		return md


