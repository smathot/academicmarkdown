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
from subprocess import check_output, call
import os
import shlex

exportFolder = u'export'
exportFormats = u'odt', u'pdf', u'doc'

def commitHash():

	"""
	Gets the latest commit hash.

	Returns:
	A unicode string with the latest hash.
	"""

	cmd = [u'git', u'log', u'--pretty=format:#%h', u'-1']
	return check_output(cmd)

def snapshot(src, msg=u'snapshot', pdfArgs={}):

	"""
	Commits the current state of the repository and exports a snapshot of the
	current documents.

	Arguments:
	src		--	The source Markdown document.

	Keyword arguments:
	msg		--	A commit message. (default=u'snapshot')
	"""

	cmd = [u'git', u'commit', u'-am', msg]
	print(u'Committing (msg: %s)' % msg)
	call(cmd)
	cmd = [u'git', u'log', u'--pretty=format:[%cd #%h] %s', u'--date=iso', \
		u'-1']
	tag = check_output(cmd).decode()
	folder = os.path.join(exportFolder, tag)
	print(u'Exporting to %s' % folder)
	if os.path.exists(folder):
		raise Exception( \
			u'Folder %s already exists! There is probably nothing new to export.' \
			% folder)
	os.mkdir(folder)
	if u'pdf' in exportFormats:
		build.PDF(src, os.path.join(folder, u'export.pdf'), **pdfArgs)
	if u'doc' in exportFormats:
		build.DOC(src, os.path.join(folder, u'export.doc'))
	if u'docx' in exportFormats:
		build.DOCX(src, os.path.join(folder, u'export.docx'))
	if u'odt' in exportFormats:
		build.ODT(src, os.path.join(folder, u'export.odt'))
	if u'html' in exportFormats:
		build.HTML(src, os.path.join(folder, u'export.html'))
