# Copyright 2015 OpenStack Foundation
# Copyright 2015 VMware Inc
# All Rights Reserved.
#
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

from tempest_lib.common.utils import data_utils
from tempest_lib import decorators

from tempest.api.network import base
from tempest import test
from tempest import config

from vmware_nsx_tempest.services import l2_gateway_client as L2GW
from vmware_nsx_tempest.services import l2_gateway_connection_client as L2GWC

CONF = config.CONF
_l2gw_1vlan = CONF.l2gw.device_1vlan
_l2gw_2vlan2 = CONF.l2gw.device_2vlans
_l2gw_trunkvlan = CONF.l2gw.device_trunkvlan


class L2GatewayTest(base.BaseAdminNetworkTest):

    credentials = ['primary', 'admin']

    @classmethod
    def skip_checks(cls):
        super(L2GatewayTest, cls).skip_checks()
        if not test.is_extension_enabled('l2-gateway', 'network'):
            msg = "l2-gateway extension not enabled."
            raise cls.skipException(msg)
        if not test.is_extension_enabled('l2-gateway-connection', 'network'):
            msg = "l2-gateway-connection extension is not enabled"
            raise cls.skipException(msg)

    @classmethod
    def setup_clients(cls):
        super(L2GatewayTest, cls).setup_clients()
        l2gw_mgr = cls.os_adm
        init_params = cls.manager.default_params_with_timeout_values.copy()
        init_params['auth_provider'] = l2gw_mgr.auth_provider
        init_params['service'] = l2gw_mgr.networks_client.service
        init_params['region'] = l2gw_mgr.networks_client.region
        init_params['endpoint_type'] = l2gw_mgr.networks_client.endpoint_type
        cls.l2gw_client = L2GW.L2GatewayClient(**init_params)
        cls.l2gwc_client = L2GWC.L2GatewayConnectionClient(**init_params)

    @classmethod
    def resource_setup(cls):
        super(L2GatewayTest, cls).resource_setup()

    @classmethod
    def resource_cleanup(cls):
        """
        """
        pass

    @test.idempotent_id('8b45a9a5-468b-4317-983d-7cceda367074')
    def test_create_update_delete_1device_1vlan_type1(self):
        skip_if_notdefined(_l2gw_1vlan, "device_1vlan")
        pass

    @test.idempotent_id('af57cf56-a169-4d88-b32e-7f49365ce407')
    def test_create_update_delete_1device_1vlan_type2(self):
        skip_if_notdefined(_l2gw_1vlan, "device_1vlan")
        pass


def skip_if_notdefined(req_attr, attr_title):
    if not req_attr:
        msg = "l2gw config attr %s is not defined" % (attr_title)
        self.skipException(msg)
