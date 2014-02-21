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
	ExecParser, IncludeParser, TOCParser, HTMLFilter, MDFilter, WkHtmlToPdf, \
	CodeParser, WcParser, VideoParser, TableParser, constants
from academicmarkdown.constants import *

def HTML(src, target=None, standalone=True):

	"""
	Builds an HTML file from a Markdown source.

	Arguments:
	src			--	Markdown source file. Should be in utf-8 encoding.

	Keyword arguments:
	target		--	HTML target file or None to skip saving. (default=None)
	standalone	--	Indicates whether a full HTML5 document should be generated,
					which embeds all content, or whether the document should
					be rendered without <head> and <body> tags, etc.

	Returns:
	The HTML file as a unicode string.
	"""

	md = MD(src)
	# Count words
	print u'Document statistics:'
	print u'Word count: %d' % len(md.split())
	print u'Character count: %d' % len(md)
	# And finally convert the Markdown to HTML
	pd = Pandoc(css=css, csl=csl, template=html5Ref, standalone=standalone, \
		verbose=True)
	html = pd.parse(md)
	for flt in htmlFilters:
		fltFunc = getattr(HTMLFilter, flt)
		html = fltFunc(html)
	if target != None:
		open(target, u'w').write(html.encode(u'utf-8'))
	print u'Done!'
	return html

def MD(src, target=None):

	"""
	Builds a Markdown file from a Markdown source.

	Arguments:
	src		--	Markdown source file. Should be in utf-8 encoding. If the file
				does not exist, it is interpreted as a Markdown string.

	Keyword arguments:
	target			--	Markdown target file or None to skip saving.
						(default=None)

	Returns:
	The compiled Markdown file as a unicode string.
	"""

	if os.path.exists(src):
		md = open(src).read().decode(u'utf-8')
		print u'Building %s from %s ...' % (target, src)
	else:
		md = src
		print u'Building from string ...'
	# Apply pre-processing Markdown Filters
	for flt in preMarkdownFilters:
		fltFunc = getattr(MDFilter, flt)
		md = fltFunc(md)
	if u'include' in extensions:
		md = IncludeParser(verbose=True).parse(md)
	if u'exec' in extensions:
		md = ExecParser(verbose=True).parse(md)
	if u'toc' in extensions:
		md = TOCParser(anchorHeaders=TOCAnchorHeaders, verbose=True).parse(md)
	if u'figure' in extensions:
		md = FigureParser(verbose=True, style=figureStyle, template= \
			figureTemplate, margins=pdfMargins).parse(md)
	if u'video' in extensions:
		md = VideoParser(verbose=True).parse(md)
	if u'table' in extensions:
		md = TableParser(style=tableStyle, template=tableTemplate, verbose= \
			True).parse(md)
	if u'code' in extensions:
		md = CodeParser(verbose=True, style=codeStyle, template=codeTemplate) \
			.parse(md)
	if u'wc' in extensions:
		md = WcParser(verbose=True).parse(md)
	# Parse Zotero references
	if zoteroApiKey != None and zoteroLibraryId != None:
		clearCache = '--clear-cache' in sys.argv
		md = ZoteroParser(verbose=True, apiKey=zoteroApiKey, libraryId= \
			zoteroLibraryId, headerText=zoteroHeaderText, headerLevel= \
			zoteroHeaderLevel, clearCache=clearCache).parse(md)
	# Apply post-processing Markdown Filters
	for flt in postMarkdownFilters:
		fltFunc = getattr(MDFilter, flt)
		md = fltFunc(md)
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
	wk = WkHtmlToPdf(css=css, margins=pdfMargins, spacing=pdfSpacing, \
		header=pdfHeader, footer=pdfFooter, verbose=True)
	wk.parse(u'.tmp.html', target)

def ODT(src, target):

	"""
	Builds an ODT file from a Markdown source.

	Arguments:
	src		--	Markdown source file. Should be in utf-8 encoding.
	target	--	ODT target file.
	"""

	global figureTemplate
	tmp = figureTemplate
	figureTemplate = u'odt'
	md = MD(src)
	pd = Pandoc(csl=csl, verbose=True)
	pd.odt(md, target, odtRef=odtRef)
	ODTFixer(verbose=True).fix(target)
	figureTemplate = tmp

def DOC(src, target):

	"""
	Builds a DOC file from a Markdown source.

	Arguments:
	src		--	Markdown source file. Should be in utf-8 encoding.
	target	--	DOCX target file.
	"""

	# Since pandoc doesn't support DOC output, we convert first to ODT and from
	# there use unoconv to convert to DOC.
	ODT(src, u'.tmp.odt')
	print u'Converting from .odt to .doc ...'
	cmd = [u'unoconv', u'-f', u'doc', u'.tmp.odt']
	subprocess.call(cmd)
	print u'Done!'
	os.rename(u'.tmp.doc', target)

def DOCX(src, target):

	"""
	Builds a DOCX file from a Markdown source.

	Arguments:
	src		--	Markdown source file. Should be in utf-8 encoding.
	target	--	DOCX target file.
	"""

	global figureTemplate
	tmp = figureTemplate
	figureTemplate = u'markdown'
	md = MD(src)
	pd = Pandoc(csl=csl, verbose=True)
	pd.docx(md, target, docxRef=docxRef)
	figureTemplate = tmp


