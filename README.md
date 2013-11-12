missing-from-wikipedia
======================

Take a file of names, find out which names do NOT have Wikipedia entries, and then spit out that resultant set to a file.

You run it like:

> ./missing.py INPUT-FILENAME WIKIPEDIA-PREFIX OUTPUT-FILENAME

1. The file of names to look for. See namelist-sample.txt for an example of how to format it: one name per line.
2. The language Wikipedia you want, as designated by its language prefix. For example, for French Wikipedia, you'd use 'fr' (no quote marks). [See the list of Wikipedias.](https://meta.wikimedia.org/wiki/List_of_Wikipedias)
3. The name of the file where the program will write the list of names missing entries. The script will write them one per line.


You might want to change these assumptions in the file:
* put your name in the User-Agent header on line 43
* count redirects as "this page exists": yes (to change to no, remove the "&redirects=" part of the URL on line 48)

If you have Python installated on your computer, go to a Terminal (or command line), make sure you're in a directory that has a namelist.txt file, and run it like:

> ./missing.py namelist-sample.txt en missing-people.txt

and things should just work. Once it's done, you should have a "missing-people.txt" file.
