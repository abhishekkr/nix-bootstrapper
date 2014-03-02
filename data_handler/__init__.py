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
Datahandler managing required data provider and parser.
"""

import logging
from common import agent_logger

from parser.json_parser import JsonParser
from provider.metadata_service import MetadataService
from provider.local_file import LocalFile


class DataHandler:
    """
    To handle fetching data from given source and parsing it to required form.
    """

    def __init__(self, parser="json", provider="local-file"):
        try:
            if parser == "json":
                _parser = JsonParser()
            else:
                raise

            if provider == "metadata-service":
                self._get_value_for = MetadataService(parser=_parser).get_value_for

            elif provider == "local-file":
                self._get_value_for = LocalFile(parser=_parser).get_value_for

            else:
                raise

            agent_logger.log(logging.info,
                "DataHandler registered. Parser: %s, Provider: %s" %
                (parser, provider))

        except Exception, e:
            agent_logger.log(logging.error,
                "DataHandler register error, Parser: %s, Provider: %s.\n%s" %
                (parser, provider, e.message))

    def _cache_data(self, key, value=None):
        """ [WIP] YET FAKE
        Cache config data state for later comparison and
        only configure on difference with current cached config.
        """
        agent_logger.log(logging.info,
                         "[TBD] Caching data need to implemented.")
        return None

    def get_value_for(self, key):
        """
        Fetch value from provider, cache and return if it's new
        else return None to indicate no action required.
        """
        try:
            value = self._get_value_for(key)
            cached_value = self._cache_data(key)
            if value == cached_value:
                return None
            self._cache_data(key, value)
            return value

        except Exception, e:
            agent_logger.log(logging.error, "Exception in value for %s: %s" %
                             (key, e.message))
            return None
