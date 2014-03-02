# ./commands/command_handler

from commands import command_handler

from nose.tools import assert_equal


class TestCommandHandler(object):

    def test_run_command(self):
        command_handler.commands.cmd_list = { "foo1": lambda x: not x }
        command_handler.commands.run = lambda func: command_handler.commands.cmd_list[func](None)

        result1 = command_handler.run_command("foo1")
        expected_result1 = True

        result2 = command_handler.run_command("no-foo2")
        expected_result2 = None

        assert_equal(result1, expected_result1)
        assert_equal(result2, expected_result2)
