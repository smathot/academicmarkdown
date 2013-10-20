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
		odtStyle=None, fixDOI=True, verbose=False):
		
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
			self.msg(u'Found citation "%s"' % queryString)
			if queryString in oldQueries:
				continue
			oldQueries.append(queryString)
			matches = self.bestMatch(queryString)
			if len(matches) == 0:
				self.msg(u'No matches for "%s"' % queryString)
				continue
			if len(matches) > 1:
				self.msg(u'Multiple matches (%d) for "%s"' % \
					(len(matches), queryString))				
			match = matches[0]
			match[u'id'] = queryString
			if self.odtStyle != None:
				match[u'title'] += u'<!--odt-style="%s"-->' % self.odtStyle
			items.append(match)
		# TODO Placing the citation info in the YAML block doesn't appear to
		# work. So for now save it as a JSON file.
		fd = open(u'.bibliography.json', u'w')
		json.dump(items, fd)
		fd.close()
		if self.headerText == None or self.headerLevel == None:
			return md
		return md + u'\n\n%s %s\n\n' % (u'#' * self.headerLevel, self.headerText)

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
			items = self.zotero.top(q=query[0].encode(u'utf-8'), limit=100, \
				content=u'csljson')
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
			if self.fixDOI and u'DOI' in item:
				item[u'doi'] = item[u'DOI']
				if item[u'doi'].startswith(u'doi:'):
					item[u'doi'] = item[u'doi'][4:]
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
				l.append(t.lower())
		return l
