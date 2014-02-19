# ./commands

import commands

from nose.tools import assert_equal


class TestCommands(object):
    @classmethod
    def setup_class(klass):
        """This method is run once for each class before any tests are run"""
        @commands.command_add("is_true")
        def is_true(bool):
            if bool == True:
                return True
            return False

        @commands.command_add("is_false", {"foo": "bar"})
        def is_not_true(bool):
            return not is_true(bool)

        klass.istrue = staticmethod(is_true)
        klass.isfalse = staticmethod(is_not_true)

    @classmethod
    def teardown_class(klass):
        """This method is run once for each class _after_ all tests are run"""

    def setUp(self):
        """This method is run once before _each_ test method is executed"""

    def teardown(self):
        """This method is run once after _each_ test method is executed"""

    def test_init(self):
        assert_equal(isinstance(commands.cmd_list, dict), True)

    def test_command_add(self):
        cmd_list = commands.cmd_list
        assert_equal(cmd_list.has_key("istrue"), False)

        assert_equal(cmd_list["is_true"]["func"](True), self.istrue(True))
        assert_equal(cmd_list["is_true"]["config_key"], None)

        assert_equal(cmd_list["is_false"]["func"](True), self.isfalse(True))
        assert_equal(cmd_list["is_false"]["config_key"], {"foo": "bar"})

    def test__dict_value_or_none(self):
        _dict = {"existing_key": "existing_value", "foo": "nosey-test"}

        _call1_result = commands._dict_value_or_none(_dict, "existing_key")
        _call1_expected_result = _dict["existing_key"]

        _call2_result = commands._dict_value_or_none(_dict, "non_existing_key")
        _call2_expected_result = None

        assert_equal(_call1_result, _call1_expected_result)
        assert_equal(_call2_result, _call2_expected_result)

    def test_run(self):
        commands.datahandler.DataHandler = FakeDataHandler
        run = commands.run
        assert_equal(run("is_true"), True)
        assert_equal(run("is_false"), False)
        assert_equal(run("no_cmd"), None)
        pass


class FakeDataHandler(object):
    def __init__(self, parser, provider):
        pass

    def get_value_for(self, key):
        return True
