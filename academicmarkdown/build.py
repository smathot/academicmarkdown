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
import sys
import shlex
import subprocess
from academicmarkdown import FigureParser, Pandoc, ZoteroParser, ODTFixer, \
	ExecParser, IncludeParser, TOCParser, Filter

zoteroApiKey = None
zoteroLibraryId = None
zoteroHeaderText = u'References'
zoteroHeaderLevel = 1
style = None
htmlFilters = [u'DOI', u'pageBreak']
extensions = [u'figure', u'exec', u'include', u'toc']
srcFolder = os.getcwd().decode(sys.getfilesystemencoding())

def HTML(src, target, standalone=True):
	
	"""
	Builds an HTML file from a Markdown source.
	
	Arguments:
	src			--	Markdown source file. Should be in utf-8 encoding.
	target		--	HTML target file or None to skip saving.
	
	Keyword arguments:
	standalone	--	Indicates whether a full HTML5 document should be generated,
					which embeds all content, or whether the document should
					be rendered without <head> and <body> tags, etc.
	
	Returns:
	The HTML file as a unicode string.
	"""
	
	md = MD(src)
	# Use style
	if style != None:
		css = os.path.join(style, u'html5.css')
		if not os.path.exists(css):
			css = None
		csl = os.path.join(style, u'references.csl')
		if not os.path.exists(csl):
			csl = None
		template = os.path.join(style, u'html5.html')
		if not os.path.exists(template):
			template = None
	else:
		css = None
		csl = None
		template = None
	# Count words
	print u'Document statistics:'
	print u'Word count: %d' % len(md.split())
	print u'Character count: %d' % len(md)
	# And finally convert the Markdown to HTML
	pd = Pandoc(css=css, csl=csl, template=template, standalone=standalone, \
		verbose=True)
	html = pd.parse(md)
	for flt in htmlFilters:
		fltFunc = getattr(Filter, flt)
		html = fltFunc(html)		
	open(target, u'w').write(html.encode(u'utf-8'))	
	print u'Done!'
	return html
	
def MD(src, target=None, figureTemplate=u'html5'):
	
	"""
	Builds a Markdown file from a Markdown source.
	
	Arguments:	
	src		--	Markdown source file. Should be in utf-8 encoding.
	
	Keyword arguments:
	target			--	Markdown target file or None to skip saving.
						(default=None)
	figureTemplate	--	The figureTemplate to be used for the FigureParser.
						(default=u'html5')
	chdir			--	Indicates whether the working directory should be
						changed to the folder of the Markdown source.
						(default=True)
	
	Returns:
	The compiled Markdown file as a unicode string.
	"""
	
	md = open(src).read().decode(u'utf-8')
	print u'Building %s from %s ...' % (target, src)	
	if u'include' in extensions:
		md = IncludeParser(verbose=True).parse(md)
	if u'toc' in extensions:
		md = TOCParser(verbose=True).parse(md)
	if u'figure' in extensions:
		md = FigureParser(verbose=True, template=figureTemplate).parse(md)
	if u'exec' in extensions:
		md = ExecParser(verbose=True).parse(md)
	# Parse Zotero references
	if zoteroApiKey != None and zoteroLibraryId != None:
		clearCache = '--clear-cache' in sys.argv
		md = ZoteroParser(verbose=True, apiKey=zoteroApiKey, libraryId= \
			zoteroLibraryId, headerText=zoteroHeaderText, headerLevel= \
			zoteroHeaderLevel, clearCache=clearCache).parse(md)
	if target != None:
		open(target, u'w').write(md.encode(u'utf-8'))
	return md

def PDF(src, target):

	"""
	Builds a PDF file from a Markdown source.
	
	Arguments:
	src					--	Markdown source file. Should be in utf-8 encoding.
	target				--	HTML target file.
	"""
	
	print u'Building %s from %s ...' % (target, src)
	HTML(src, u'.tmp.html')
	if style != None and os.path.exists(os.path.join(style, \
		u'wkhtmltopdf.tmpl')):
		tmpl = open(os.path.join(style, u'wkhtmltopdf.tmpl')).read().decode( \
			u'utf-8')
	else:
		tmpl = u'wkhtmltopdf %(source)s %(target)s'
	cmd = tmpl % {u'source' : u'.tmp.html', u'target' : target}	
	subprocess.call(shlex.split(cmd.encode(u'utf-8')))
	os.remove(u'.tmp.html')
	print u'Done!'

def ODT(src, target):
	
	"""
	Builds an ODT file from a Markdown source.
	
	Arguments:
	src		--	Markdown source file. Should be in utf-8 encoding.
	target	--	ODT target file.
	"""		
	
	md = MD(src, figureTemplate=u'odt')
	# Use style
	if style != None:
		csl = os.path.join(style, u'references.csl')
		if not os.path.exists(csl):
			csl = None
	else:
		csl = None
	pd = Pandoc(csl=csl, verbose=True)		
	pd.odt(md, target)
	ODTFixer(verbose=True).fix(target)
	
def DOCX(src, target):
	
	"""
	Builds an ODT file from a Markdown source.
	
	Arguments:
	src		--	Markdown source file. Should be in utf-8 encoding.
	target	--	DOCX target file.
	"""		
	
	md = MD(src, figureTemplate=u'md')
	# Use style
	if style != None:
		csl = os.path.join(style, u'references.csl')
		if not os.path.exists(csl):
			csl = None
	else:
		csl = None
	pd = Pandoc(csl=csl, verbose=True)
	pd.docx(md, target)
	
	