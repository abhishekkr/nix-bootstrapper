# vim tabstop=4 shiftwidth=4 softtabstop=4
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
List of command modules to load
"""

import glob
#cmd_plugins = {}
#for f in glob.glob('cmd_plugins/*.py'):
    #fnam = f.split("/")[-1][:-3]
    #cmd_plugins[fnam] = __import__("cmd_plugins", fnam)

from command_plugins import misc, password
