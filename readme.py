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

import yamldoc
import academicmarkdown

df = yamldoc.DocFactory(academicmarkdown)
academicmarkdown.build.extensions = [u'toc', u'exec', u'code', u'constant',
                                     u'python']
academicmarkdown.build.postMarkdownFilters = []
academicmarkdown.build.MD(unicode(df), u'readme.md')
academicmarkdown.build.PDF(unicode(df), u'readme.pdf')
