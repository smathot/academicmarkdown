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
import subprocess
import sys

figureTemplate = {
	u'html5':  u"""
<figure id='%(id)s' style='width: %(width)s%%;'>
	<img src='%(source)s' alt='%(caption)s' width=100%%><br />
	<figcaption><strong>Figure %(nFig)d.</strong> %(caption)s</figcaption>
</figure>
""",
u'jekyll':  u"""
![%(source)s](%(source)s)

__Figure %(nFig)d.__ %(caption)s\n{: .fig-caption #%(id)s}\n
""",
	u'odt': u"""
![__Figure %(nFig)d.__ %(caption)s](%(source)s)

__Figure %(nFig)d.__ *%(caption)s*<!--odt-style="Illustration"-->
""",
	u'markdown': u"""
![__Figure %(nFig)d.__ %(caption)s](%(source)s)
"""}


class FigureParser(YAMLParser):

	"""
	The `figure` block embeds a Figure in the text. Figures are numbered
	automatically. The ID can be used to refer to the Figure in the text, using
	a `%` character. So the following figure would be referred to as `%FigFA`.

		%--
		figure:
		 id: FigFA
		 source: foveal_acuity.svg
		 caption: "Visual acuity drops of rapidly with distance from the fovea."
		 width: 100
		--%

	The `caption` and `width` attributes are optional.
	"""

	def __init__(self, style=u'inline', template=u'html5', convertSVG=True, \
			  margins=(30, 20, 30, 20), verbose=False):

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
		margins		--	Page margins. (default=30,20,30,20)
		verbose		--	Indicates whether verbose output should be generated.
						(default=False)
		"""

		self.style = style
		self.template = template
		self.convertSVG = convertSVG
		self.margins = margins
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
			dest = d[u'source'] + u'.png'
			self.msg(u'Converting from SVG')
			A4WidthMm = 210
			A4WidthPx = 744.09
			pxPerMm = A4WidthPx / A4WidthMm
			realWidthMm = A4WidthMm - self.margins[1] - self.margins[3]
			realWidthPx = realWidthMm * pxPerMm
			cmd = [u'inkscape', u'-f', d[u'source'], '-W']
			figWidthPx = float(subprocess.check_output(cmd))
			d[u'width'] = min(100, 100. * figWidthPx / realWidthPx)
			self.msg(u'Width: %.2f (%.2f%%)' % (figWidthPx, d[u'width']))
			if not os.path.exists(dest) or '--clear-svg' in sys.argv:
				cmd = [u'inkscape', u'-f', d[u'source'], u'-e', dest, u'-d', \
					'200', u'-b', u'white', u'-y', u'1.0']
				subprocess.call(cmd)
			else:
				self.msg('"%s" exists, not regenerating' % dest)
			d[u'source'] = dest

		if u'caption' not in d:
			d[u'caption'] = u''
		replaceList = [
			(u'"', u'&quot;'),
			(u'\'', u'&#39;'),
			(u'<', u'&lt;'),
			(u'>', u'&gt;')
			]
		for _from, _to in replaceList:
			d[u'caption'] = d[u'caption'].replace(_from, _to)
		d[u'caption'] = d[u'caption'].strip()
		if u'width' not in d:
			d[u'width'] = 100
		img = figureTemplate[self.template] % d

		if self.style == u'inline':
			md = md.replace(_yaml, img)
		else:
			md = md.replace(_yaml, u'')
			md += img
		# Replace both %MyFigure::a and %MyFigure, to allow for suffixes
		md = md.replace(u'%%%s::' % d[u'id'], u'[Figure %d](#%s)' % (self.nFig, \
			d[u'id']))
		md = md.replace(u'%%%s' % d[u'id'], u'[Figure %d](#%s)' % (self.nFig, \
			d[u'id']))
		return md

