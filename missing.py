#!/usr/bin/python
#encoding:utf-8
# Copyright 2013 Sumana Harihareswara
# Licensed under the GPL - see LICENSE
# The point of this script is to take a giant list of names from some source
# file, check which names do not have an entry on one language's Wikipedia,
# and then spit out that resultant set to a file. The command-line options let
# you specify the wiki to check and the filenames to read and write.

# Please add your name to the User-Agent in the headers dict in 'leftout'.

# Note: to find out who actually did have an entry on the wiki, do a simple set
# operation for difference between the original namelist and the file that
# comes out at the end.

# test names include: Mazari, Abu ʿAbd Allah Muhammad al- ; Mlapa III; Andrade, Mário Pinto de; Bayram al-Khaʾmis, Mohamed; Be’alu Girma; Bédié, Henri-Konan; Obama, Barack, Sr.; Okwei

import requests
import codecs
import sys
from datetime import datetime


def getnamelist(filename):
    """Open the file and turn it into a list split up by newlines."""
    with codecs.open(filename, encoding='utf-8') as f:
        fstr = f.read()
        namelist = fstr.split("\n")
    return namelist


def massagenames(nlist):
    """Take list, make each name firstname lastname, then return a list of old-and-new tuples."""
    mlist = map(lambda elem: " ".join(elem.split(", ")[::-1]), nlist)
    mlist = [name[1].replace("- ", "-") for name in enumerate(mlist)]  # dealing with names with "al-" & similar strings
    return zip(nlist, mlist)


def chunknames(tuplelist):
    """A generator to yield up 50 name pairs at a time.

    Can send up to 50 titles in 1 API query, at least on English Wikipedia."""
    while tuplelist:
        yield tuplelist[:50]
        tuplelist = tuplelist[50:]


def leftout(nametuples, wikipedia, resultfile):
    """Return list of people who don't have pages on the wiki.

    For each name, do a check to see whether the page exists on the wiki (as specified via command-line argument).
       Sample title that does not exist: Narrrgh
       API call goes to: /w/api.php?action=query&prop=info&format=json&titles=Narrrgh&redirects=&maxlag=5
    If ["query"]["pages"] has a negative int like -1, -2, etc. as a key, and if a key within that dict has the value "missing" (value: ""), then the page is missing from the wiki.
    We use pipes, e.g. Narrgh|Call Me Maybe|NEVEREXISTS in titles= , to make multiple queries at once.
    Currently accepts redirects as meaning the page exists. TODO: if the redirect is to a page that is NOT a biography (e.g., it redirects to the page for a war), then count that person as unsung."""

    headers = {'User-Agent': 'missing-from-wikipedia project (https://github.com/brainwane/missing-from-wikipedia/), using Python requests library'}
    g = chunknames(nametuples)
    for chunk in g:
        names = [x[1] for x in chunk]
        payload = dict(titles="|".join(names))
        URI = "http://%s.wikipedia.org/w/api.php?action=query&prop=info&format=json&redirects=&maxlag=5" % wikipedia
        r = requests.get(URI, params=payload, headers=headers)
        for key in r.json()["query"]["pages"]:
            if "missing" in r.json()["query"]["pages"][key]:
                outputfile(r.json()["query"]["pages"][key]["title"], resultfile)
        # print("just ran a chunk, yo") # for debugging

# spit out list of who is left out


def outputfile(pagename, fname):
    with codecs.open(fname, encoding='utf-8', mode='a') as u:
        u.write(pagename)
        u.write("\n")


def nameoutputfile(startfile):
    """Name the output file: the input filename plus timestamp.

    Will not overwrite output file unless run more than once per second."""
    base = startfile.split('.txt')[0]
    now = datetime.utcnow().isoformat('-')
    now = now[:19].replace(':', '-')
    return "%s-%s.txt" % (base, now)


def ratio(missed, orig, origfile, wikipedia):
    """Command-line output with stats and call to action.

    Tell user the percentage of people who do not have wiki pages about them.
    Suggest things to do about that.

    Takes the resultfile from leftout and the list from getnamelist."""
    with codecs.open(missed, encoding='utf-8', mode='r') as g:
        a = float(len(list(g)))
    b = len(orig)
    percentage = 100*(a/b)
    print """Your output file: %(outfile)s
%(unsungnum)s people (%(pct).0f percent of the %(orignum)s people listed in %(infile)s) do not have %(lang)s.wikipedia.org pages about them.
Change that: https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Countering_systemic_bias
In your language: https://www.wikidata.org/wiki/Q4656680\n""" % {'outfile': missed, 'unsungnum': int(a), 'pct': percentage, 'orignum': b, 'infile': origfile, 'lang': wikipedia}


def run():
    (inputfile, wiki) = sys.argv[1:]
    out = nameoutputfile(inputfile)
    listofnames = getnamelist(inputfile)
    querynames = massagenames(listofnames)
    leftout(querynames, wiki, out)
    ratio(out, listofnames, inputfile, wiki)


if __name__ == "__main__":
    """Run as: ./missing.py input-filename Wikipedia-code output-filename"""
    run()
