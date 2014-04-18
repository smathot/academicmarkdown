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
		s = open(s).read().decode(u'utf-8')
	if excludeYAML:
		s = re.sub(u'%--(.*?)--%', lambda x: u'', s, flags=re.M|re.S)
	if clean:
		s = re.sub(u'^#+\s', lambda x: u'', s, flags=re.M)
	l = []
	for w in s.split():
		if clean:
			w = re.sub(ur'[^a-zA-Z0-9]', u'', w)
		if len(w) > 0:
			l.append(w)
	return len(l)
