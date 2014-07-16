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

try:
	from pyzotero import zotero
except:
	zotero = None

from academicmarkdown import BaseParser
import os
import re
import yaml
import json
import pickle
import warnings

class ZoteroParser(BaseParser):

	cachePath = u'.zoteromarkdown.cache'

	def __init__(self, libraryId, apiKey, libraryType=u'user', \
		clearCache=False, headerText=u'References', headerLevel=1, \
		odtStyle=None, fixDOI=True, fixAuthorNames=True, verbose=False, \
		removeURL=True):

		"""
		Constructor.

		Arguments:
		libraryId		--	The libraryId, available from your Zotero profile.
		apiKey			--	The API key, available from your Zotero profile.

		Keyword arguments:
		libraryType		--	The library type. Can be 'user' or 'group'.
							(default=u'user')
		clearCache		--	Indicates whether the cache should be cleared.
							(default=False)
		headerText		--	Indicates the text to be used for the header.
							(default=u'References')
		headerLevel		--	Indicates the header level for the references.
							(default=1)
		odtStyle		--	Indicates the style to be used for ODT output. This
							style is indicated as an HTML comment, so that it
							does not affect HTML output. (default=None)
		fixDOI			--	Indicates that the DOI field should be remapped and
							cleaned up for proper rendering. (default=True)
		fixAuthorNames	--	Indicates that first names of authors should be
							converted to clean initials, to avoid one author
							appearing as multiple. (default=True)
		removeURL		--	Removes the URL from the references, because some
							styles insist on adding it. The URL is only removed
							when a journal (i.e. `container-title` field) is
							available. (default=True)
		verbose			--	Indicates whether verbose output should be printed.
							(default=False)
		"""

		if zotero == None:
			raise Exception(u'pyzotero is not available!')
		super(ZoteroParser, self).__init__(verbose=verbose)
		self.zotero = None
		self.libraryId = libraryId
		self.apiKey = apiKey
		self.libraryType = libraryType
		self.headerText = headerText
		self.headerLevel = headerLevel
		self.odtStyle = odtStyle
		self.fixDOI = fixDOI
		self.fixAuthorNames = fixAuthorNames
		self.removeURL = removeURL
		self.refCount = 0
		if not os.path.exists(self.cachePath) or clearCache:
			self.cache = {}
		else:
			fd = open(self.cachePath)
			try:
				self.cache = pickle.load(fd)
			except:
				self.msg(u'Failed to open cache.')
				self.cache = {}
			fd.close()

	def connect(self):

		"""Connects to the Zotero API."""

		self.msg(u'Connecting to Zotero server.')
		self.zotero = zotero.Zotero(self.libraryId, self.libraryType, \
			self.apiKey)

	def getYear(self, s):

		"""
		Extracts the year from a string in a clever way.

		Arguments:
		s	--	A string.

		Returns:
		A best guess of the year.
		"""

		try:
			from dateutil import parser
		except:
			self.msg(u'dateutil is not available to guess the year.')
			return s
		try:
			return parser.parse(s).year
		except:
			self.msg(u'failed to parse date %s' % s)
			return s

	def parse(self, md):

		"""
		Parses pandoc-style citations from the documents and adds a
		corresponding bibliography as YAML to the documents.

		Arguments:
		md		--	A string containing MarkDown text.

		Returns:
		The Markdown text with bibliography added.
		"""

		items = []
		oldQueries = []
		regexp =  ur'@([^ ?!,.\t\n\r\f\v\]\[;]+)'
		for r in re.finditer(regexp, md):
			queryString = r.groups()[0]
			self.msg(u'Found citation (#%d) "%s"' % (self.refCount,
				queryString))
			if queryString in oldQueries:
				continue
			self.refCount += 1
			matches = self.bestMatch(queryString)
			if len(matches) == 0:
				self.msg(u'No matches for "%s"!' % queryString)
				continue
			if len(matches) > 1:
				raise Exception( \
					u'Multiple Zotero matches (%d) for "@%s". Be more specific!' % \
					(len(matches), queryString))
			match = matches[0]
			if match in items and queryString not in oldQueries:
				for _queryString in sorted(oldQueries):
					print u'Ref: %s' % _queryString
				raise Exception( \
					u'"%s" refers to an existent reference with a different name. Please use consistent references (see list above)!' \
					% queryString)
			match[u'id'] = queryString
			if self.odtStyle != None:
				match[u'title'] += u'<!--odt-style="%s"-->' % self.odtStyle
			items.append(match)
			oldQueries.append(queryString)
		# TODO Placing the citation info in the YAML block doesn't appear to
		# work. So for now save it as a JSON file.
		fd = open(u'.bibliography.json', u'w')
		json.dump(items, fd, indent=1)
		fd.close()
		if self.headerText == None or self.headerLevel == None:
			return md
		md = md.replace(u'%rc%', unicode(self.refCount))
		return md + u'\n\n%s %s\n\n' % (u'#' * self.headerLevel, \
			self.headerText)

	def bestMatch(self, queryString):

		"""
		Retrieves a matching item for a given query. Queries

		Arguments:
		queryString		--	A query string.


		Returns:
		A csljson-style dictionary for the matching item.
		"""

		query = self.splitCitation(queryString)
		if query[0] in self.cache:
			self.msg(u'Retrieving "%s" from cache.' % query[0])
			items = self.cache[query[0]]
		else:
			self.msg(u'Retrieving "%s" from Zotero API.' % query[0])
			if self.zotero == None:
				self.connect()
			try:
				items = self.zotero.top(q=query[0].encode(u'utf-8'), limit= \
					100, content=u'csljson')
			except:
				self.msg(u'Failed to query Zotero server!')
				return []
			self.cache[query[0]] = items
			fd = open(self.cachePath, u'w')
			pickle.dump(self.cache, fd)
			fd.close()
		matches = []
		for item in items:
			match = True
			matchPhase = 0
			for i in range(len(query)):
				# Determine whether we are matching a year or an author name
				term = query[i].lower()
				try:
					int(term)
					matchPhase += 1
				except:
					pass
				# Check authors
				if matchPhase == 0:
					if i >= len(item[u'author']):
						match = False
						break
					if not item[u'author'][i][u'family'].lower().startswith( \
						term):
						match = False
						break
				# Check year
				elif matchPhase == 1:
					if u'issued' not in item or term not in item[u'issued'] \
						[u'raw']:
						match = False
						break
					matchPhase += 1
				# Check title or publication
				elif matchPhase == 2:
					if not (u'title' in item and term in \
						item[u'title'].lower()) and not (u'container-title' in \
						item and term in item[u'container-title'].lower()):
						match = False
						break
			# Sometimes, the year of publication is stored as issued.raw,
			# instead of issued.year. Fix this, if this is the case. We need to
			# explictly remove the 'raw' entry as well.
			if u'issued' in item and u'year' not in item[u'issued']:
				if u'raw' in item[u'issued']:
					item[u'issued'][u'year'] = self.getYear(item[u'issued'][ \
						u'raw'])
				else:
					item[u'issued'][u'year'] = u'date unknown'
			# Fix capitalized DOIs and warn about missing DOIs.
			if self.fixDOI:
				if u'DOI' in item:
					item[u'doi'] = item[u'DOI']
					if item[u'doi'].startswith(u'doi:'):
						item[u'doi'] = item[u'doi'][4:]
				if u'doi' not in item:
					self.msg('Missing DOI: %s' % item[u'title'])
			# Remove URL field
			if self.removeURL:
				if u'URL' in item.keys() and (u'container-title' in \
					item.keys() or u'publisher' in item.keys()):
					del item[u'URL']
			# Convert initials to 'A.B.C.' style to avoid mixups.
			if self.fixAuthorNames and u'author' in item:
				_author = []
				for author in item[u'author']:
					if u'given' not in author or u'family' not in author:
						continue
					given = author[u'given']
					family = author[u'family']
					# First replace dots by spaces
					given = given.replace(u'.', u' ')
					# Concatenate a list of capitalized initials
					given = u''.join([i[0].upper() for i in given.split()])
					# Add dots after each initial
					given = u'. '.join(given) + u'.'
 					_author.append({u'family' : family, u'given': given})
				item[u'author'] = _author
			# Remove empty fields
			for field in item:
				if isinstance(item[field], basestring) and \
					item[field].strip() == u'':
					self.msg(u'Removing empty field: %s' % field)
					del item[field]
			if match:
				matches.append(item)
		return matches

	def splitCitation(self, s):

		"""
		Splits a citation string, like Land1999WhyAnimals, and returns each
		element of the string in a list.

		Arguments:
		s		--	The citation string, e.g. 'Land1999WhyAnimals'.

		Returns:
		A list of citation elements, e.g. ['land', '1999', 'why', 'animals'].
		"""

		# First, split underscore-style citations, like '@land_1999_why_animals'
		if u'_' in s:
			return s.split(u'_')
		regexp = ur'([A-Z][^ 0-9A-Z?!,.\t\n\r\f\v\]\[;]*)'
		# Otherwise, split camelcase-style citations, like @Land1999WhyAnimals.
		l = []
		for t in re.split(regexp, s):
			if t != u'':
				l.append(t.lower().replace(u'+', u' '))
		return l
