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

import os
import yaml
from academicmarkdown import YAMLParser
import subprocess
import sys

videoTemplate = {
	u'vimeo' : u"""
<iframe id="%(id)s" src="//player.vimeo.com/video/%(videoid)s?color=8ae234" width="%(width)d" height="%(height)d" class="video vimeo" allowfullscreen>
</iframe>
<div class='vid-caption'><strong>Video %(nVid)d.</strong> %(caption)s</div>
""",
	u'youtube' : u"""
<iframe id="%(id)s" width="%(width)d" height="%(height)d" src="//www.youtube.com/embed/%(videoid)s" class="video youtube" allowfullscreen>
</iframe>
<div class='vid-caption'><strong>Video %(nVid)d.</strong> %(caption)s</div>
"""
}

class VideoParser(YAMLParser):

	"""
	Embeds a video. Currently, YouTube and Vimeo sources are supported. The
	keywords `width`, `height`, and `caption` are optional.

	%--
	video:
	 id: VidRefresh
	 source: vimeo
	 videoid: 24216910
	 width: 640
	 height: 240
	 caption: "A figure caption"
	--%

	"""

	def __init__(self, verbose=False):

		"""
		Constructor.

		Keyword arguments:
		verbose		--	Indicates whether verbose output should be generated.
						(default=False)
		"""

		super(VideoParser, self).__init__(_object=u'video', required=['id', \
			'source', 'videoid'], verbose=verbose)

	def parse(self, md):

		"""See BaseParser.parse()."""

		self.nVid = 0
		return super(VideoParser, self).parse(md)

	def parseObject(self, md, _yaml, d):

		"""See YAMLParser.parseObject()."""

		self.nVid += 1
		d['nVid'] = self.nVid
		self.msg(u'Found video: %s (%d)' % (d['id'], self.nVid))
		if u'caption' not in d:
			d[u'caption'] = u''
		if u'width' not in d:
			d[u'width'] = 640
		if u'height' not in d:
			d[u'height'] = 320
		vid = videoTemplate[d[u'source']] % d
		md = md.replace(_yaml, vid)
		md = md.replace(u'%%%s' % d[u'id'], u'[Video %d](#%s)' % (self.nVid, \
			d[u'id']))
		return md

