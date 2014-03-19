#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of academicmarkdown.

academicmarkdown is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

academicmarkdown is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with academicmarkdown.  If not, see <http://www.gnu.org/licenses/>.
"""

from academicmarkdown import build
build.extensions = [u'toc', u'exec', u'code', u'python']
build.path.append('..')
build.css = 'styles/modern/html5.css'
build.postMarkdownFilters = []
build.TOCAppendHeaderRefs = True
build.PDF(u'readme/readme.md', u'readme/readme.pdf')
build.HTML(u'readme/readme.md', u'readme/readme.html')
build.MD(u'readme/readme.md', u'readme.md')
#build.ODT(u'readme.md', u'readme/readme.odt')
#build.DOCX(u'readme.md', u'readme/readme.docx')
