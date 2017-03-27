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

import yaml
from academicmarkdown import YAMLParser
from academicmarkdown.py3compat import *
from academicmarkdown.constants import *

class GitHubParser(YAMLParser):

	"""
	The `github` block includes references to GitHub issues or user profiles.
	For example:

		%-- github: { user: smathot } --%
		%-- github: { repo: "smathot/academicmarkdown", issue: 1 } --%
	"""

	def __init__(self, verbose=False):

		"""See YAMLParser.__init__()."""

		super(GitHubParser, self).__init__(_object=u'github', verbose=verbose)

	def parseObject(self, md, _yaml, d):

		"""See YAMLParser.parseObject()."""

		if not isinstance(d, dict):
			raise Exception(u'Expecting a dict')
		if u'user' in d:
			username = d['user']
			return md.replace(_yaml, \
				u'[@%s](https://github.com/%s)' % (username, username))
		if u'issue' in d:			
			from cachedurlget import urlget
			url = u'https://api.github.com/repos/%(repo)s/issues/%(issue)d' % d
			s = urlget(url)
			d = yaml.load(s)
			summary = u'[Issue #%(number)s](%(url)s): %(title)s' % d
			for label in d[u'labels']:
				summary += u' (*%(name)s*) ' % label
			return md.replace(_yaml, summary)
		raise Exception(u'Invalid GitHub block')
