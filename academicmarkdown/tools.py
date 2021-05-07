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

import re
import os
from academicmarkdown.py3compat import *

def wordCount(s, excludeYAML=True, clean=True):

	"""
	Returns the word count of a file or a string of text.

	Arguments:
	s			--	A filename or a string of text. This paramater can also
					be a list of filenames or a list of strings of text, in
					which case the summed word count will be returned.

	Keyword arguments:
	excludeYAML	--	Indicates whether the contents of %-- --% YAML blocks
					should be excluded from the word count. (default=True)
	clean		--	Indicates whether the text should be cleaned of things
					that you probably don't want to count, such as `##`
					characters. (default=True)

	Returns:
	A word count.
	"""

	if isinstance(s, list):
		wc = 0
		for _s in s:
			wc += wordCount(_s, excludeYAML=excludeYAML, clean=clean)
		return wc
	if os.path.exists(s):
		s = safe_decode(open(s).read())
	if excludeYAML:
		s = re.sub(u'%--(.*?)--%', lambda x: u'', s, flags=re.M|re.S)
	if clean:
		s = re.sub(u'^#+\s', lambda x: u'', s, flags=re.M)
	l = []
	for w in s.split():
		if clean:
			w = re.sub(r'[^a-zA-Z0-9]', u'', w)
		if len(w) > 0:
			l.append(w)
	return len(l)

def addLineNumbersToPDF(inFile, outFile, color='#d3d7cf'):

	"""
	desc:
		Adds line numbers to a PDF file.

	arguments:
		inFile:
			desc:	The name of the input PDF.
			type:	str, unicode
		outFile:
			desc:	The name of the output PDF.
			type:	str, unicode

	keywords:
		color:
			desc:	An HTML-style color name.
			type:	str, unicode
	"""

	import os
	import shutil
	import subprocess
	try:
		from scipy.ndimage import imread
	except ImportError:
		from imageio import imread
	import numpy as np
	from PIL import Image, ImageDraw, ImageFont

	#fontFile = '/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf'
	fontFile = '/usr/share/fonts/truetype/freefont/FreeSans.ttf'
	fontSize = 20
	tmpFolder = u'line-numbers-tmp'
	pageFolder = u'%s/page' % tmpFolder
	watermarkFolder = u'%s/watermark' % tmpFolder

	try:
		shutil.rmtree(tmpFolder)
	except:
		pass
	os.makedirs(pageFolder)
	os.makedirs(watermarkFolder)

	print(u'Adding line numbers to PDF')
	print(u'Converting ...')
	cmd = u'convert -density 150 %s %s' % (inFile, os.path.join(pageFolder,
		u'%03d.png'))
	subprocess.call(cmd.split())
	print(u'Done!')
	# Create watermarks for all pages
	for path in os.listdir(pageFolder):
		try:
			im = imread(os.path.join(pageFolder, path), flatten=True)
		except TypeError:
			im = imread(os.path.join(pageFolder, path), as_gray=True)
		# Create a list of indices that have text on them
		nonEmptyRows = np.where(im.mean(axis=1) != 255)[0]
		# Store the rows (i.e.) y coordinates of all to-be-numbered-rows
		numberRows =[]
		firstRow = None
		for row in nonEmptyRows:
			if im[row-1].mean() == 255:
				numberRows.append(row)
		print(u'Found %d lines!' % len(numberRows))
		# Create watermark image
		print(u'Creating watermark ...')
		font = ImageFont.truetype(fontFile, fontSize)
		wm = Image.new('RGBA', (im.shape[1], im.shape[0]))
		dr = ImageDraw.Draw(wm)
		i = 1
		for row in numberRows:
			dr.text((32, row), '%s' % i, font=font, fill=color)
			i += 1
		wm.save(os.path.join(watermarkFolder, path))
		print(u'Done!')

	print(u'Creating watermark pdf ...')
	cmd = 'convert %s/*.png watermark.pdf' % watermarkFolder
	subprocess.call(cmd.split())
	print(u'Done!')

	print(u'Merging watermark and source document ...')
	cmd = u'pdftk %s multibackground watermark.pdf output %s' \
		% (inFile, outFile)
	subprocess.call(cmd.split())
	print(u'Done!')

	print(u'Cleaning up ...')
	shutil.rmtree(tmpFolder)
	print(u'Done')
