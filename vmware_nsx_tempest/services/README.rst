This folder contains services for managing NSX-t, NSX-v and
neutron sub-services not yet migrating to tempest-lib. 

Services provided:

nsxv_client.py which it has API ops on the following NSX-v components
    - Logical switch (Tenant network)
    - Edge (Service edge, DHCP edge, and VDR edge)
    - DFW firewall rules (Security group)
    - SpoofGuard

l2_gateway_client.py



lbv1_client.py



