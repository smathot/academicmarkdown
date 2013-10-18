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

figureTemplate = {
	u'html5':  u"""
<figure id='%(id)s'>
	<img src='%(source)s' alt='%(caption)s'><br />
	<figcaption><strong>Figure %(nFig)d.</strong> %(caption)s</figcaption>
</figure>
""",
	u'odt': u"""
![__Figure %(nFig)d.__ %(caption)s](%(source)s)

__Figure %(nFig)d.__ %(caption)s<!--odt-style="Illustration"-->
""",
	u'md': u"""
![__Figure %(nFig)d.__ %(caption)s](%(source)s)
"""}
	

class FigureParser(YAMLParser):
	
	def __init__(self, style=u'inline', template=u'html5', convertSVG=True, \
			  verbose=False):
		
		"""
		Constructor.
		
		Keyword arguments:
		style		--	Can be u'inline' or u'below' to indicate whether figures
						should be placed in or below the text.
						(default=u'inline')
		template	--	Indicates the output format, which can be 'odt' or 
						'html5'. (default=u'html5')
		convertSVG	--	Indicates whether .svg files should be converted to .png
						for better embedding. (default=True)
		verbose		--	Indicates whether verbose output should be generated.
						(default=False)
		"""
		
		self.style = style
		self.template = template
		self.convertSVG = convertSVG
		super(FigureParser, self).__init__(_object=u'figure', required=['id', \
			'source'], verbose=verbose)
		
	def parse(self, md):
		
		"""See BaseParser.parse()."""
		
		self.nFig = 0
		return super(FigureParser, self).parse(md)

	def parseObject(self, md, _yaml, d):
		
		"""See YAMLParser.parseObject()."""
		
		self.nFig += 1
		d['nFig'] = self.nFig
		self.msg(u'Found figure: %s (%d)' % (d['id'], self.nFig))
		
		d[u'source'] = self.getPath(d[u'source'])
		
		if d[u'source'].lower().endswith(u'.svg') and self.convertSVG:
			self.msg(u'Converting to .png')
			dest = d[u'source'] + u'.tiff'
			_cmd = ['convert', '-compress', 'lzw', '-bordercolor', \
				'white' , '-density', '100', '-trim', '-border', \
				'2', '-depth', '8', '-alpha', 'Off', d['source'],  \
				dest]
			_cmd = ['rsvg-convert', '-f', 'tiff', \
					'-o', dest, d['source']]	
			print _cmd
			subprocess.call(_cmd)
			d[u'source'] = dest
			
		
		if u'caption' not in d:
			d[u'caption'] = u''		
		_id = u'figure-%d' % self.nFig		
		img = figureTemplate[self.template] % d
		
		if self.style == u'inline':
			md = md.replace(_yaml, img)
		else:
			md = md.replace(_yaml, u'')
			md += img
		# Replace both %MyFigure::a and %MyFigure, to allow for suffixes
		md = md.replace(u'%%%s::' % d[u'id'], u'[Figure %d](#%s)' % (self.nFig, \
			_id))
		md = md.replace(u'%%%s' % d[u'id'], u'[Figure %d](#%s)' % (self.nFig, \
			_id))		
		return md
	
