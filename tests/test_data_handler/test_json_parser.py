# ./commands

from data_handler.parser import json_parser

from nose.tools import assert_equal


class TestJsonParser(object):

    def test_parse(self):
        import json
        expected_result = {"firstname": "anon", "lastname": "ymous"}
        dummy_json = json.dumps(expected_result)
        result = json_parser.JsonParser().parse(dummy_json)
        assert_equal(result,expected_result)
