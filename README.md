missing-from-wikipedia
======================

Take a file of names, find out which names do NOT have Wikipedia entries, and then spit out that resultant set to a file.

You might want to change these assumptions in the file:
* original file: "namelist.txt" (on the last line, line 66)
* file to write to: "missing-people.txt" (on the last line, line 66)
* put your name in the User-Agent header on line 43
* wiki to check: English Wikipedia (the URL on line 48)
* count redirects as "this page exists": yes (to change to no, remove the "&redirects=" part of the URL on line 48)

If you have Python installated on your computer, go to a Terminal (or command line), make sure you're in a directory that has a namelist.txt file, and run:

> python missing.py

and things should just work. Once it's done, you should have a "missing-people.txt" file.
