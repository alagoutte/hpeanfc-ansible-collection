#!/usr/bin/python
# -*- coding: utf-8 -*-

# (C) Copyright 2020-2025 Hewlett Packard Enterprise Development LP.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: afc_multifabrics
version_added: "0.0.1"
short_description: Configure Multi-Fabrics.
description: >
    This module is used to configure Multi-Fabrics.
options:
    afc_ip:
        description: >
            IP address of HPE ANW Fabric Composer.
        type: str
        required: true
    afc_username:
        description: >
            User account having permission to create MF on
            HPE ANW Fabric Composer
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
            Operation to execute - Create.
        type: str
        choices:
            - create
        required: true
    data:
        description: >
            Multi-Fabrics data containing information.
        type: dict
        suboptions:
            name:
                description: EVPN Workflow Name
                type: str
                required: true
            local_fabric:
                description: Name of the local Fabric
                type: str
                required: true
            border_leader:
                description: >
                    Name or IPv4 Address of the Border Leader.
                    In case of VSX just provide the Name or
                    IPv4 Address of one of the members.
                type: str
                required: true
            l3_ebgp_borders:
                description: L3 eBGP border switch(es)
                type: list
                elements: str
                required: false
            bgp_auth_password:
                description: Set password for bgp neighbor
                type: str
                required: false
            uplink_to_uplink:
                description: Enable or Disable uplink to uplink.
                type: bool
                required: false
            remote_fabrics:
                description: Information related to the remote Fabric.
                type: list
                elements: dict
                required: true
                suboptions:
                    fabric:
                        description: Name of the remote Fabric
                        type: str
                        required: true
                    border_leader:
                        description: >
                            Name or IPv4 Address of the Border Leader.
                            In case of VSX just provide the Name or
                            IPv4 Address of one of the members.
                        type: str
                        required: true
                    peering_ip:
                        description: IP address for BGP neighbor peering
                        type: str
                        required: true
        required: true
author: Aruba Networks (@ArubaNetworks)
"""

EXAMPLES = r"""
-   name: Configure L3LS settings using username and password
    arubanetworks.afc.afc_multifabrics:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        operation: "create"
        data:
            name: "MF-ArubaFabric"
            local_fabric: "Aruba-Fabric"
            border_leader: "10.10.10.20"
            remote_fabrics:
                - fabric: "Aruba-Fabric2"
                  border_leader: "10.20.20.20"
                  peering_ip: "loopback0"

-   name: Configure L3LS settings using token
    arubanetworks.afc.afc_multifabrics:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        operation: "create"
        data:
            name: "MF-ArubaFabric"
            local_fabric: "Aruba-Fabric"
            border_leader: "10.10.10.20"
            remote_fabrics:
                - fabric: "Aruba-Fabric2"
                  border_leader: "10.20.20.20"
                  peering_ip: "loopback0"

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
    data = ansible_module.params["data"]

    if token is not None:
        auth_data = {
            "ip": ip,
            "auth_token": token,
        }
    else:
        auth_data = {
            "ip": ip,
            "username": username,
            "password": password,
        }

    afc_instance = instantiate_afc_object(data=auth_data)

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
            name=data["local_fabric"],
        )
        if fabric_instance.uuid:
            message, status, changed = fabric_instance.create_multi_fabrics(
                **data
            )
        else:
            message = f"Fabric {data['local_fabric']} not found"
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
