# Academic Markdown

*Who knew writing could be so nerdy?*

version %-- python: "from academicmarkdown import version; print version" --%

Copyright 2013-2014 Sebastiaan Mathôt

## Contents

%--
toc:
 mindepth: 2
 exclude: [Contents]
--%

## About

Academic Markdown is a Python module that allows you generate `.md`, `.html`, `.pdf`, `.docx`, and `.odt` files from Markdown source. [Pandoc] is used for most of the heavy lifting, so refer to the Pandoc website for detailed information about writing in Pandoc Markdown. However, Academic Markdown offers some additional functionality that is useful for writing scientific documents, such as integration with [Zotero references], and a number of useful [Academic Markdown extensions].

At present, the main target for Academic Markdown is the OpenSesame documentation site, <http://osdoc.cogsci.nl/>, although it may in time grow into a more comprehensive and user-friendly tool.

## Example

This `readme` is itself an example of a document written in Academic Markdown. For exports in various formats, see the `/readme/` sub folder included with the source code.

## Download

You can download the latest release of Academic Markdown here:

- <https://github.com/smathot/academicmarkdown/releases>

Ubuntu users can install Academic Markdown from the Cogsci.nl PPA:

	sudo add-apt-repository ppa:smathot/cogscinl
	sudo apt-get update
	sudo apt-get install python-academicmarkdown

## Basic usage

Academic Markdown assumes that input files are encoded with `utf-8` encoding.

~~~ {.python}
from academicmarkdown import build
build.HTML(u'input.md', u'output.html')
build.HTML(u'input.md', u'output.html', standalone=False)
build.PDF(u'input.md', u'output.pdf')
build.DOCX(u'input.md', u'output.docx')
build.ODT(u'input.md', u'output.odt')
~~~

A number of options can be specified by setting attributes of the `build` module, like so

~~~ {.python}
build.spacing = 30, 0
~~~

The full list of options is available in `academicmarkdown/constants.py`, or see [Appendix: `constants`].

## Dependencies

Academic Markdown has been tested exclusively on Ubuntu Linux. The following dependencies are required:

- [pandoc] is used for most of the heavy lifting. At the time of writing, the Ubuntu repositories do not contain a sufficiently recent version of Pandoc. Therefore, if you encounter trouble, try installing the latest version of Pandoc manually.
- [pyzotero] is necessary for extracting Zotero references.
- [wkhtmltopdf] is necessary for converting to `.pdf`. For best results, use the latest statically linked release, instead of the version from the Ubuntu repositories.

## Zotero references

### Pandoc citation style

Since the basic Markdown conversion is performed by Pandoc, citations should be formatted as described on the Pandoc site:

- <http://johnmacfarlane.net/pandoc/README.html#citations>

### Zotero API key and library ID

You can automatically extract references from your Zotero library by setting the `zoteroApiKey` and `zoteroLibraryId` properties. Your references are not extracted from your local Zotero database, but through the web API of <http://www.zotero.org>. This means that you need to have a Zotero account and synchronize your local database with your account, in order to use this feature. You can find your your API key and library ID online on your Zotero profile page.

~~~ {.python}
from academicmarkdown import build
build.zoteroApiKey = u'myapikey'
build.zoteroLibraryId = u'mylibraryid'
build.PDF(u'input.md', u'output.pdf')
~~~

### Citation identifiers

Citations are split into separate terms using camelcase or undescore logic. An example of an underscore-style citation is `@bárány_halldén_1948`. And example of a camelcase-style citation is `@Land1999WhyAnimals`. Each citation is interpreted as a series of author names, followed by the year of publication, optionally followed by terms that match either the publication title, or the article title. So the following reference ...

Land, M., Mennie, N., & Rusted, J. (1999). The roles of vision and eye movements in the control of activities of daily living. *Perception*, *28*(11), 1311–1328.

... matches any of the following terms:

- `@Land1999`
- `@Land1999Roles`
- `@LandMennie1999`
- `@LandRusted1999Percept`
- `@land_rusted_1999_percept`
- etc.

If a name contains spaces, you can indicate this using a `+` character. So the following reference ...

Van Zoest, W., & Donk, M. (2005). The effects of salience on saccadic target selection. *Visual Cognition*, *12*(2), 353–375.

... matches any of the following terms:

- `@Van+zoestDonk2005`
- `@van+zoest_donk_2005`

Note that you must consistently use the same citation to refer to a single reference in one document. If a citation matched multiple references from your Zotero database, one citation will be chosen at random.

### Sorting citations

Pandoc does not allow you to sort your references, which can be annoying. To get around this, Academic Markdown allows you to explicitly sort your citations by linking chains of citations with a `+` character:

	[@Zzz2014]+[@Aaa2014]

### Clearing cache

Previous references will be cached automatically. To refresh, remove the file `.zoteromarkdown.cache` or run your Python script with the command-line argument: `--clear-cache`.

## Academic Markdown extensions

Academic Markdown provides certain extensions to regular Markdown, in the form of YAML blocks embedded in `%-- --%` tags. You can which, and the order in which, extensions are called by settings the `extensions` list:

~~~ {.python}
from academicmarkdown import build
# First call the include extension, second call the figure extension
build.extensions = [u'include', u'figure']
~~~

### `code`: Code listings

%--
python: |
 import inspect
 from academicmarkdown import CodeParser
 print inspect.getdoc(CodeParser)
--%

### `exec`: external commands

%--
python: |
 import inspect
 from academicmarkdown import ExecParser
 print inspect.getdoc(ExecParser)
--%

### `figure`: figures

%--
python: |
 import inspect
 from academicmarkdown import FigureParser
 print inspect.getdoc(FigureParser)
--%

### `include`: include other Markdown files

%--
python: |
 import inspect
 from academicmarkdown import IncludeParser
 print inspect.getdoc(IncludeParser)
--%

### `python`: python code

%--
python: |
 import inspect
 from academicmarkdown import PythonParser
 print inspect.getdoc(PythonParser)
--%

### `table`: table

%--
python: |
 import inspect
 from academicmarkdown import TableParser
 print inspect.getdoc(TableParser)
--%

### `toc`: table of contents

%--
python: |
 import inspect
 from academicmarkdown import TOCParser
 print inspect.getdoc(TOCParser)
--%

### `wc`: word count

%--
python: |
 import inspect
 from academicmarkdown import WcParser
 print inspect.getdoc(WcParser)
--%

### Magic variables

Magic variables are automatically replaced by certain values, and are indicated like this: `%varname%`. The following magic variables are available:

- `%wc%`: Word count
- `%cc%`: Character count
- `%rc%`: Reference count

## License

Academic Markdown is available under the GNU General Public License 3. For more information, see the included file `COPYING`.

## Appendix: `constants`

%--
code:
 id: LstConstants
 syntax: python
 source: academicmarkdown/constants.py
--%

[pandoc]: http://johnmacfarlane.net/pandoc/
[pyzotero]: http://pyzotero.readthedocs.org/
[zotero]: http://www.zotero.org/
[wkhtmltopdf]: https://code.google.com/p/wkhtmltopdf/
