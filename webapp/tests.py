#!/usr/bin/python
#encoding:utf-8
# Copyright 2013 Sumana Harihareswara
# Licensed under the GPL - see LICENSE


import os
import unittest
from missing import *


class input_processing_test(unittest.TestCase):
    def test_fileopen(self):
    # Test that the list splitting-up works.
        testfile = "namelist-sample.txt"
        expectedresult = [u"Mazari, Abu ʿAbd Allah Muhammad al-", u"Mlapa III", u"Andrade, Mário Pinto de", u"Bayram al-Khaʾmis, Mohamed", u"Be’alu Girma", u"Bédié, Henri-Konan", u"Obama, Barack, Sr.", u"Okwei", u"Marie Curie", u"Cleopatra", u"Gandhi, Indira", u"Madikizela-Mandela, Winnie"]
        testresult = getnamefile(testfile)
        self.assertEqual(testresult, expectedresult)


class name_processing_test(unittest.TestCase):
    def test_name_reversal_hyphenation(self):
    # Test that names of 1 or 2 items reverse and remove hyphen spaces properly.
        testnames = ["Mazari, Abu ʿAbd Allah Muhammad al-", "Mlapa III", "Andrade, Mário Pinto de", "Bayram al-Khaʾmis, Mohamed", "Be’alu Girma", "Bédié, Henri-Konan", "Okwei"]
        expectedresult = ["Abu ʿAbd Allah Muhammad al-Mazari", "Mlapa III", "Mário Pinto de Andrade", "Mohamed Bayram al-Khaʾmis", "Be’alu Girma", "Henri-Konan Bédié", "Okwei"]
        testresult = massagenames(testnames)
        self.assertEqual(testresult, expectedresult)

    def test_three_item_reversal(self):
    # Test that special three-name items reverse appropriately.
        testname = ["Obama, Barack, Sr."]
        expectedresult = ["Barack Obama Sr."]
        testresult = massagenames(testname)
        self.assertEqual(testresult, expectedresult)


class page_existence_test(unittest.TestCase):

    def setUp(self):
        self.notablepeople = ["Booker T. Washington", "Angie Zapata"]
        self.imaginarypeople = ["NEVEREXISTS"]

    def test_existing_page(self):
    # Check that we know an existing page exists.
    # Resulting list should have 0 names in it
        testresults = leftout(self.notablepeople, "en")
        self.assertEqual(len(testresults), 0)

    def test_nonexistent_page(self):
    # Check that we know a nonexistent page is nonexistent.
        testresults = leftout(self.imaginarypeople, "en")
        self.assertEqual(testresults, ["NEVEREXISTS"])

    def test_mixed_people(self):
    # Check a mixed group; should result in ONLY the nonexistent page.
        people = self.imaginarypeople + self.notablepeople
        testresults = leftout(people, "en")
        self.assertEqual(testresults, ["NEVEREXISTS"])

class stats_test(unittest.TestCase):
    def setUp(self):
        self.testfile = "namelist-sample.txt"

    def test_percentage(self):
        expectedresult = 50
        names = getnamefile(self.testfile)
        querynames = massagenames(names)
        results = leftout(querynames, "en")
        testresult = generate_statistics(results, names)
        self.assertEqual(testresult["ratio"], expectedresult)


def main():
    unittest.main()

if __name__ == "__main__":
    main()
