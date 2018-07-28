import unittest
import config
from flatcsvparser import ImpRecFlatFile

imp_rec_filename = "IMP_REC_2018_07_06_10_30_43_762.csv"


class TestImpRecMethods(unittest.TestCase):
    def test_group_by_reception(self):
        with open(imp_rec_filename, "r") as imp_rec_file:
            imp_rec = ImpRecFlatFile(imp_rec_file, config.CONFIG)
            res = imp_rec.get_reception_by_id("00181373")
            self.assertEquals(len(res), 4)


def suite():
    suite = unittest.TestSuite()
    suite.add(TestImpRecMethods('test_group_by_reception'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

