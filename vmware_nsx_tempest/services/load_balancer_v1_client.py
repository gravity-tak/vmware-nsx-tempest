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


default_params = {
    'disable_ssl_certificate_validation': True,
    'ca_certs': None,
    'trace_requests': ''}
POOL_RID = 'pools'
VIP_RID = 'vips'
HEALTHMONITOR_RID = 'health_monitors'
MEMBER_RID = 'members'


class LoadBalancerV1Client(base.BaseNetworkClient):

    def _list_lb(self, lb_resource, **filters):
        resource_name_s, resource_name_p = _g_resource_namelist(lb_resource)
        req_uri = '/lb/%s' % (resource_name_p)
        return self.list_resources(req_uri, **filters)

    def _show_lb(self, lb_resource, resource_id, **fields):
        resource_name_s, resource_name_p = _g_resource_namelist(lb_resource)
        req_uri = '/lb/%s/%s' % (resource_name_p, resource_id)
        return self.show_resource(req_uri, **fields)

    def _delete_lb(self, lb_resource, resource_id):
        resource_name_s, resource_name_p = _g_resource_namelist(lb_resource)
        req_uri = '/lb/%s/%s' % (resource_name_p, resource_id)
        return self.delete_resource(req_uri)

    def _create_lb(self, lb_resource, **kwargs):
        resource_name_s, resource_name_p = _g_resource_namelist(lb_resource)
        req_uri = '/lb/%s' % (resource_name_p)
        post_body = {resource_name_s: kwargs}
        return self.create_resource(req_uri, post_body)

    def _update_lb(self, lb_resource, resource_id, **kwargs):
        resource_name_s, resource_name_p = _g_resource_namelist(lb_resource)
        req_uri = '/lb/%s/%s' % (resource_name_p, resource_id)
        post_body = {resource_name_s: kwargs}
        return self.update_resource(req_uri, post_body)

    def show_agent_hosting_pool(self, pool_id):
        """Get loadbalancer agent hosting a pool."""
        req_uri = "/lb/pools/%s/loadbalancer-agent" % (pool_id)
        return self.show_resource(req_uri)

    def associate_health_monitor_with_pool(self, health_monitor_id, pool_id):
        """Create a mapping between a health monitor and a pool."""
        post_body = {'health_monitor': { 'id': health_monitor_id }}
        req_uri = '/lb/pools/%s/health_monitor' % (pool_id)
        return self.create_resource(req_uri, post_body)

    def create_health_monitor(self, **kwargs):
        """Create a health monitor."""
        create_kwargs = dict(
            type=kwargs.pop('type', 'TCP'),
            max_retries=kwargs.pop('nax_retries', 3),
            timeout=kwargs.pop('timeout', 1),
            delay=kwargs.pop('delay', 4),
        )
        create_kwargs.update(**kwargs)
        return self._create_lb(HEALTHMONITOR_RID, **create_kwargs)

    def delete_health_monitor(self, health_monitor_id):
        """Delete a given health monitor."""
        return self._delete_lb(HEALTHMONITOR_RID, health_monitor_id)

    def disassociate_health_monitor_with_pool(self, health_monitor_id, pool_id):
        """Remove a mapping from a health monitor to a pool."""
        req_uri = ('/lb/pools/%s/health_monitor/%s'
                   % (pool_id, health_monitory_id))
        return self.delete_resource(req_uri)

    def list_health_monitor(self):
        """List health monitors that belong to a given tenant."""
        return self._list_lb(HEALTHMONITOR_RID)

    def show_health_monitor(self, health_monitor_id):
        """Show information of a given health monitor."""
        return self._show_lb(HEALTHMONITOR_RID, health_monitor_id)

    def update_health_monitor(self, health_monitor_id,
                              show_then_update=True, **kwargs):
        """Update a given health monitor."""
        body = (self.lb_health_monitor_show(health_monitor_id)
                if show_then_update else {})
        body.update(**kwargs)
        return self._update_lb(HEALTHMONITOR_RID,
                               health_monitor_id, **body)

    # tempest create_member(self,protocol_port, pool, ip_version)
    # we use pool_id
    def create_member(self, protocol_port, pool_id,
                      ip_version=4, **kwargs):
        """Create a member."""
        create_kwargs = dict(
            protocol_port=protocol_port,
            pool_id=pool_id,
            # address=("fd00:abcd" if ip_version == 6 else "10.0.9.46"),
        )
        create_kwargs.update(**kwargs)
        return self._create_lb(MEMBER_RID, **create_kwargs)

    def delete_member(self, member_id):
        """Delete a given member."""
        return self._delete_lb(MEMBER_RID, member_id)

    def list_member(self):
        """List members that belong to a given tenant."""
        return self._list_lb(MEMBER_RID)

    def show_member(self, member_id):
        """Show information of a given member."""
        return self._show_lb(MEMBER_RID, member_id)

    def update_member(self, member_id,
                      show_then_update=True, **kwargs):
        """Update a given member."""
        body = (self.lb_member_show(member_id) if
                show_then_update else {})
        body.update(**kwargs)
        return self._update_lb(MEMBER_RID, member_id, **body)

    def create_pool(self, pool_name, lb_method, protocol, subnet_id,
                    **kwargs):
        """Create a pool."""
        lb_method = lb_method or 'ROUND_ROBIN'
        protocol = protocol or 'HTTP'
        create_kwargs = dict(
            name=pool_name, lb_method=lb_method,
            protocol=protocol, subnet_id=subnet_id,
        )
        create_kwargs.update(kwargs)
        return self._create_lb(POOL_RID, **create_kwargs)

    def delete_pool(self, pool_id):
        """Delete a given pool."""
        return self._delete_lb(POOL_RID, pool_id)

    def list_pool(self):
        """List pools that belong to a given tenant."""
        return self._list_lb(POOL_RID)

    def list_lb_pool_stats(self, pool_id):
        """Retrieve stats for a given pool."""
        req_uri = '/lb/pools/%s/stats' % (pool_id)
        return self.show_resource(req_uri)

    def list_pool_on_agent(self):
        """List the pools on a loadbalancer agent."""
        pass

    def show_pool(self, pool_id):
        """Show information of a given pool."""
        return self._show_lb(POOL_RID, pool_id)

    def update_pool(self, pool_id, show_then_update=True, **kwargs):
        """Update a given pool."""
        body = (self.lb_pool_show(pool_id) if
                show_then_update else {})
        body.update(**kwargs)
        return self._update_lb(POOL_RID, pool_id, **body)

    def create_vip(self, pool_id, **kwargs):
        """Create a vip."""
        create_kwargs = dict(
            pool_id=pool_id,
            protocol=kwargs.pop('protocol', 'HTTP'),
            protocol_port=kwargs.pop('protocol_port', 80),
            name=kwargs.pop('name', None),
            address=kwargs.pop('address', None),
        )
        for k in create_kwargs.keys():
            if create_kwargs[k] is None:
                create_kwargs.pop(k)
        create_kwargs.update(**kwargs)
        # subnet_id needed to create vip
        return self._create_lb(VIP_RID, **create_kwargs)

    def delete_vip(self, vip_id):
        """Delete a given vip."""
        return self._delete_lb(VIP_RID, vip_id)

    def list_vip(self):
        """List vips that belong to a given tenant."""
        return self._list_lb(VIP_RID)

    def show_vip(self, vip_id):
        """Show information of a given vip."""
        return self._show_lb(VIP_RID, vip_id)

    def update_vip(self, vip_id, show_then_update=True, **kwargs):
        """Update a given vip."""
        body = (self.lb_vip_show(vip_id) if
                show_then_update else {})
        body.update(**kwargs)
        return self._update_lb(VIP_RID, vip_id, **body)


def _g_resource_namelist(lb_resource):
    if lb_resource[-1] == 's':
        return (lb_resource[:-1], lb_resource)
    return (lb_resource, lb_resource + "s")


def create_lbv1_client(auth_provider, catalog_type, region,
                       endpoint_type, build_interval, build_timeout,
                       **kwargs):
    params = default_params.copy()
    params.update(kwargs)
    lbv1_client = LoadBalancerV1Client(auth_provider, catalog_type, region,
                                       endpoint_type, build_interval,
                                       build_timeout, **params)
    return lbv1_client


def destroy_tenant_lb(lbv1_client):
    for o in lbv1_client.list_member():
        lbv1_client.delete_member(o['id'])
    for o in lbv1_client.list_health_monitor():
        lbv1_client.delete_health_monitor(o['id'])
    for o in lbv1_client.list_vip():
        lbv1_client.delete_vip(o['id'])
    for o in lbv1_client.list_pool():
        lbv1_client.delete_pool(o['id'])
