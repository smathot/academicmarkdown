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
from academicmarkdown import BaseParser

class YAMLParser(BaseParser):
	
	def __init__(self, _object, required=[], verbose=False):
		
		"""
		Constructor.
		
		Arguments:
		_object		--	Indicates which objects should be parsed.
		
		Keyword arguments:
		required	--	A list of required options in the YAML block.
						(default=[])
		verbose		--	Indicates whether verbose output should be generated.
						(default=False)
		"""
		
		self._object = _object
		self.required = required
		super(YAMLParser, self).__init__(verbose=verbose)
	
	def parse(self, md):
		
		"""See BaseParser.parse()."""
		
		for r in re.finditer(u'%--(.*?)--%', md, re.M|re.S):
			try:
				d = yaml.load(r.groups()[0])
			except:
				self.msg(u'Invalid YAML block: %s' % r.groups()[0])
				continue
			if not isinstance(d, dict):
				continue
			obj = list(d.keys())[0]
			if obj.lower() != self._object:
				continue
			keys = d[obj]
			for key in self.required:
				if key not in keys:
					raise Exception( \
						u'"%s" is a required option for %s objects' % (key, \
						self._object))
			md = self.parseObject(md, r.group(), keys)
		return md
	
	def parseObject(self, md, _yaml, d):
		
		"""
		Parses a specific YAML object found in a Markdown text.
		
		Arguments:
		md		--	The full markdown text.
		yaml	--	The yaml block.
		d		--	The yaml block already parsed into a dictionary.
		
		Returns:
		The parsed Markdown text.
		"""
		
		return md
