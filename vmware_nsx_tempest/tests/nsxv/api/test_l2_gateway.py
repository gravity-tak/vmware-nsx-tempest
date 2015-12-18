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

from vmware_nsx_tempest.services import base_l2gw
from vmware_nsx_tempest.services import l2_gateway_client as L2GW

CONF = config.CONF
L2GW_RID = 'l2_gateway'
L2GW_RIDs = 'l2_gateways'


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
        # if CONF attr device_on_vlan not defined, SKIP entire test suite
        dev_profile = cls.getattr_or_skip_test("device_one_vlan")

    @classmethod
    def getattr_or_skip_test(cls, l2gw_attr_name):
        attr_value = getattr(CONF.l2gw, l2gw_attr_name, None)
        if attr_value:
            return attr_value
        msg = "CONF session:l2gw attr:%s is not defined." % (l2gw_attr_name)
        raise cls.skipException(msg)

    @classmethod
    def setup_clients(cls):
        super(L2GatewayTest, cls).setup_clients()
        cls.l2gw_created = {}
        l2gw_mgr = cls.os_adm
        init_params = cls.manager.default_params_with_timeout_values.copy()
        init_params['auth_provider'] = l2gw_mgr.auth_provider
        init_params['service'] = l2gw_mgr.networks_client.service
        init_params['region'] = l2gw_mgr.networks_client.region
        init_params['endpoint_type'] = l2gw_mgr.networks_client.endpoint_type
        cls.l2gw_client = L2GW.L2GatewayClient(**init_params)
        cls.l2gw_list_0 = cls.l2gw_client.list_l2_gateways()[L2GW_RIDs]

    @classmethod
    def resource_setup(cls):
        super(L2GatewayTest, cls).resource_setup()

    @classmethod
    def resource_cleanup(cls):
        """
        """
        for _id in cls.l2gw_created.keys():
            try:
                cls.l2gw_client.delete_l2_gateway(_id)
            except Exception:
                # log it please
                pass

    def _csuld_single_device_interface_vlan(self, _name, _devices):
        _vlan_id_list = _devices['devices'][0]['interfaces'][0].get(
            'segmentation_id', None)
        _res_new = self.l2gw_client.create_l2_gateway(
            name=_name, **_devices)[L2GW_RID]
        self.l2gw_created[_res_new['id']] = _res_new
        _res_show = self.l2gw_client.show_l2_gateway(_res_new['id'])[L2GW_RID]
        _name2 = _name + "-day2"
        _res_upd = self.l2gw_client.update_l2_gateway(
            _res_new['id'], name=_name2)[L2GW_RID]
        _res_lst = self.l2gw_client.list_l2_gateways(name=_name2)[L2GW_RIDs]
        _res_del = self.l2gw_client.delete_l2_gateway(_res_new['id'])
        _res_lst = self.l2gw_client.list_l2_gateways(name=_name2)[L2GW_RIDs]
        self.l2gw_created.pop(_res_new['id'])

    @test.idempotent_id('8b45a9a5-468b-4317-983d-7cceda367074')
    def test_csuld_single_device_interface_vlan_type1(self):
        """This method don't have vlan in the device profile when creating l2gw"""
        dev_profile = self.getattr_or_skip_test("device_one_vlan")
        _name = data_utils.rand_name('l2gw-1v1')
        _devices = base_l2gw.get_l2gw_body(dev_profile)
        _vlan_id_list = _devices['devices'][0]['interfaces'][0].pop(
            'segmentation_id', None)
        self._csuld_single_device_interface_vlan(_name, _devices)

    @test.idempotent_id('af57cf56-a169-4d88-b32e-7f49365ce407')
    def test_csuld_single_device_interface_vlan_type2(self):
        """This method have vlan in the device profile when creating l2gw"""
        dev_profile = self.getattr_or_skip_test("device_one_vlan")
        _name = data_utils.rand_name('l2gw-1v2')
        _devices = base_l2gw.get_l2gw_body(dev_profile)
        self._csuld_single_device_interface_vlan(_name, _devices)

    @test.idempotent_id('cb59145e-3d2b-46b7-8f7b-f30f794a4d51')
    def test_csuld_single_device_interface_mvlan_type2(self):
        dev_profile = self.getattr_or_skip_test("device_multiple_vlans")
        _name = data_utils.rand_name('l2gw-2v1')
        _devices = base_l2gw.get_l2gw_body(dev_profile)
        self._csuld_single_device_interface_vlan(_name, _devices)

    @test.idempotent_id('5522bdfe-ebe8-4eea-81b4-f4075bb608cf')
    def test_csuld_single_device_minterface_mvlan_type1(self):
        # NSX-v does not support multiple interfaces
        dev_profile = self.getattr_or_skip_test(
            "multiple_interfaces_multiple_vlans")
        _name = data_utils.rand_name('l2gw-m2v1')
        _devices = base_l2gw.get_l2gw_body(dev_profile)
        self._csuld_single_device_interface_vlan(_name, _devices)

    @test.idempotent_id('5bec26e0-855f-4537-b31b-31663a820ddb')
    def test_csuld_single_device_minterface_mvlan_type2(self):
        dev_profile = self.getattr_or_skip_test(
            "multiple_interfaces_multiple_vlans")
        _name = data_utils.rand_name('l2gw-m2v2')
        _devices = base_l2gw.get_l2gw_body(dev_profile)
        self._csuld_single_device_interface_vlan(_name, _devices)