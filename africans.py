#!/usr/bin/python

import requests

starterlist= ['Kayibanda, Grégoire','Kayoya, Michel','Kazahendike, Urieta','Kazibwa, Specioza Wandira','Kebede Mikael','Keen, John','Keino, Kip','Kéita, Aoua','Keita, Fodéba','Keïta, Modibo','Keïta, Salif','Keïta, Seydou']

# massage names to make them firstname lastname

pagelist = []

for elem in starterlist:
    elem = elem.split(", ")
    elem.reverse()
    pagelist.append(" ".join(elem))

print "pagelist: %s" % pagelist


# massagednames = map(lambda elem:" ".join(elem.split(",").reverse()), starterlist)
# gets a TypeError; figure it out later.

# for each name, do a search to see whether the pages exist on english wikipedia

# spit out list of who is left out
