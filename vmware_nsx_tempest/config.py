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
    cfg.StrOpt('device_1vlan',
                default={},
                help=" Define single VLAN device."
                     " required attribute is interface_names."
                     " name=l2gw-falcon-1,interface_names=dvportgroup-14425|1151"),
    cfg.StrOpt('device_trunkvlan',
                default={},
                help=" Define trunk VLAN device."
                     " required attribute is interface_names."
                     " nname=l2gw-falcon-x,interface_names=dvportgroup-14429|3880#3381#3382#3383#3384#3385"),
]
