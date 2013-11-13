missing-from-wikipedia
======================

Take a file of names, find out which names do NOT have Wikipedia entries, and then spit out that resultant set to a file.

You run it with two options:

> ./missing.py INPUT-FILENAME WIKIPEDIA-PREFIX

1. The file of names to look for. See namelist-sample.txt for an example of how to format it: one name per line.
2. The language Wikipedia you want, as designated by its language prefix. For example, for French Wikipedia, you'd use 'fr' (no quote marks). [See the list of Wikipedias.](https://meta.wikimedia.org/wiki/List_of_Wikipedias)

It then creates a new file containing the output (one name per line), with a filename like "INPUT-FILENAME-[timestamp].txt". You'll also see, on the command line, some statistics about the percentage of people who didn't have Wikipedia pages.

If you have Python installed on your computer, go to a Terminal (or command line), make sure you're in a directory that has the namelist-sample.txt file, and run it like:

> ./missing.py namelist-sample.txt en

and things should just work. Once it's done, you should have a "namelist-sample.2013-12-02-16-59-19.txt" file, or something with a similar name.

More options
============
You might want to change these assumptions in the file:
* put your name in the User-Agent header on line 48
* count redirects as "this page exists": yes (to change to no, remove the "&redirects=" part of the URI on line 53)
