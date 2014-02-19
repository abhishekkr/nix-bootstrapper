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

import datahandler

import logging
from common import agent_logger


cmd_list = {}


def command_add(cmd_name, config_key=None):
    def wrap(_func):
        if cmd_name in cmd_list.keys():
            agent_logger.log(logging.error,
                         "%s couldn't be added to feature list." % cmd_name)
        else:
            agent_logger.log(logging.info,
                         "%s added to feature list." % cmd_name)
            cmd_list[cmd_name] = {"func": _func,
                                  "config_key": config_key}

        return _func
    return wrap


def _dict_value_or_none(dictionary, key):
    if isinstance(dictionary, dict):
        if key in dictionary.keys():
            return dictionary[key]
    return None


def run(cmd):
    try:
        config_keys = cmd_list[cmd]["config_key"]
        parser, provider, data_keys = (
            _dict_value_or_none(config_keys, "parser"),
            _dict_value_or_none(config_keys, "provider"),
            _dict_value_or_none(config_keys, "data_keys")
        )
        _datahandler = datahandler.DataHandler(parser, provider)
        data_values = {}
        if isinstance(data_keys, str):
            data_values[data_keys] = _datahandler.get_value_for(data_keys)
        elif isinstance(data_keys, list):
            for _data_key in data_keys:
                data_values[_data_key] = _datahandler.get_value_for(_data_key)

        config_result = cmd_list[cmd]["func"](data)

        agent_logger.log(logging.info, "Running '%s'" % cmd,
                         data=data, result=config_result)
        return config_result

    except Exception, e:
        agent_logger.log(logging.error, e.message)
        return None
