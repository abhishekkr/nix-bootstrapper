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

import commands
import command_list

import logging
from common import agent_logger


def run_command(cmd_name):
    try:
        if not cmd_name in commands.cmd_list.keys():
            raise
        return commands.run(cmd_name)

    except:
        agent_logger.log(logging.error,
                     "%s is not a registered command to run." % cmd_name)
        return None
