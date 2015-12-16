#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import time

from tempest_lib import exceptions as lib_exc

from tempest import exceptions
from tempest.services.network.json import base


# netowrk/json/base.py does not include thoese method in network_client
class BaseNetworkClient(base.BaseNetworkClient):
    def __init__(self, auth_provider, service, region,
                 endpoint_type=None, build_interval=None, build_timeout=None,
                 disable_ssl_certificate_validation=None, ca_certs=None,
                 trace_requests=None, **kwargs):
        dsca = disable_ssl_certificate_validation
        super(base.BaseNetworkClient, self).__init__(
            auth_provider, service, region,
            endpoint_type=endpoint_type,
            build_interval=build_interval,
            build_timeout=build_timeout,
            disable_ssl_certificate_validation=dsca,
            ca_certs=ca_certs,
            trace_requests=trace_requests)

    def wait_for_resource_deletion(self, resource_type, id, client=None):
        """Waits for a resource to be deleted."""
        start_time = int(time.time())
        while True:
            if self.is_resource_deleted(resource_type, id, client=client):
                return
            if int(time.time()) - start_time >= self.build_timeout:
                raise exceptions.TimeoutException
            time.sleep(self.build_interval)

    def is_resource_deleted(self, resource_type, id, client=None):
        if client is None:
            client = self
        method = 'show_' + resource_type
        try:
            getattr(client, method)(id)
        except AttributeError:
            raise Exception("Unknown resource type %s " % resource_type)
        except lib_exc.NotFound:
            return True
        return False


default_params = {
    'disable_ssl_certificate_validation': True,
    'ca_certs': None,
    'trace_requests': ''}
default_params_2 = {
    'catalog_type': 'network',
    'region': 'nova',
    'endpoint_type': 'publicURL',
    'build_timeout': 300,
    'build_interval': 1}
