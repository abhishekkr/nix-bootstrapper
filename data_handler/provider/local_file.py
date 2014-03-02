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
[WIP] Supposed to provide config values from a local file.
"""

import os


class LocalFile:
    """
    Local file communication plugin
    """

    def __init__(self, parser, **kwargs):
        self.parse = parser.parse
        self.filepath = kwargs["filepath"]

    def _get_value_for(self, key):
        with open(self.filepath, "r") as fyl:
            key_val = self.parse(fyl.read())
        return key_val[key]

    def get_value_for(self, key):
        """ Check if file exists and get value of desired key. """
        try:
            if not os.path.exists(self.filepath):
                raise
            return self._get_value_for(key)

        except:
            return ""
