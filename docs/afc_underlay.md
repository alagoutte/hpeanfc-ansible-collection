# module: afc_underlay

Description: This module creates or deletes an underlay in the specified VRF.

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
fabric_name:
    description: >
        Name of the Fabric where an underlay configuration will be created or deleted from.
    type: str
    required: true
vrf_name:
    description: >
        Name of the VRF where underlay configuratoin needs to be applied.
    type: str
    required: true
operation:
    description: >
        Operation to be performed on the Underlay, create or reapply.
    type: str
    required: true
underlay_name:
    description: >
        Name of the underlay.
    type: str
    required: true
underlay_data:
    description: >
        Underlay configuration data. The mandatory structure is provided in the example.
    type: dict
    required: false
```

##### EXAMPLES

```YAML
-   name: Create an underlay configuration using username and password
    arubanetworks.afc.afc_underlay:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        fabric_name: "Aruba-Fabric"
        vrf_name: "default"
        operation: "create"
        underlay_name: "Test-underlay"
        underlay_data:
            ipv4_address: 'IP POOL'
            transit_vlan: 120
            underlay_type: 'OSPF'

-   name: Reapply an underlay configuration using username and password
    arubanetworks.afc.afc_underlay:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        fabric_name: "Aruba-Fabric"
        vrf_name: "default"
        operation: "reapply"
        underlay_name: "Test-underlay"

-   name: Create an underlay configuration using token
    arubanetworks.afc.afc_underlay:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        fabric_name: "Aruba-Fabric"
        vrf_name: "default"
        operation: "create"
        underlay_name: "Test-underlay"
        underlay_data:
            ipv4_address: 'IP POOL'
            transit_vlan: 120
            underlay_type: 'OSPF'

-   name: Reapply an underlay configuration using token
    arubanetworks.afc.afc_underlay:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        fabric_name: "Aruba-Fabric"
        vrf_name: "default"
        operation: "reapply"
        underlay_name: "Test-underlay"
```
