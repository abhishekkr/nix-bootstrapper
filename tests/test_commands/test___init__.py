# ./commands

import commands

from nose.tools import assert_equal


class TestCommands(object):
    @classmethod
    def setup_class(klass):
        """This method is run once for each class before any tests are run"""
        @commands.command_add("is_true", "foo")
        def is_true(data_values):
            if data_values["foo"] == True:
                return True
            return False

        @commands.command_add("is_false", ["foo", "bar"])
        def is_not_true(data_values):
            return not is_true({"foo": data_values["bar"]})

        @commands.command_add("blaah")
        def blaah(data_values):
            """Just Blaah! Can't use data_values cuz no data_keys. """
            return "blaah"

        klass.istrue = staticmethod(is_true)
        klass.isfalse = staticmethod(is_not_true)
        klass.blaah = staticmethod(blaah)

    def test_init(self):
        assert_equal(isinstance(commands.cmd_list, dict), True)

    def test_command_add(self):
        cmd_list = commands.cmd_list
        assert_equal(cmd_list.has_key("istrue"), False)

        assert_equal(cmd_list["is_true"]["func"]({"foo": True}),
                     self.istrue({"foo": True}))
        assert_equal(cmd_list["is_true"]["data_keys"], ["foo"])

        assert_equal(cmd_list["is_false"]["func"]({"bar": True}),
                     self.isfalse({"bar": True}))
        assert_equal(cmd_list["is_false"]["data_keys"], ["foo", "bar"])

        assert_equal(cmd_list["blaah"]["func"]({}), self.blaah({}))
        assert_equal(cmd_list["blaah"]["data_keys"], [])

    def test__dict_value_or_none(self):
        _dict = {"existing_key": "existing_value", "foo": "nosey-test"}

        _call1_result = commands._dict_value_or_none(_dict, "existing_key")
        _call1_expected_result = _dict["existing_key"]

        _call2_result = commands._dict_value_or_none(_dict, "non_existing_key")
        _call2_expected_result = None

        assert_equal(_call1_result, _call1_expected_result)
        assert_equal(_call2_result, _call2_expected_result)

    def test_run(self):
        run = commands.run
        fakedata = FakeDataHandler("parser", "provider")
        assert_equal(run("is_true", fakedata.get_value_for), True)
        assert_equal(run("is_false", fakedata.get_value_for), False)
        assert_equal(run("blaah", fakedata.get_value_for), "blaah")
        assert_equal(run("no_cmd", fakedata.get_value_for), None)


class FakeDataHandler(object):
    def __init__(self, parser, provider):
        pass

    def get_value_for(self, key):
        return True
