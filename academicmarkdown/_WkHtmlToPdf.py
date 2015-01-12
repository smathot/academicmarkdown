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
import shlex
import subprocess
from academicmarkdown import BaseParser
from academicmarkdown.py3compat import *

# From <http://madalgo.au.dk/~jakobt/wkhtmltoxdoc/wkhtmltopdf-0.9.9-doc.html>
feaderTmpl = """<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8" />
<script>
function subst() {
  var vars={};
  var x=document.location.search.substring(1).split('&');
  for(var i in x) {var z=x[i].split('=',2);vars[z[0]] = unescape(z[1]);}
  var x=['frompage','topage','page','webpage','section','subsection','subsubsection'];
  for(var i in x) {
    var y = document.getElementsByClassName(x[i]);
    for(var j=0; j<y.length; ++j) y[j].textContent = vars[x[i]];
  }
}
</script>
%css%
</head><body onload="subst()">
<div class="%class%">%feader%</div>
</body></html>"""

class WkHtmlToPdf(BaseParser):

	def __init__(self, css=None, fix00=True, margins=(20, 20, 30, 20),
		spacing=(10, 10), header=None, footer=u'%page% / %topage%',
		verbose=False, args=''):

		"""
		Constructor.

		Keyword arguments:
		css			--	A path to a css stylesheet or None. (default=None)
		fix00		--	Indicates whether #00 corruptions should be fixed.
						(default=True)
		margins		--	A T,R,B,L tuple of page margins. (default=20,20,30,20)
		spacing		--	A (header spacing, footer spacing) tuple.
						(default=10,10)
		header		--	A header text, or None. (default=None)
		footer		--	A footer text, or None. (default=u'%page% / %topage%')
		verbose		--	Indicates whether verbose output should be generated.
						(default=False)
		args		--
		"""

		self.css = css
		self.args = args
		self.fix00 = fix00
		self.margins = margins
		self.spacing = spacing
		self.header = header
		self.footer = footer
		super(WkHtmlToPdf, self).__init__(verbose=verbose)

	def createFeader(self, s, cssClass):

		"""
		Builds a header or footer html file.

		Arguments:
		s			--	The contents for the header/ footer.
		cssClass	--	The css class to be used for the div containing the
						contents.

		Returns:
		An HTML string containing the header/ footer.
		"""

		regEx = r'%(?P<var>[a-z]+)%'
		for r in re.finditer(regEx, s):
			s = s.replace(u'%%%s%%' % r.group('var'), \
				u'<span class="%s"></span>' % r.group('var'))
		feader = feaderTmpl.replace(u'%feader%', s)
		if self.css != None:
			feader = feader.replace(u'%css%', \
				u'<link rel="stylesheet" href="%s" type="text/css" />' % \
				self.css)
		else:
			feader = feader.replace(u'%css%', u'')
		feader = feader.replace(u'%class%', cssClass)
		return feader

	def parse(self, html, target):

		"""See BaseParser.parse()."""

		self.msg(u'Invoking wkhtmltopdf')
		cmd = u'wkhtmltopdf -T %s -R %s -B %s -L %s' % self.margins
		if self.header != None:
			open('.header.html', 'wb').write(safe_encode(self.createFeader(
				self.header, u'header')))
			cmd += u' --header-html .header.html --header-spacing %s' % \
				self.spacing[0]
		if self.footer != None:
			open('.footer.html', 'wb').write(safe_encode(
				self.createFeader(self.footer, u'footer')))
			cmd += u' --footer-html .footer.html --footer-spacing %s' % \
				self.spacing[1]
		cmd += u' ' + self.args
		cmd += u' %s "%s"' % (html, target)
		self.msg(cmd)
		if not py3:
			cmd = safe_encode(cmd)
		subprocess.call(shlex.split(cmd))
		if self.fix00:
			# Due to a bug in wkhtmltopdf, the PDF may contain #00 strings,
			# which cause Acrobat Reader to choke (but not other PDF readers).
			# This happens mostly when filenames are very long, in which case
			# anchors are hashed, and the resulting hashes sometimes contain #00
			# values. Here we simply replace all #00 strings, which seems to
			# work.
			self.msg(u'Checking for #00')
			pdf = open(target, 'rb').read()
			if safe_encode('#00') in pdf:
				self.msg(u'Fixing #00!')
				pdf = pdf.replace('#00', '#01')
				open(target, u'wb').write(pdf)
