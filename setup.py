#!/usr/bin/env python
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

from os import path
from itertools import imap, ifilter
from ast import parse
from setuptools import setup, find_packages

if __name__ == '__main__':
    package_name = u'python-academicmarkdown'
    package_dir = package_name.partition('-')[2]

    with open(path.join(package_dir, '__init__.py')) as f:
        __version__ = next(imap(lambda buf: next(imap(lambda e: e.value.s, parse(buf).body)),
                                ifilter(lambda line: line.startswith('__version__'), f)))

    setup(
        name=package_name,
        version=__version__,
        description=u'A Python package for generating scientific documents using Markdown.',
        author=u'Sebastiaan Mathôt',
        author_email=u's.mathot@cogsci.nl',
        license=u'GNU GPL Version 3',
        url=u'https://github.com/smathot/academicmarkdown',
        packages=find_packages()
    )
