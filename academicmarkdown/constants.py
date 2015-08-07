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
desc: |
    Contains the settings, which are imported into `academicmarkdown.build`. You
    can change these settings in the `build` module, as shown below.

    __Module source:__

    %--
    code:
        id: LstConstants
        syntax: python
        source: academicmarkdown/constants.py
    --%

example: |
    from academicmarkdown import build
    build.pdfHeader = u'A header for my PDF'
---
"""

import os

from academicmarkdown.py3compat import *

# A list of folders that are searched for figures, scripts, etc.
path = [safe_decode(os.getcwd(), enc=sys.getfilesystemencoding())]

# Parameters for Zotero integration
zoteroApiKey = None
zoteroLibraryId = None
zoteroHeaderText = u'References'
zoteroHeaderLevel = 1

# Options for the appearance of figures, blocks, and tables
figureTemplate = u'html5'
figureStyle = u'inline'
codeTemplate = u'pandoc'
codeStyle = u'inline'
tableTemplate = u'html5'
tableStyle = u'inline'

# Indicates whether headers should be turned into clickable anchors by TOCParser
TOCAnchorHeaders = False
# Indicates whether references to header ids should be automatically appended
# to the main text.
TOCAppendHeaderRefs = True

# Paths to files that determine the document's appearance. For more information,
# see the Pandoc documentation.
css = None  # CSS stylesheet
csl = None  # CSL citation style
html5Ref = None  # HTML5 template
odtRef = None  # ODT reference document
docxRef = None  # DOCX reference document

# A list of filters from academicmarkdown.HTMLFilter that should be performed
# after an HTML document has been genertated.
htmlFilters = [u'DOI', u'citationGlue']

# A list of filters from academicmarkdown.MDFilter that should be performed
# on the Markdown source, prior to any processing.
preMarkdownFilters = []
# A list of filters from academicmarkdown.MDFilter that should be performed
# on the Markdown source, after all other processing has been performed
postMarkdownFilters = [u'autoItalics', u'pageBreak', u'magicVars', u'highlight']

# A list of extensions that are enabled.
extensions = [u'include', u'exec', u'python', u'toc', u'code', u'video', \
              u'table', u'figure', u'constant', u'wc']

# The page margins
pdfMargins = 30, 20, 30, 20

# The spacing between the content and the header and footer
pdfSpacing = 10, 10

# Header and footer text
pdfHeader = u'%section%'
pdfFooter = u'%page% of %topage%'
