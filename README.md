missing-from-wikipedia
======================

A Flask web app to take a file or list of names, find out which names do NOT have Wikipedia entries, and then spit out that resultant set as links to create those pages on the target Wikipedia. [Wikimedia's Tool Labs hosts an instance of this app.](https://tools.wmflabs.org/missing-from-wikipedia/index)

See namelist-sample.txt for an example of how to format a file you can pass into the app: one name per line.

If you want a command-line version you can run to use the MediaWiki web API, see [commit 3246205a9fc67d4c1abfe43c9c2a67ef723b4936](https://github.com/brainwane/missing-from-wikipedia/tree/3246205a9fc67d4c1abfe43c9c2a67ef723b4936).

[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)

Known bugs
==========

# Unicode problems - if you pass in a string with Unicode characters, even if a page with that name exists, it'll falsely say that the page doesn't exist.
# SQL escaping problems - if you pass in a string with a single quotation mark in it, same problem as above.
# Only checks the Latin representation, thus leading to false positives -- need to hit Wikidata database and use Universal Language Selector to really address this.
