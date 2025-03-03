import unittest
from TestUtils import TestParser

class ParserSuite(unittest.TestCase):


    def test_correct_1(self):
        input = \
        """
        func something() int {
            for index := 0; index < 100; index := index + 3 {
                if (index == 1) {
                    break;
                } else if (index == 2) {
                    return (index * 100) - index;
                } else if (index % 3 == 0) {
                    continue;
                } else {
                    return -1
                }
            }
            return index;
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,201))