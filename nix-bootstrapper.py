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

import sys

from commands import command_handler
import data_handler


if __name__ == "__main__":
    # need to make DataHandler pass custom parser/provider from some config
    _data_handler = data_handler.DataHandler()
    if len(sys.argv) == 1:
        command_handler.run_command("password", _data_handler.get_value_for)
    else:
        for _cmd in sys.argv[2:]:
            command_handler.run_command(_cmd, _data_handler.get_value_for)

