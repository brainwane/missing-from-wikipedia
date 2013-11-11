#!/usr/bin/python
#encoding:utf-8
# The point of this script is to take a giant list of 2126 names from the Dictionary of African Biography Oxford Reference, check which names do not have an English Wikipedia entry, and then spit out that resultant set.
# Note: to find out who actually did have an entry, do a simple set operation for difference between set(pagelist) and set(starterlist)

import requests
import pprint

# starting with a small hardcoded sample to see what works

starterlist= [u'Kayibanda, Grégoire',u'Kayoya, Michel',u'Kazahendike, Urieta',u'Kazibwa, Specioza Wandira',u'Kebede Mikael',u'Keen, John',u'Keino, Kip',u'Kéita, Aoua',u'Keita, Fodéba',u'Keïta, Modibo',u'Keïta, Salif',u'Keïta, Seydou']

def massagenames(namelist):
    """massage names to make them firstname lastname"""
    return map(lambda elem:" ".join(elem.split(", ")[::-1]), starterlist)

def leftout(origlist, formattedlist):
    """return list of people who don't have pages on English Wikipedia

    for each name, do a search to see whether the page exists on english wikipedia
    sample title that does not exist: Narrrgh
    /w/api.php?action=query&prop=info&format=json&titles=Narrrgh: if ["query"]["pages"] has a negative int like -1, -2, etc. as a key, and if a key within that dict has the value "missing" (value: ""), then the page is missing from enwiki
    TODO: use pipes, e.g. Narrgh|Call Me Maybe|NEVEREXISTS in titles= , to make multiple queries at once."""
    unsung = []
    for x, elem in enumerate(formattedlist):
        payload = dict(titles=elem)
        r = requests.get("http://en.wikipedia.org/w/api.php?action=query&prop=info&format=json, data=payload")
        if "-1" in r["query"]["pages"]:
            if "missing" in r["query"]["pages"]["-1"]:
                unsung.append(starterlist[x])
    return unsung

# spit out list of who is left out
