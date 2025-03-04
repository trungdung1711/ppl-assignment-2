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


    def test_correct_2(self):
        input = \
        """
        var arr [3][4][5][CONST]float = [2][3]float{ {1.2, 2.2, 3.3} , {4.5, 5.6, 7.8} , 1.125 }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,202))