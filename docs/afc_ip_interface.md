# module: afc_ip_interface

Description: This module is used to create and delete Switch Virtual Interface or IP Interface.

##### ARGUMENTS

```YAML
afc_ip:
    description: >
        IP address of the Aruba Fabric Composer.
    type: str
    required: true
afc_username:
    description:
    - User account having write permission on the Aruba Fabric Composer
    type: str
    required: false
afc_password:
    description:
    - Password of the user account
    type: str
    required: false
auth_token:
    description: >
        Auth token from the create session playbook.
    type: str
    required: false
vrf_name:
    description: >
        Name of the VRF in which IP Interface, ROP, loopback or SVI should be created or deleted from.
    type: str
    required: true
operation:
    description: >
        Operation to be performed with the IP Interface, ROP, loopback or SVI, create or delete.
    type: str
    required: true
ip_interface_data:
    description: >
        IP Interface data containing if_type, vlan, active_gateway, ipv4_primary_address, local_proxy_arp_enabled and the switches. The values vlan and the
        prefix_length need to be integers. Structure is provided in the example.
    type: dict
    required: true
```

##### EXAMPLES

```YAML
-   name: Create IP Interface using username and password
    arubanetworks.afc.afc_ip_interface:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        fabric_name: "Aruba-Fabric"
        vrf_name: "Aruba-VRF"
        operation: "create"
        ip_interface_data:
            vrf: "Aruba-VRF"
            enable: True
            local_proxy_arp_enabled: True
            name: "VLAN250"
            vlan: 250
            if_type: vlan
            ipv4_primary_address:
                address: "10.10.10.11-10.10.10.50"
                prefix_length: 24
            active_gateway:
                ipv4_address: "10.10.10.1"
                mac_address: "00:00:00:00:00:01"
            switches:
                - "10.10.10.7"
                - "10.10.10.8"
                - "10.10.10.9"

-   name: Create a ROP (Routed Only Port) using username and password
    arubanetworks.afc.afc_ip_interface:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        fabric_name: "Aruba-Fabric"
        vrf_name: "Aruba-VRF"
        operation: "create"
        ip_interface_data:
            vrf: "Aruba-VRF"
            enable: True
            local_proxy_arp_enabled: True
            name: "VLAN250"
            interface: 1/1/14
            if_type: routed
            ipv4_primary_address:
                address: "10.10.10.25"
                prefix_length: 24
            switches:
                - "10.10.10.7"

-   name: Create an SVI using username and password
    arubanetworks.afc.afc_ip_interface:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        fabric_name: "Aruba-Fabric"
        vrf_name: "Aruba-VRF"
        operation: "create"
        ip_interface_data:
            vrf: "Aruba-VRF"
            enable: True
            local_proxy_arp_enabled: True
            name: "VLAN250"
            vlan: 250
            if_type: vlan
            ipv4_primary_address:
                address: "10.10.10.11-10.10.10.50"
                prefix_length: 24
            active_gateway:
                ipv4_address: "10.10.10.1"
                mac_address: "00:00:00:00:00:01"
            switches:
                - "10.10.10.7"
                - "10.10.10.8"
                - "10.10.10.9"

-   name: Create a loopback interface using username and password
    arubanetworks.afc.afc_ip_interface:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        fabric_name: "Aruba-Fabric"
        vrf_name: "Aruba-VRF"
        operation: "create"
        ip_interface_data:
            vrf: "Aruba-VRF"
            enable: True
            if_type: loopback
            loopback_name: loopback10
            ipv4_primary_address:
                address: "10.10.10.32"
                prefix_length: 32
            switches:
                - "10.10.10.7"

-   name: Delete IP Interface using username and password
    arubanetworks.afc.afc_ip_interface:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        fabric_name: "Aruba-Fabric"
        vrf_name: "Aruba-VRF"
        operation: "delete"
        ip_interface_data:
            vrf: "Aruba-VRF"
            enable: True
            local_proxy_arp_enabled: True
            name: "VLAN250"
            vlan: 250
            if_type: vlan
            ipv4_primary_address:
                address: "10.10.10.11"
                prefix_length: 24
            active_gateway:
                ipv4_address: "10.10.10.1"
                mac_address: "00:00:00:00:00:01"
            switches:
                - "10.10.10.7"

-   name: Delete a ROP (Routed Only Port) using username and password
    arubanetworks.afc.afc_ip_interface:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        fabric_name: "Aruba-Fabric"
        vrf_name: "Aruba-VRF"
        operation: "delete"
        ip_interface_data:
            vrf: "Aruba-VRF"
            enable: True
            local_proxy_arp_enabled: True
            name: "VLAN250"
            interface: 1/1/14
            if_type: routed
            ipv4_primary_address:
                address: "10.10.10.25"
                prefix_length: 24
            switches:
                - "10.10.10.7"

-   name: Delete an SVI using username and password
    arubanetworks.afc.afc_ip_interface:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        fabric_name: "Aruba-Fabric"
        vrf_name: "Aruba-VRF"
        operation: "delete"
        ip_interface_data:
            vrf: "Aruba-VRF"
            enable: True
            local_proxy_arp_enabled: True
            name: "VLAN250"
            vlan: 250
            if_type: vlan
            ipv4_primary_address:
                address: "10.10.10.11-10.10.10.50"
                prefix_length: 24
            active_gateway:
                ipv4_address: "10.10.10.1"
                mac_address: "00:00:00:00:00:01"
            switches:
                - "10.10.10.7"
                - "10.10.10.8"
                - "10.10.10.9"

-   name: Delete a loopback interface using username and password
    arubanetworks.afc.afc_ip_interface:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        fabric_name: "Aruba-Fabric"
        vrf_name: "Aruba-VRF"
        operation: "delete"
        ip_interface_data:
            vrf: "Aruba-VRF"
            enable: True
            if_type: loopback
            loopback_name: loopback10
            ipv4_primary_address:
                address: "10.10.10.32"
                prefix_length: 32
            switches:
                - "10.10.10.7"

-   name: Create IP Interface using token
    arubanetworks.afc.afc_ip_interface:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        fabric_name: "Aruba-Fabric"
        vrf_name: "Aruba-VRF"
        operation: "create"
        ip_interface_data:
            vrf: "Aruba-VRF"
            enable: True
            local_proxy_arp_enabled: True
            name: "VLAN250"
            vlan: 250
            if_type: vlan
            ipv4_primary_address:
                address: "10.10.10.11-10.10.10.50"
                prefix_length: 24
            active_gateway:
                ipv4_address: "10.10.10.1"
                mac_address: "00:00:00:00:00:01"
            switches:
                - "10.10.10.7"
                - "10.10.10.8"
                - "10.10.10.9"

-   name: Create a ROP (Routed Only Port) using token
    arubanetworks.afc.afc_ip_interface:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        fabric_name: "Aruba-Fabric"
        vrf_name: "Aruba-VRF"
        operation: "create"
        ip_interface_data:
            vrf: "Aruba-VRF"
            enable: True
            local_proxy_arp_enabled: True
            name: "VLAN250"
            interface: 1/1/14
            if_type: routed
            ipv4_primary_address:
                address: "10.10.10.25"
                prefix_length: 24
            switches:
                - "10.10.10.7"

-   name: Create an SVI using token
    arubanetworks.afc.afc_ip_interface:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        fabric_name: "Aruba-Fabric"
        vrf_name: "Aruba-VRF"
        operation: "create"
        ip_interface_data:
            vrf: "Aruba-VRF"
            enable: True
            local_proxy_arp_enabled: True
            name: "VLAN250"
            vlan: 250
            if_type: vlan
            ipv4_primary_address:
                address: "10.10.10.11-10.10.10.50"
                prefix_length: 24
            active_gateway:
                ipv4_address: "10.10.10.1"
                mac_address: "00:00:00:00:00:01"
            switches:
                - "10.10.10.7"
                - "10.10.10.8"
                - "10.10.10.9"

-   name: Create a loopback interface using token
    arubanetworks.afc.afc_ip_interface:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        fabric_name: "Aruba-Fabric"
        vrf_name: "Aruba-VRF"
        operation: "create"
        ip_interface_data:
            vrf: "Aruba-VRF"
            enable: True
            if_type: loopback
            loopback_name: loopback10
            ipv4_primary_address:
                address: "10.10.10.32"
                prefix_length: 32
            switches:
                - "10.10.10.7"

-   name: Delete IP Interface using token
    arubanetworks.afc.afc_ip_interface:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        fabric_name: "Aruba-Fabric"
        vrf_name: "Aruba-VRF"
        operation: "delete"
        ip_interface_data:
            vrf: "Aruba-VRF"
            enable: True
            local_proxy_arp_enabled: True
            name: "VLAN250"
            vlan: 250
            if_type: vlan
            ipv4_primary_address:
                address: "10.10.10.11"
                prefix_length: 24
            active_gateway:
                ipv4_address: "10.10.10.1"
                mac_address: "00:00:00:00:00:01"
            switches:
                - "10.10.10.7"

-   name: Delete a ROP (Routed Only Port) using token
    arubanetworks.afc.afc_ip_interface:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        fabric_name: "Aruba-Fabric"
        vrf_name: "Aruba-VRF"
        operation: "delete"
        ip_interface_data:
            vrf: "Aruba-VRF"
            enable: True
            local_proxy_arp_enabled: True
            name: "VLAN250"
            interface: 1/1/14
            if_type: routed
            ipv4_primary_address:
                address: "10.10.10.25"
                prefix_length: 24
            switches:
                - "10.10.10.7"

-   name: Delete an SVI using token
    arubanetworks.afc.afc_ip_interface:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        fabric_name: "Aruba-Fabric"
        vrf_name: "Aruba-VRF"
        operation: "delete"
        ip_interface_data:
            vrf: "Aruba-VRF"
            enable: True
            local_proxy_arp_enabled: True
            name: "VLAN250"
            vlan: 250
            if_type: vlan
            ipv4_primary_address:
                address: "10.10.10.11-10.10.10.50"
                prefix_length: 24
            active_gateway:
                ipv4_address: "10.10.10.1"
                mac_address: "00:00:00:00:00:01"
            switches:
                - "10.10.10.7"
                - "10.10.10.8"
                - "10.10.10.9"

-   name: Delete a loopback interface using token
    arubanetworks.afc.afc_ip_interface:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        fabric_name: "Aruba-Fabric"
        vrf_name: "Aruba-VRF"
        operation: "delete"
        ip_interface_data:
            vrf: "Aruba-VRF"
            enable: True
            if_type: loopback
            loopback_name: loopback10
            ipv4_primary_address:
                address: "10.10.10.32"
                prefix_length: 32
            switches:
                - "10.10.10.7"
```
