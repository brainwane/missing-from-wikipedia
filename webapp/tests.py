#!/usr/bin/python
#encoding:utf-8
# Copyright 2013 Sumana Harihareswara
# Licensed under the GPL - see LICENSE


import os
import unittest
import time
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
    # Test that names of 1 or 2 items reverse & remove hyphen spaces properly.
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
        self.testinfile = "namelist-sample.txt"
        self.expectedresult = 50
        self.names = getnamefile(self.testinfile)
        self.querynames = massagenames(self.names)
        self.results = leftout(self.querynames, "en")
        self.testresult = generate_statistics(self.results, self.names)
        self.testoutfilename = "testresulttodelete.txt"
        outputfile(self.results, self.testoutfilename)

    def test_percentage(self):
        self.assertEqual(self.testresult["ratio"], self.expectedresult)

    def test_stat_results(self):
        expectedresult = """Your output file: testresulttodelete.txt
6 people (50 percent of the 12 people listed in namelist-sample.txt) do not have en.wikipedia.org pages about them.
Change that: https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Countering_systemic_bias
In your language: https://www.wikidata.org/wiki/Q4656680\n"""
        teststats = stat_results(self.testinfile, self.testoutfilename, "en", self.testresult)
        self.assertEqual(teststats, expectedresult)

    def tearDown(self):
        os.remove(self.testoutfilename)


class file_test(unittest.TestCase):
    def setUp(self):
        self.testfile = "testoffilewrite.txt"
        self.testlist = ["hey there"]
        outputfile(self.testlist, self.testfile)

    def test_outputfile(self):
        with codecs.open(self.testfile, encoding='utf-8', mode='r') as f:
            testresult = f.read()
        self.assertEqual(testresult, u"hey there\n")

    def test_nameoutputfile(self):
        testresult1 = nameoutputfile(self.testfile)
        time.sleep(1)
        testresult2 = nameoutputfile(self.testfile)
        self.assertNotEqual(testresult1, testresult2)
        self.assertIn(self.testfile[:15], testresult1)
        self.assertIn(self.testfile[16:], testresult1)
        weirdname = "bleeee"
        testresult3 = nameoutputfile(weirdname)
        self.assertNotIn(".", testresult3)
        self.assertEqual(testresult3[:7], "bleeee-")

    def tearDown(self):
        os.remove(self.testfile)


class integration_test(unittest.TestCase):
    def setUp(self):
        pass

    def test_run_function(self):
        # need testdata file and
        pass

    def tearDown(self):
        pass


def main():
    unittest.main()

if __name__ == "__main__":
    main()
