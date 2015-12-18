from oslo_config import cfg
from tempest import config

scenario_group = config.scenario_group

ScenarioGroup = [
    cfg.FloatOpt('waitfor_disassoc',
                 default=15.0,
                 help="Waitfor seconds after disassociation."),
    cfg.FloatOpt('waitfor_assoc',
                 default=5.0,
                 help="Waitfor seconds after association."),
    cfg.FloatOpt('waitfor_connectivity',
                 default=120.0,
                 help="Waitfor seconds to become connected."),
    cfg.ListOpt('outside_world_servers',
                default=["8.8.8.8", "8.8.4.4"],
                help="List of servers reside outside of openstack env."
                     " which is used to test default gateway behavior"
                     " when VMs are under logical routers,"
                     " & DNS are local to provider's settings."),
    cfg.DictOpt('flat_alloc_pool_dict',
                default={},
                help=" Define flat network ip range."
                     " required attributes are gateway, start, end"
                     " and cidr. Example value: gateway:10.1.1.253,"
                     " start:10.1.1.30,end:10.1.1.49,cidr=10.1.1.0/24"),
]

network_group = config.network_group

NetworkGroup = [
    cfg.StrOpt('l2gw_switch',
               default='',
               help="Distributed Virtual Portgroup to create VLAN port."),
    cfg.DictOpt('l2gw_switch_dict',
                default={},
                help="dict version of l2gw_switch:"
                     "device_name:,interfaces:,segmentation_id:,"),
]

nsxv_group = cfg.OptGroup(name='nsxv',
                          title="NSX-v Configuration Options")

NSXvGroup = [
    cfg.StrOpt('manager_uri',
               default='https://10.0.0.10',
               help="NSX-v manager ip address"),
    cfg.StrOpt('user',
               default='admin',
               help="NSX-v manager username"),
    cfg.StrOpt('password',
               default='default',
               help="NSX-v manager password"),
    cfg.StrOpt('vdn_scope_id',
               default='vdnscope-1',
               help="NSX-v vdn scope id"),
    cfg.FloatOpt('waitfor_disassoc',
                 default=15.0,
                 help="Waitfor seconds after disassociation."),
    cfg.FloatOpt('waitfor_assoc',
                 default=5.0,
                 help="Waitfor seconds after association."),
    cfg.FloatOpt('waitfor_connectivity',
                 default=120.0,
                 help="Waitfor seconds to become connected."),
    cfg.DictOpt('flat_alloc_pool_dict',
                default={},
                help=" Define flat network ip range."
                     " required attributes are gateway, start, end"
                     " and cidr. Example value: gateway:10.1.1.253,"
                     " start:10.1.1.30,end:10.1.1.49,cidr=10.1.1.0/24"),
    cfg.StrOpt('vlan_physical_network',
               default='',
               help="physval_network to create vlan."),
    cfg.IntOpt('provider_vlan_id',
               default=888,
               help="The default vlan_id for admin vlan."),
]


l2gw_group = cfg.OptGroup(name='l2gw',
                          title="l2-gateway Configuration Options")

L2gwGroup = [
    cfg.StrOpt('device_one_vlan',
                default="",
                help="l2g2 device with one VLAN"
                     " l2gw-1::dvportgroup-14420|3845"),
    cfg.StrOpt('device_multiple_vlans',
                default="",
                help="l2gw device with multiple VLANs"
                     " l2gw-falcon-x::dvportgroup-14429|3880#3381#3382#3383#3384#3385"),
    cfg.StrOpt('multiple_interfaces_multiple_vlans',
                default="",
                help="l2g2 multiple devices, each interface has multiple VLANs"
                     " l2gw-m-ifs::dvportgroup-14420|3845#3846;dvportgroup-15530|3900"),
]
