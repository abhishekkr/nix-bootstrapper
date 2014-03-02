# ./data_handler

import data_handler

import tests.fakers

from nose.tools import assert_equal
from nose.tools import assert_raises
import mox

from nose.tools import nottest


class TestDataHandler(object):
    def setUp(self):
        data_handler.JsonParser = tests.fakers.FakeParser
        data_handler.MetadataService = tests.fakers.FakeProvider
        data_handler.LocalFile = tests.fakers.FakeProvider
        self._data_handler = data_handler.DataHandler()
        self._data_handler_meta = data_handler.DataHandler(
                                                provider="metadata-service")

    def test_init(self):
        assert_raises(data_handler.DataHandler(provider="foo"))
        assert_raises(data_handler.DataHandler(parser="bar"))

    @nottest
    def test__cache_data(self):
        assert(False) #TBD

    def test_get_value_for(self):
        result = self._data_handler.get_value_for("alpha")
        expected_result = (True, "alpha")
        assert_equal(result, expected_result)

        result = self._data_handler_meta.get_value_for("beta")
        expected_result = (True, "beta")
        assert_equal(result, expected_result)
