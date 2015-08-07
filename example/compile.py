#!/usr/bin/env python
# -*- coding:utf-8 -*-

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

from os import path

import academicmarkdown
from academicmarkdown import build

import myZoteroCredentials

base_path = path.join(u'example', u'src')
build.path.append(base_path)
build.zoteroLibraryId = myZoteroCredentials.zoteroLibraryId
build.zoteroApiKey = myZoteroCredentials.zoteroApiKey
build.setStyle('modern')
build.pdfHeader = u'Generated with academicmarkdown {version}'.format(
    version=academicmarkdown.__version__
)
build.PDF(path.join(base_path, 'example.md'), path.join(base_path, 'example.html'))
build.HTML(path.join(base_path, 'example.md'), path.join(base_path, 'example.html'))
