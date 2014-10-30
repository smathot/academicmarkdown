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

---
desc:
	Contains functions to build documents from Markdown source.
---
"""

import os
import sys
import shlex
import subprocess
from academicmarkdown import FigureParser, Pandoc, ZoteroParser, ODTFixer, \
	ExecParser, IncludeParser, TOCParser, HTMLFilter, MDFilter, WkHtmlToPdf, \
	CodeParser, WcParser, VideoParser, TableParser, PythonParser, \
	tools, ConstantParser
from academicmarkdown.constants import *

def HTML(src, target=None, standalone=True):

	"""
	desc: |
		Builds an HTML file from a Markdown source.

		%--
		constant:
			arg_src:
				The Markdown source. If it is a path to an existing file, the
				contents of this file are read. Otherwise, the string itself
				it used. Should be in utf-8 encoding.
		--%

	arguments:
		src:
			desc:	"%arg_src"
			type:	[str, unicode]

	keywords:
		target:
			desc:	The name of an HTML target file or None to skip saving.
			type:	[str, unicode, NoneType]
		standalone:
			desc:	Indicates whether a full HTML5 document should be generated,
					which embeds all content, or whether the document should
					be rendered without `<head>` and `<body>` tags, etc.
			type:	bool

	returns:
		desc:		The HTML file as a unicode string.
		type:		unicode
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
	desc:
		Builds a Markdown file from a Markdown source.

	arguments:
		src:
			desc:	"%arg_src"
			type:	[str, unicode]

	keywords:
		target:
			desc: 	The name of a Markdown target file or None to skip saving.
			type:	[str, unicode, NoneType]

	returns:
		desc:		The compiled Markdown file as a unicode string.
		type:		unicode
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
	# Apply all extensions
	for ext in extensions:
		print u'Parsing with %s extension ...' % ext
		if u'include' == ext:
			md = IncludeParser(verbose=True).parse(md)
		elif u'toc' == ext:
			md = TOCParser(anchorHeaders=TOCAnchorHeaders, appendHeaderRefs= \
				TOCAppendHeaderRefs, verbose=True).parse(md)
		elif u'figure' == ext:
			md = FigureParser(verbose=True, style=figureStyle, template= \
				figureTemplate, margins=pdfMargins).parse(md)
		elif u'video' == ext:
			md = VideoParser(verbose=True).parse(md)
		elif u'table' == ext:
			md = TableParser(style=tableStyle, template=tableTemplate, verbose= \
				True).parse(md)
		elif u'code' == ext:
			md = CodeParser(verbose=True, style=codeStyle, template=codeTemplate) \
				.parse(md)
		elif u'wc' == ext:
			md = WcParser(verbose=True).parse(md)
		elif u'exec' == ext:
			md = ExecParser(verbose=True).parse(md)
		elif u'python' == ext:
			md = PythonParser(verbose=True).parse(md)
		elif u'constant' == ext:
			md = ConstantParser(verbose=True).parse(md)
		else:
			raise Exception(u'Unknown Academic Markdown extension: %s' % ext)
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

def PDF(src, target, lineNumbers=False, args=''):

	"""
	desc:
		Builds a PDF file from a Markdown source.

	arguments:
		src:
			desc:	"%arg_src"
			type:	[str, unicode]
		target:
			desc:	The name of a PDF target file.
			type:	[str, unicode]

	keywords:
		lineNumbers:
			desc:	Determines whether line numbers should be added. This is
					currently quite a complicated process, which may break.
			type:	bool
		args:
			desc:	Indicates extra arguments to be passed onto wkhtmltopdf.
			type:	[str, unicode]
	"""

	print u'Building %s from %s ...' % (target, src)
	HTML(src, u'.tmp.html')
	wk = WkHtmlToPdf(css=css, margins=pdfMargins, spacing=pdfSpacing, \
		header=pdfHeader, footer=pdfFooter, verbose=True, args=args)
	if lineNumbers:
		_target = u'.tmp.pdf'
	else:
		_target = target
	wk.parse(u'.tmp.html', _target)
	if lineNumbers:
		tools.addLineNumbersToPDF(_target, target)
		os.remove(_target)

def ODT(src, target):

	"""
	desc:
		Builds an ODT file from a Markdown source.

	arguments:
		src:
			desc:	"%arg_src"
			type:	[str, unicode]
		target:
			desc:	The name of an ODT target file.
			type:	[str, unicode]
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
	desc:
		Builds a DOC file from a Markdown source.

	arguments:
		src:
			desc:	"%arg_src"
			type:	[str, unicode]
		target:
			desc:	The name of a DOC target file.
			type:	[str, unicode]
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
	desc:
		Builds a DOCX file from a Markdown source.

	arguments:
		src:
			desc:	"%arg_src"
			type:	[str, unicode]
		target:
			desc:	The name of a DOCX target file.
			type:	[str, unicode]
	"""

	global figureTemplate
	tmp = figureTemplate
	figureTemplate = u'markdown'
	md = MD(src)
	pd = Pandoc(csl=csl, verbose=True)
	pd.docx(md, target, docxRef=docxRef)
	figureTemplate = tmp

def setStyle(style):

	"""
	desc:
		Automatically sets a style.

	arguments:
		style:
			desc:	The style name. This should be the name of a folder that
					contains style files. See the `academicmarkdown\styles`
					subfolder for examples.
			type:	[str, unicode]
	"""

	global css, csl, html5Ref, odtRef, docxRef
	moduleFolder = os.path.dirname(__file__).decode(sys.getfilesystemencoding())
	if os.path.exists(style):
		stylePath = style
	elif os.path.exists(os.path.join(moduleFolder, u'styles', style)):
		stylePath = os.path.join(moduleFolder, u'styles', style)
	else:
		raise Exception(u'There is no style folder named "%s"' % style)
	print u'Using style folder: %s' % stylePath
	css = os.path.join(stylePath, u'stylesheet.css')
	if not os.path.exists(css):
		css = None
	csl = os.path.join(stylePath, u'citation-style.csl')
	if not os.path.exists(csl):
		csl = None
	html5Ref = os.path.join(stylePath, u'template.html')
	if not os.path.exists(html5Ref):
		html5Ref = None
	odtRef = os.path.join(stylePath, u'reference.odt')
	if not os.path.exists(odtRef):
		odtRef = None
	docxRef = os.path.join(stylePath, u'reference.docx')
	if not os.path.exists(docxRef):
		docxRef = None
