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

from vmware_nsx_tempest.services import network_client_base as base


class L2GatewayClient(base.BaseNetworkClient):
    resource = 'l2_gateway'
    resource_plural = 'l2_gateways'
    path = 'l2-gateways'
    resource_base_path = '/%s' % path
    resource_object_path = '/%s/%%s' % path

    def create_l2_gateway(self, **kwargs):
        uri = self.resource_base_path
        post_data = {self.resource: kwargs}
        return self.create_resource(uri, post_data)

    def update_l2_gateway(self, l2_gateway_id, **kwargs):
        uri = self.resource_object_path % l2_gateway_id
        post_data = {self.resource: kwargs}
        return self.update_resource(uri, post_data)

    def show_l2_gateway(self, l2_gateway_id, **fields):
        uri = self.resource_object_path % l2_gateway_id
        return self.show_resource(uri, **fields)

    def delete_l2_gateway(self, l2_gateway_id):
        uri = self.resource_object_path % l2_gateway_id
        return self.delete_resource(uri)

    def list_l2_gateways(self, **filters):
        uri = self.resource_base_path
        return self.list_resources(uri, **filters)


def create_l2_gateway_client(auth_provider, catalog_type, region,
                             endpoint_type, build_interval, build_timeout,
                             **kwargs):
    params = base.default_params.copy()
    params.update(kwargs)
    l2_gateway_client = L2GatewayClient(auth_provider, catalog_type, region,
                                        endpoint_type, build_interval,
                                        build_timeout, **params)
    return l2_gateway_client
