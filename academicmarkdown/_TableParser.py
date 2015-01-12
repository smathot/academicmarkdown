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

import os
import yaml
from academicmarkdown import YAMLParser
from academicmarkdown.py3compat import *
import subprocess
import sys

tableTemplate = {u'html5':  u"""
<span style='color:red;'>NOT IMPLEMENTED</span>
""",
u'kramdown':  u"""
%(table)s

__Table %(nTbl)d.__ %(caption)s\n{: .tbl-caption #%(id)s}
""",
u'pandoc':  u"""

<div class='table'>

<span class='table-id'>Table %(nTbl)d</span>

<span class='caption'>%(caption)s</span>

%(table)s

</div>
"""}


class TableParser(YAMLParser):

	"""
	The `table` block reads a table from a `.csv` file and embed it into the
	document. The source file needs to be a utf-8 encoded file that is
	comma separated and double quoted.

		%--
		table:
		 id: MyTable
		 source: my_table.csv
		 caption: "My table caption."
		 ndigits: 4
		--%
	"""

	def __init__(self, style=u'inline', template=u'kramdown', verbose= \
		False):

		"""
		Constructor.

		Keyword arguments:
		style		--	Can be u'inline' or u'below' to indicate whether figures
						should be placed in or below the text.
						(default=u'inline')
		template	--	Indicates the output format, which can be 'odt' or
						'html5'. (default=u'html5')
		verbose		--	Indicates whether verbose output should be generated.
						(default=False)
		"""

		self.style = style
		self.template = template
		super(TableParser, self).__init__(_object=u'table', required=['id', \
			'source'], verbose=verbose)

	def parse(self, md):

		"""See BaseParser.parse()."""

		self.nTbl = 0
		return super(TableParser, self).parse(md)

	def parseObject(self, md, _yaml, d):

		"""See YAMLParser.parseObject()."""

		self.nTbl += 1
		d['nTbl'] = self.nTbl
		self.msg(u'Found table: %s (%d)' % (d['id'], self.nTbl))
		d[u'source'] = self.getPath(d[u'source'])
		if u'caption' not in d:
			d[u'caption'] = u''
		if u'ndigits' not in d:
			d[u'ndigits'] = 4
		# Read table and turn it into a kramdown-style table
		s = u''
		import csv
		i = 0
		with open(d[u'source'], u'r') as csvFile:
			csvReader = csv.reader(csvFile, delimiter=',', quotechar='"')
			for row in csvReader:
				# Pandoc requires a row of alignment indicators below the
				# header. See also:
				# - <http://johnmacfarlane.net/pandoc/README.html#tables>
				if self.template == u'pandoc':
					if i == 1:
						alignList = []
						for col in row:
							try:
								float(col)
								alignList.append(u'--:')
							except:
								alignList.append(u':--')
						s += (u'|' + u'|'.join(alignList) + u'|\n')
				_row = []
				for col in row:
					try:
						# If a value is numeric, we need to round it. If the
						# rounde value is 0, we indicated this with a smaller
						# than sign.
						float(col)
						col = round(float(col), d[u'ndigits'])
						if col == 0:
							col = u'< 0.' + u'0'*(d[u'ndigits']-1) + u'1'
						else:
							# Use a somethat convoluted string formatting
							# operation to make sure that we don't lose trailing
							# zeros.
							col = (u'%%.%df' % d[u'ndigits']) % col
						_row.append(col)
					except:
						_row.append(safe_decode(col))
				s += (u'|' + u'|'.join(_row) + u'|\n')
				i += 1
		d[u'table'] = s
		tbl = tableTemplate[self.template] % d
		# Insert/ append table into document
		if self.style == u'inline':
			md = md.replace(_yaml, tbl)
		else:
			md = md.replace(_yaml, u'')
			md += tbl
		# Replace reference to table
		md = md.replace(u'%%%s' % d[u'id'], u'[Table %d](#%s)' % (self.nTbl, \
			d[u'id']))
		return md
