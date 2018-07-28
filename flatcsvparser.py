import csv
import config
import importlib
import os.path
import re
import testlib.common
import argparse


def get_struct_from_pattern(conf_obj, filepath):
    """
    Search in the configuration object for a file structure matching the pattern of the file
    :param conf_obj: CsvParserConfig object
    :param filepath: path to the file to parse
    :return: A CsvFlatFileStructure object
    """
    basename = os.path.basename(filepath)
    conf_structures = conf_obj.file_structures

    structures = [conf_structures[struc_name] for struc_name in conf_structures if re.match(conf_structures[struc_name].file_pattern, basename) is not None]

    if len(structures) == 0:
        return None
    if len(structures) != 1:
        raise Exception("More than one structure found for this pattern")

    return structures[0]


class CsvFlatFile(object):
    def __init__(self, file, structure):
        self.structure = structure
        self.filename = file.name
        rows = list(csv.reader(file, delimiter=self.structure.sep, quotechar="\""))
        self.rows = rows

    def parse_groups(self):
        """
        Parses a group of a rows with a give common key
        :returns: an array og rows with the same key
        """
        groups = {}
        for idx, row in enumerate(self.rows):
            row_type = row[self.structure.type_pos - 1]
            keys = [struct.key_pos for struct in self.structure.row_structures if row_type == struct.type]
            if len(keys) == 0:
                raise Exception("Could not find key for line type" + row_type + ". Row " + str(idx) + " of file "
                                + self.filename)
            key_pos = keys[0]
            row_key = row[key_pos - 1]
            if row_key not in groups:
                groups[row_key] = []
            groups[row_key].append(row)

        return groups

    def run_test_case(self, test_name):
        """
        Run the test test_name. It must be implemented in a submodule within the testlib module
        :param test_name: name of the test. If two test have the same name, the first will be uesed
        :return: the result of the test inside a TestCaseResult object
        """
        for idx, module_name in enumerate(config.TEST_MODULES):
            module = importlib.import_module("testlib." + module_name)
            if test_name in dir(module):
                break
            del module
            if idx == (len(config.TEST_MODULES) - 1):
                 raise Exception("Could not find the test in modules")
        test_function = getattr(module, test_name)
        return test_function(self)

    def run_test_suite(self, test_list):
        suite_result = testlib.common.TestSuiteResult()
        for test in test_list:
            tc_result = self.run_test_case(test)
            suite_result.tcs.append(tc_result)
        return suite_result

    def run_defined_tests(self):
        return self.run_test_suite(self.structure.tests)

    def list_keys(self):
        return self.parse_groups().keys()


class ImpRecFlatFile(CsvFlatFile):
    def __init__(self, file, config_object):
        structure = config_object.file_structures[config.IMP_REC_STRUCT_NAME]
        CsvFlatFile.__init__(self, file, structure)

    def get_reception_by_id(self, id):
        return self.parse_groups()[id]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check a csv file structure')
    parser.add_argument('csv_files', metavar='FILES', nargs='+',
                        help='Files to be checked')
    args = parser.parse_args()
    print(args)
    # print(dir(test_lib))
    # f = getattr(test_lib,'check_dates')
    # print([method_name for method_name in dir(test_lib) if callable(getattr(test_lib, method_name))])
    #file = open("C:\\Users\\menkonda\\Downloads\\IMP_REC_2018_07_06_10_30_43_762.csv", "r", encoding="utf-8")
    # file = open("C:\\Users\\menkonda\\Downloads\\IMP_REC_2018_07_23_10_30_36_642.csv", "r", encoding="utf-8")
    #s = get_struct_from_pattern(config.CONFIG, "C:\\Users\\menkonda\\Downloads\\IMP_REC_2018_07_06_10_30_43_762.csv")
    # pass
    # a = ImpRecFlatFile(file, config.CONFIG)
    # res = a.run_defined_tests()

    # print(res)

