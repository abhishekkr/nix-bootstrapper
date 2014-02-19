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

import logging
from common import agent_logger


cmd_list = {}


def command_add(cmd_name, data_keys=[]):
    def wrap(_func):
        agent_logger.log(logging.error, str(data_keys))
        if cmd_name in cmd_list.keys():
            agent_logger.log(logging.error,
                         "%s already exists in feature list. Duplicacy." %
                             cmd_name)

        else:
            _data_keys = data_keys
            if isinstance(_data_keys, str):
                _data_keys = _data_keys.split()
            with open("/tmp/pylog", "a") as fyl:
                fyl.write(repr(_data_keys))

            cmd_list[cmd_name] = {"func": _func,
                                  "data_keys": _data_keys}

            agent_logger.log(logging.info,
                             "%s added to feature list with keys: %s." %
                             (cmd_name, _data_keys))

        return _func
    return wrap


def _dict_value_or_none(dictionary, key):
    if isinstance(dictionary, dict):
        if dictionary.has_key(key):
            return dictionary[key]
    return None


def run(cmd, get_value_for):
    try:
        data_keys = cmd_list[cmd]["data_keys"]
        data_values = {}
        for _data_key in data_keys:
            data_values[_data_key] = get_value_for(_data_key)
        agent_logger.log(logging.info, ">>>> %s" % repr(data_keys))
        agent_logger.log(logging.info, ">>>> %s" % repr(data_values))

        config_result = cmd_list[cmd]["func"](data_values)

        agent_logger.log(logging.info, "Running '%s'" % cmd,
                         data=data_values, result=config_result)
        return config_result

    except Exception, e:
        agent_logger.log(logging.error, e.message)
        return None
