from testlib.common import TestCaseResult, TestCaseStepResult
import os.path


def imp_rec_check_required(flat_file_object):
    """
    Check the required fields according to file
    :param flat_file_object: the CsvFlatFile object containing the content of the flat file and file structure
    :return: a TesCaseResult object with all the lines and position containing missing fields
    """
    result = TestCaseResult()
    for idx, row in enumerate(flat_file_object.rows):
        row_type = row[flat_file_object.structure.type_pos - 1]
        row_struct = [struct for struct in flat_file_object.structure.row_structures if row_type == struct.type][0]
        for pos in range(0, row_struct.length):
            if (pos + 1) in row_struct.optional_fields:
                continue

            # In Specification "Article Champ vide pour les lignes de type C lorsque la source est N21"
            if row_type == "L" and row[1] == "C" and pos == 3:
                continue

            if row[pos] == "":
                step_result = TestCaseStepResult(idx + 1, False, 'REQUIRED_FIELD', "Missing required field at position"
                                                 + str(pos + 1), os.path.basename(flat_file_object.filename))
                result.steps.append(step_result)
    return result
