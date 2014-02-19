# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
#  Copyright (c) 2011 Openstack, LLC.
#  All Rights Reserved.
#
#     Licensed under the Apache License, Version 2.0 (the "License"); you may
#     not use this file except in compliance with the License. You may obtain
#     a copy of the License at
#
#          http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#     WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#     License for the specific language governing permissions and limitations
#     under the License.
#

"""
misc commands plugin
"""

import commands


@commands.command_add('features')
def features_cmd(data_values):
    """ To display all plugged-in feature commands available. """
    cmd_list = commands.cmd_list
    _commands_doc = map(
                    (lambda x: "%s: %s\n\twith %s config keys" % (
                        x,
                        cmd_list[x]["func"].__doc__,
                        cmd_list[x]["config_key"])),
                    cmd_list)
    _commands_doc = "\n".join(_commands_doc)
    return _commands_doc


@commands.command_add('version')
def version_cmd(data_values):
    """ To display version of current agent. """
    # Ignore the version arguments
    return "TBD"
