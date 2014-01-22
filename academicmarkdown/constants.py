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

import os, sys

# A list of folders that are searched for figures, scripts, etc.
path = [os.getcwd().decode(sys.getfilesystemencoding())]

# Parameters for Zotero integration
zoteroApiKey = None
zoteroLibraryId = None
zoteroHeaderText = u'References'
zoteroHeaderLevel = 1

# Options for the appearance of figures and code blocks
figureTemplate = u'html5'
figureStyle = u'inline'
codeTemplate = u'kramdown'
codeStyle = u'inline'

# Indicates whether headers should be turned into clickable anchors by TOCParser
TOCAnchorHeaders = False

# Paths to files that determine the document's appearance. For more information,
# see the Pandoc documentation.
css = None # CSS stylesheet
csl = None # CSL citation style
html5Ref = None # HTML5 template
odtRef = None # ODT reference document
docxRef = None # DOCX reference document

# A list of filters from academicmarkdown.HTMLFilter that should be performed
# after an HTML document has been genertated.
htmlFilters = [u'DOI', u'citationGlue']

# A list of filters from academicmarkdown.MDFilter that should be performed
# on the Markdown source, prior to any processing.
preMarkdownFilters = []
# A list of filters from academicmarkdown.MDFilter that should be performed
# on the Markdown source, after all other processing has been performed
postMarkdownFilters = [u'autoItalics', u'pageBreak', u'magicVars']

# A list of extensions that are enabled.
extensions = [u'figure', u'exec', u'include', u'toc', u'code', u'wc']

# The page margins
pdfMargins = 30, 20, 30, 20

# The spacing between the content and the header and footer
pdfSpacing = 10, 10

# Header and footer text
pdfHeader = u'%section%'
pdfFooter = u'%page% of %topage%'
