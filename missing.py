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


# Constants
CHUNK_SIZE = 50 # Can send up to 50 titles in 1 API query, at least on English Wikipedia.
DEFAULT_HEADERS = {
    'User-Agent': 'missing-from-wikipedia project (https://github.com/brainwane/missing-from-wikipedia/), using Python requests library'
}


def getnamelist(filename):
    """Open the file and turn it into a list split up by newlines."""
    with codecs.open(filename, encoding='utf-8') as f:
        fstr = f.read()
        namelist = fstr.split("\n")
    return namelist


def massagenames(names):
    """Take list, make each name firstname lastname, then return a list of old-and-new tuples."""
    massaged = map(lambda elem: " ".join(elem.split(", ")[::-1]), names)
    massaged = [name[1].replace("- ", "-") for name in enumerate(massaged)]  # dealing with names with "al-" & similar strings
    return massaged

def chunknames(names):
    """A generator to yield up CHUNK_SIZE name pairs at a time."""
    while names:
        yield names[:CHUNK_SIZE]
        names = names[CHUNK_SIZE:]


def leftout(massaged_names, wikipedia_language, resultfile):
    """Return list of people who don't have pages on the wiki.

    For each name, do a check to see whether the page exists on the wiki (as specified via command-line argument).
       Sample title that does not exist: Narrrgh
       API call goes to: /w/api.php?action=query&prop=info&format=json&titles=Narrrgh&redirects=&maxlag=5
    If ["query"]["pages"] has a negative int like -1, -2, etc. as a key, and if a key within that dict has the value "missing" (value: ""), then the page is missing from the wiki.
    We use pipes, e.g. Narrgh|Call Me Maybe|NEVEREXISTS in titles= , to make multiple queries at once.
    Currently accepts redirects as meaning the page exists. TODO: if the redirect is to a page that is NOT a biography (e.g., it redirects to the page for a war), then count that person as unsung."""
    
    for chunk in chunknames(massaged_names):
        payload = dict(titles="|".join(chunk))
        URI = "http://%s.wikipedia.org/w/api.php?action=query&prop=info&format=json&redirects=&maxlag=5" % wikipedia_language
        request = requests.get(URI, params=payload, headers=DEFAULT_HEADERS)
        for key in request.json()["query"]["pages"]:
            if "missing" in request.json()["query"]["pages"][key]:
                outputfile(request.json()["query"]["pages"][key]["title"], resultfile)


def outputfile(pagename, filename):
    with codecs.open(filename, encoding='utf-8', mode='a') as out_fd:
        out_fd.write("%s\n" % pagename)


def nameoutputfile(name):
    """Name the output file: the input filename plus timestamp.

    Will not overwrite output file unless run more than once per second."""
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    pos = name.rfind('.')
    return "%s-%s.%s" % (name[:pos], now, name[pos+1:]) if pos > 0 else "%s-%s" % (name, now)


def generate_statistics(file_with_missing_entries, original_list_of_names):
    """Command-line output with stats and call to action.

    Tell user the percentage of people who do not have wiki pages about them.
    Suggest things to do about that.

    Takes the resultfile from leftout and the list from getnamelist."""
    with codecs.open(file_with_missing_entries, encoding='utf-8', mode='r') as fd:
        number_of_missing_entries = len(list(fd))

    number_of_original_entries = len(original_list_of_names)
    percentage = 100 * (float(number_of_missing_entries) / float(number_of_original_entries))
    return {'ratio': percentage, 'original': number_of_original_entries, 'missing': number_of_missing_entries}


def print_results(input_file, file_with_missing_entries, wikipedia_language, stats):
    print """Your output file: %(outfile)s
%(unsungnum)s people (%(pct).0f percent of the %(orignum)s people listed in %(infile)s) do not have %(lang)s.wikipedia.org pages about them.
Change that: https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Countering_systemic_bias
In your language: https://www.wikidata.org/wiki/Q4656680\n""" % {
        'outfile': file_with_missing_entries, 
        'unsungnum': stats['missing'], 
        'pct': stats['ratio'], 
        'orignum': stats['original'], 
        'infile': input_file, 
        'lang': wikipedia_language}


def run():
    (inputfilename, wikipedia_language) = sys.argv[1:]
    outputfilename = nameoutputfile(inputfilename)
    names = getnamelist(inputfilename)
    querynames = massagenames(names)
    leftout(querynames, wikipedia_language, outputfilename)
    stats = generate_statistics(outputfilename, names)
    print_results(inputfilename, outputfilename, wikipedia_language, stats)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        run()
    else:
        print "Usage: ./%s <input-filename> <wikipedia-language-code>" % sys.argv[0]
