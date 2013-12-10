#!/usr/bin/python
#encoding:utf-8
# Copyright 2013 Sumana Harihareswara
# Licensed under the GPL - see LICENSE
# The point of this script is to take a giant list of names from some source
# file, check which names do not have an entry on one language's Wikipedia,
# and then spit out that resultant set to a file. The command-line options let
# you specify the wiki to check and the filenames to read and write.

# Please add your name to the User-Agent in the headers dict in DEFAULT_HEADERS.

# Note: to find out who actually did have an entry on the wiki, do a simple set
# operation for difference between the original namelist and the file that
# comes out at the end.


import codecs
import requests
import sys
from datetime import datetime
import MySQLdb


# Constants
CHUNK_SIZE = 50  # Can send up to 50 titles in 1 API query, at least on English Wikipedia.
DEFAULT_HEADERS = {
    'User-Agent': 'missing-from-wikipedia project (https://github.com/brainwane/missing-from-wikipedia/), using Python requests library'
}


def getnamefile(filename):
    """Open the file and turn it into a list split up by newlines."""
    with codecs.open(filename, encoding='utf-8') as f:
        namelist = [line.strip('\n') for line in f]
    return namelist


def massagenames(names):
    """Take list of strings, make each name firstname lastname, then return list of processed names."""
    def process_name(name):
        if not isinstance(name, unicode):
            name = name.decode('utf-8')
        parts = name.split(", ")
        # flip first and last names
        if (len(parts) > 1):
            parts[0], parts[1] = parts[1], parts[0]

        # special case with "lastname, firstname, suffix"
        # fix to "firstname lastname, suffix"
        if (len(parts) == 3):
            inprogress = "%s %s, %s" % (parts[0], parts[1], parts[2])
        else:
            inprogress = " ".join(parts)
        # replace hyphens
        inprogress = inprogress.replace("- ", "-")
        final = inprogress.replace(" ", "_")
        return final
    return [process_name(name) for name in names]


def chunknames(names):
    """A generator to yield up CHUNK_SIZE name pairs at a time."""
    while names:
        yield names[:CHUNK_SIZE]
        names = names[CHUNK_SIZE:]

def getconnection(wikipedia_language):
    db = MySQLdb.connect(read_default_file='~/replica.my.cnf',
                         host=wikipedia_language+"wiki.labsdb",
                         db=wikipedia_language+"wiki_p",
                         charset='utf8',
                         use_unicode=True)
    return db.cursor()

def leftout(massaged_names, wikipedia_language):
    """Return list of people who don't have pages on the wiki.

    For each name, do a check to see whether the page exists on the wiki (as specified via command-line argument).

    Uses a direct MySQL check on the replicated database.
"""

    cur = getconnection(wikipedia_language)
    sql = u"SELECT page_title FROM page WHERE page_title in (%s) AND page_namespace=0;"
    format_strings = u','.join(['%s'] * len(massaged_names))
    cur.execute(sql % format_strings , massaged_names)
    sqlresults = cur.fetchall()
    exists_set = set(map(lambda x: x[0], sqlresults))
    resultset = set(massaged_names).difference(exists_set)
    return list(resultset)


def outputfile(resultlist, filename):
    with codecs.open(filename, encoding='utf-8', mode='a') as out_fd:
        [out_fd.write("%s\n" % pagename) for pagename in resultlist]


def nameoutputfile(name):
    """Name the output file: the input filename plus timestamp.

    Will not overwrite output file unless run more than once per second."""
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    pos = name.rfind('.')
    return "%s-%s.%s" % (name[:pos], now, name[pos+1:]) if pos > 0 else "%s-%s" % (name, now)


def generate_statistics(resultlist, original_list_of_names):
    """Command-line output with stats and call to action.

    Tell user the percentage of people who do not have wiki pages about them.
    Suggest things to do about that.

    Takes the resultfile from leftout and the list from getnamefile."""
    number_of_missing_entries = len(resultlist)
    number_of_original_entries = len(original_list_of_names)
    percentage = 100 * (float(number_of_missing_entries) / float(number_of_original_entries))
    return {'ratio': percentage, 'original': number_of_original_entries, 'missing': number_of_missing_entries}


def stat_results(input_file, file_with_missing_entries, wikipedia_language, stats):
    return """Your output file: %(outfile)s
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
    names = getnamefile(inputfilename)
    querynames = massagenames(names)
    results = leftout(querynames, wikipedia_language)
    outputfile(results, outputfilename)
    stats = generate_statistics(results, names)
    print(stat_results(inputfilename, outputfilename, wikipedia_language, stats))


if __name__ == "__main__":
    if len(sys.argv) > 2:
        run()
    else:
        print "Usage: ./%s <input-filename> <wikipedia-language-code>" % sys.argv[0]
