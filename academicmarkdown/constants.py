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

zoteroApiKey = None
zoteroLibraryId = None
zoteroHeaderText = u'References'
zoteroHeaderLevel = 1
path = [os.getcwd().decode(sys.getfilesystemencoding())]

figureTemplate = u'html5'
figureStyle = u'inline'

codeTemplate = u'jekyll'
codeStyle = u'inline'

TOCAnchorHeaders = False

style = None
htmlFilters = [u'DOI', u'pageBreak']
mdFilters = [u'autoItalics']
extensions = [u'figure', u'exec', u'include', u'toc', u'code']
pdfMargins = 30, 20, 30, 20
pdfSpacing = 10, 10
pdfHeader = u'%section%'
pdfFooter = u'%page% of %topage%' 
