#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
This file is part of pseudorandom.

pseudorandom is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pseudorandom is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pseudorandom.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import unittest
import academicmarkdown
from academicmarkdown.py3compat import *
import importlib

class AcadamicMarkdownTest(unittest.TestCase):

	"""
	desc:
		Basic unit testing for academicmarkdown.
	"""

	def setUp(self):

		academicmarkdown.build.path += [os.path.join(self.dataFolder(),
			u'includes')]

	def dataFolder(self):

		return os.path.join(os.path.dirname(__file__), u'testdata')

	def getTestData(self, fname):

		with open(os.path.join(self.dataFolder(), fname)) as fd:
			s = fd.read()
		return safe_decode(s)

	def singleTest(self, path):

		clsName = path[:-8]
		print(u'testing %s' % clsName)
		cls = getattr(academicmarkdown, clsName)
		md = self.getTestData(path)
		l = md.split(u'===')
		inp = l[0]
		predOut = l[1].strip()
		realOut = cls().parse(inp).strip()
		self.assertTrue(predOut == realOut)

	def test_all(self):

		for path in os.listdir(self.dataFolder()):
			if not path.endswith(u'.test.md'):
				continue
			self.singleTest(path)

if __name__ == '__main__':
	unittest.main()
