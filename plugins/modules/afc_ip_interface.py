#!/usr/bin/python

# (C) Copyright 2020-2025 Hewlett Packard Enterprise Development LP.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: afc_ip_interface
version_added: "0.0.1"
short_description: Create or delete a SVI, a Loopback or a Routed Port.
description: >
    This module is used to create and delete SVI, a Loopback or a Routed Port.
options:
    afc_ip:
        description: >
            IP address of the HPE ANW Fabric Composer.
        type: str
        required: true
    afc_username:
        description:
        - User account having write permission on the HPE ANW Fabric Composer
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
    operation:
        description: >
            Operation to be performed with the IP Interface, ROP,
            loopback or SVI, create or delete.
        type: str
        choices:
            - create
            - delete
        required: true
    data:
        description: >
            IP Interface data containing if_type, vlan, active_gateway,
            ipv4_primary_address, local_proxy_arp_enabled and the switches.
            The values vlan and the prefix_length need to be integers.
            Structure is provided in the example.
        type: dict
        suboptions:
            fabric:
                description: Fabric Name
                type: str
                required: true
            vrf:
                description: VRF Name
                type: str
                required: true
            name:
                description: IP Interface Name
                type: str
                required: true
            enable:
                description: IP Interface's Status.
                type: bool
                default: true
                required: false
            local_proxy_arp_enabled:
                description: >
                    Enable or disable local proxy arp.
                type: bool
                default: false
                required: false
            vlan:
                description: VLAN to be mapped to the IP Interface.
                type: int
                required: false
            if_type:
                description: IP Interface type.
                type: str
                choices:
                    - vlan
                    - routed
                    - loopback
                required: true
            ipv4_primary_address:
                description: Primary IPv4 to be configured.
                type: dict
                required: true
                suboptions:
                    address:
                        description: IPv4 Address. Can IPv4 Address or Range
                        type: str
                        required: true
                    prefix_length:
                        description: IPv4 Prefix length.
                        type: int
                        required: true
            active_gateway:
                description: Active Gateway to be configured.
                type: dict
                required: false
                suboptions:
                    ipv4_address:
                        description: IPv4 Address.
                        type: str
                        required: true
                    mac_address:
                        description: MAC Address.
                        type: str
                        required: true
            switches:
                description: List of Switches
                type: list
                elements: str
                required: false
        required: true

author: Aruba Networks (@ArubaNetworks)
"""

EXAMPLES = r"""
-   name: Create IP Interface using username and password
    arubanetworks.afc.afc_ip_interface:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        operation: "create"
        data:
            fabric: "Aruba-Fabric"
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
        operation: "create"
        data:
            fabric: "Aruba-Fabric"
            vrf: "Aruba-VRF"
            enable: True
            local_proxy_arp_enabled: True
            name: "ROP to External Router"
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
        operation: "create"
        data:
            fabric: "Aruba-Fabric"
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
        operation: "create"
        data:
            fabric: "Aruba-Fabric"
            vrf: "Aruba-VRF"
            enable: True
            if_type: loopback
            name: loopback10
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
        operation: "delete"
        data:
            fabric: "Aruba-Fabric"
            vrf: "Aruba-VRF"
            name: "VLAN250"
            switches:
                - "10.10.10.7"

-   name: Delete a ROP (Routed Only Port) using username and password
    arubanetworks.afc.afc_ip_interface:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        operation: "delete"
        data:
            fabric: "Aruba-Fabric"
            vrf: "Aruba-VRF"
            name: 1/1/14
            switches:
                - "10.10.10.7"

-   name: Delete an SVI using username and password
    arubanetworks.afc.afc_ip_interface:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        operation: "delete"
        data:
            fabric: "Aruba-Fabric"
            vrf: "Aruba-VRF"
            name: "VLAN250"
            switches:
                - "10.10.10.7"
                - "10.10.10.8"
                - "10.10.10.9"

-   name: Delete a loopback interface using username and password
    arubanetworks.afc.afc_ip_interface:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        operation: "delete"
        data:
            fabric: "Aruba-Fabric"
            vrf: "Aruba-VRF"
            name: loopback10
            switches:
                - "10.10.10.7"

-   name: Create IP Interface using token
    arubanetworks.afc.afc_ip_interface:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        operation: "create"
        data:
            fabric: "Aruba-Fabric"
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
        operation: "create"
        data:
            fabric: "Aruba-Fabric"
            vrf: "Aruba-VRF"
            enable: True
            local_proxy_arp_enabled: True
            name: "ROP to External Router"
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
        operation: "create"
        data:
            fabric: "Aruba-Fabric"
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
        operation: "create"
        data:
            fabric: "Aruba-Fabric"
            vrf: "Aruba-VRF"
            enable: True
            if_type: loopback
            name: loopback10
            ipv4_primary_address:
                address: "10.10.10.32"
                prefix_length: 32
            switches:
                - "10.10.10.7"

-   name: Delete IP Interface using token
    arubanetworks.afc.afc_ip_interface:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        operation: "delete"
        data:
            fabric: "Aruba-Fabric"
            vrf: "Aruba-VRF"
            name: "VLAN250"
            switches:
                - "10.10.10.7"

-   name: Delete a ROP (Routed Only Port) using token
    arubanetworks.afc.afc_ip_interface:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        operation: "delete"
        data:
            fabric: "Aruba-Fabric"
            vrf: "Aruba-VRF"
            name: "ROP1"
            switches:
                - "10.10.10.7"

-   name: Delete an SVI using token
    arubanetworks.afc.afc_ip_interface:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        operation: "delete"
        data:
            fabric: "Aruba-Fabric"
            vrf: "Aruba-VRF"
            name: "VLAN250"
            switches:
                - "10.10.10.7"
                - "10.10.10.8"
                - "10.10.10.9"

-   name: Delete a loopback interface using token
    arubanetworks.afc.afc_ip_interface:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        operation: "delete"
        data:
            fabric: "Aruba-Fabric"
            vrf: "Aruba-VRF"
            name: loopback10
            switches:
                - "10.10.10.7"
"""

RETURN = r"""
message:
    description: The output generated by the module
    type: str
    returned: always
    sample: "Successfully completed configuration"
status:
    description: True or False depending on the action taken
    type: bool
    returned: always
    sample: True
changed:
    description: True or False if something has been changed or not
    type: bool
    returned: always
    sample: True
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.arubanetworks.afc.plugins.module_utils.afc import (
    instantiate_afc_object,
)
from pyafc.fabric import fabric
from pyafc.vrf import vrf


def main():
    module_args = {
        "afc_ip": {"type": "str", "required": True},
        "afc_username": {"type": "str", "required": False},
        "afc_password": {"type": "str", "required": False},
        "auth_token": {"type": "str", "required": False},
        "operation": {"type": "str", "required": False},
        "data": {"type": "dict", "required": True},
    }

    ansible_module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    # Get playbook's arguments
    token = None
    ip = ansible_module.params["afc_ip"]
    if "afc_username" in list(ansible_module.params.keys()):
        username = ansible_module.params["afc_username"]
    if "afc_password" in list(ansible_module.params.keys()):
        password = ansible_module.params["afc_password"]
    if "auth_token" in list(ansible_module.params.keys()):
        token = ansible_module.params["auth_token"]
    operation = ansible_module.params["operation"]
    data = ansible_module.params["data"]

    if token is not None:
        auth_data = {"ip": ip, "auth_token": token}
    else:
        auth_data = {"ip": ip, "username": username, "password": password}

    result = {"changed": False}

    if ansible_module.check_mode:
        ansible_module.exit_json(**result)

    status = False
    changed = False
    message = ""

    afc_instance = instantiate_afc_object(data=auth_data)

    if afc_instance.afc_connected:
        fabric_instance = fabric.Fabric(
            afc_instance.client,
            name=data["fabric"],
        )
        if fabric_instance.uuid:
            vrf_instance = vrf.Vrf(
                afc_instance.client,
                name=data["vrf"],
                fabric_uuid=fabric_instance.uuid,
            )
            if vrf_instance.uuid:
                if operation == "create":
                    message, status, changed = (
                        vrf_instance.create_ip_interface(**data)
                    )
                elif operation == "delete":
                    message, status, changed = (
                        vrf_instance.delete_ip_interface(**data)
                    )
                else:
                    message = "Operation not supported - No action taken"
            else:
                message = "VRF not found - No action taken"
                status = False
                changed = False
        else:
            message = "Fabric not found - No action taken"
            status = False
            changed = False

        # Disconnect session if username and password are passed
        if username and password:
            afc_instance.disconnect()

    else:
        message = "Not connected to AFC"

    result["message"] = message
    result["status"] = status
    result["changed"] = changed

    # Exit
    if status:
        ansible_module.exit_json(changed=changed, msg=message)
    else:
        ansible_module.fail_json(changed=changed, msg=message)


if __name__ == "__main__":
    main()
