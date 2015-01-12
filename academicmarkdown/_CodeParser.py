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

import yaml
from academicmarkdown import YAMLParser
import subprocess

codeTemplate = {
u'pandoc' : u"""
~~~ {%(syntax)s}
%(code)s
~~~
""",
u'kramdown' : u"""
~~~ %(syntax)s
%(code)s
~~~
""",
u'jekyll' : u"""
{%% highlight %(syntax)s %%}
%(code)s
{%% endhighlight %%}

__Listing %(nCode)d.__ %(caption)s\n{: .lst-caption #%(id)s}
"""}

class CodeParser(YAMLParser):

	"""
	The `code` blocks embeds a code listing in the text, quite to similar to the
	`figure` block.

		%--
		code:
		 id: CodeA caption: |
  Test!

		 source: my_script.py
		 syntax: python
		 caption: "A simple Python script"
		--%

	The `caption` and `syntax` attributes are optional.
	"""

	def __init__(self, style=u'inline', template=u'kramdown', verbose=False):

		"""
		Constructor.

		Keyword arguments:
		style		--	Can be u'inline' or u'below' to indicate whether code
						should be placed in or below the text.
						(default=u'inline')
		template	--	Indicates the output format, which can be 'kramdown' or
						'liquid'. (default=u'kramdown')
		verbose		--	Indicates whether verbose output should be generated.
						(default=False)
		"""

		self.style = style
		self.template = template
		super(CodeParser, self).__init__(_object=u'code', required=['id', \
			'source', 'syntax'], verbose=verbose)

	def parse(self, md):

		"""See BaseParser.parse()."""

		self.nCode = 0
		return super(CodeParser, self).parse(md)

	def parseObject(self, md, _yaml, d):

		"""See YAMLParser.parseObject()."""

		self.nCode += 1
		d['nCode'] = self.nCode
		self.msg(u'Found code: %s (%d)' % (d['id'], self.nCode))
		d[u'source'] = self.getPath(d[u'source'])
		if u'caption' not in d:
			d[u'caption'] = u''
		if self.template == u'kramdown':
			d[u'syntax'] = u'.' + d[u'syntax']
		with open(self.getPath(d[u'source'])) as fd:
			d[u'code'] = fd.read().strip()
		code = codeTemplate[self.template] % d
		if self.style == u'inline':
			md = md.replace(_yaml, code)
		else:
			md = md.replace(_yaml, u'')
			md += code
		md = md.replace(u'%%%s' % d[u'id'], u'[Listing %d](#%s)' % (self.nCode, \
			d[u'id']))
		return md
