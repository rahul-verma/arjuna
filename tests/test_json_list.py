import unittest
from arjuna.tpi.parser.json import JsonList


class JsonListTest(unittest.TestCase):
    
    
    def test_empty_JSONList_construct01(self):
        try :
            json_list = JsonList()
        except TypeError as te:
            pass
        else :
            raise AssertionError("JsonList shouldn't allow with default construct")

    def test_empty_JSONList_construct02(self):
        json_list = JsonList([])
        json_list.assert_empty(msg = "Should be empty")

    def test_non_empty_JSONList(self):
        json_list = JsonList([1])
        json_list.assert_not_empty(msg = "Should not be empty")

    def test_empty_JSONList(self):
        json_list = JsonList([])
        try:
            json_list.assert_not_empty(msg = "Should not be empty")
        except AssertionError as ae:
            pass
        else:
            raise AssertionError("Assert non empty Json List is not working as expected")

    def test_JSONList_size_01(self):
        exp_list = [1,2,34]
        json_list = JsonList(exp_list)
        json_list.assert_size(len(exp_list), msg = "Should match with expected size")

    def test_JSONList_size_02(self):
        exp_list = [1,2,34]
        json_list = JsonList(exp_list)
        try:
            json_list.assert_size(len(exp_list)-1, msg = "Should match with expected size")
        except AssertionError as ae:
            pass
        else:
            raise AssertionError("assert_size Json List is not working as expected")

    def test_JSONList_size_03(self):
        exp_list = [1,2,34]
        json_list = JsonList(exp_list)
        try:
            json_list.assert_size(len(exp_list)+1,  msg = "Should match with expected size")
        except AssertionError as ae:
            pass
        else:
            raise AssertionError("assert_size Json List is not working as expected")

    def test_JSONList_size_04(self):
        exp_list = [1,2,34]
        json_list = JsonList(exp_list)
        try:
            json_list.assert_size(0,  msg = "Should match with expected size")
        except AssertionError as ae:
            pass
        else:
            raise AssertionError("assert_size Json List is not working as expected")

    def test_JSONList_size_05(self):
        exp_list = [1,2,34]
        json_list = JsonList(exp_list)
        try:
            json_list.assert_size(-1,  msg = "Should match with expected size")
        except AssertionError as ae:
            pass
        else:
            raise AssertionError("assert_size Json List is not working as expected")

    def test_JSONList_size_06(self):
        exp_list = [1,2,34]
        json_list = JsonList(exp_list)
        try:
            json_list.assert_size(None,  msg = "Should match with expected size")
        except AssertionError as ae:
            pass
        else:
            raise AssertionError("assert_size Json List is not working as expected")

    def test_JSONList_min_size_01(self):
        exp_list = [1]
        json_list = JsonList(exp_list)
        json_list.assert_min_size(len(exp_list)-1,  msg = "Should match with expected min size")

    def test_JSONList_min_size_02(self):
        exp_list = [1]*10
        json_list = JsonList(exp_list)
        json_list.assert_min_size(len(exp_list)-5,  msg = "Should match with expected min size")

    def test_JSONList_min_size_03(self):
        exp_list = [1]*10
        json_list = JsonList(exp_list)
        try:
            json_list.assert_min_size(len(exp_list)+5,  msg = "Should match with expected min size")
        except AssertionError as ae:
            pass
        else:
            raise AssertionError("assert_min_size Json List is not working as expected")

    def test_JSONList_min_size_04(self):
        exp_list = [1]*10
        json_list = JsonList(exp_list)
        try:
            json_list.assert_min_size("2",  msg = "Should match with expected min size")
        except TypeError as ae:
            pass
        else:
            raise AssertionError("assert_min_size Json List is not working as expected")

    def test_JSONList_max_size_01(self):
        exp_list = [1]*10
        json_list = JsonList(exp_list)
        json_list.assert_max_size(len(exp_list), msg = "Should match with expected max size")

    def test_JSONList_max_size_02(self):
        exp_list = [1]*10
        json_list = JsonList(exp_list)
        try :
            json_list.assert_max_size(-1, msg = "Should match with expected max size")
        except TypeError as te:
            pass
        else:
            raise AssertionError("assert_max_size Json List is not working as expected")

    def test_JSONList_max_size_03(self):
        exp_list = []
        json_list = JsonList(exp_list)
        json_list.assert_max_size(0,   msg = "Should match with expected max size")

    def test_JSONList_max_size_04(self):
        exp_list = [1]*10
        json_list = JsonList(exp_list)
        try:
            json_list.assert_max_size("2",   msg = "Should match with expected max size")
        except TypeError as ae:
            pass
        else:
            raise AssertionError("assert_max_size Json List is not working as expected")

    def test_JSONList_max_size_05(self):
            exp_list = [1]*10
            json_list = JsonList(exp_list)
            json_list.assert_max_size(10.5,   msg = "Should match with expected max size")
            # try:
            #     json_list.assert_max_size(len(exp_list)+5,   msg = "Should match with expected max size")
            # except AssertionError as ae:
            #     raise ae
            # else:
            #     raise AssertionError("assert_max_size Json List is not working as expected")

    def test_JSONList_size_range_01(self):
        exp_list = [1]*10
        json_list = JsonList(exp_list)
        json_list.assert_size_range(len(exp_list)-5, len(exp_list),   msg = "Should be within the range")



if __name__ == "__main__":
    unittest.main()