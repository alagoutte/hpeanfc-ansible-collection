#!/usr/bin/python

# (C) Copyright 2020-2025 Hewlett Packard Enterprise Development LP.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: afc_vlan
version_added: "0.0.1"
short_description: Create or Delete VLANs through HPE ANW Fabric Composer.
description: >
    This Ansible module facilitates the creation or deletion of VLANs in a
    fabric managed by the HPE ANW Fabric Composer.
    It creates VLANs based on specified names and IDs and updates their
    configuration within the fabric.
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
            Operation to be performed with the VLAN, create or delete
        type: str
        operation:
            - create
            - delete
        required: true
    data:
        description: >
            Data to manipulate VLANs.
        type: dict
        suboptions:
            type:
                description: VLAN type.
                type: str
                choices:
                    - vlan_group
                    - stretched_vlan
                required: true
            name:
                description: VLAN Name.
                type: str
                required: true
            description:
                description: VLAN Description.
                type: str
                required: false
            vlans:
                description: >
                    VLAN Group specific.
                    VLANs list.
                type: str
                required: false
            fabrics:
                description: >
                    Stretched VLAN Specific.
                    List of Fabrics
                type: list
                elements: str
                required: false
            stretched_vlans:
                description: >
                    Stretched VLAN Specific.
                    Stretched VLAN ID.
                type: str
                required: false
            global_route_targets:
                description: Stretched VLAN Specific. Global Route Targets.
                type: list
                required: false
                elements: dict
                suboptions:
                    rt_type:
                        description: Route Target Type.
                        type: str
                        choices:
                            - NN:VLAN
                            - NN:VNI
                        required: false
                    administrative_number:
                        description: AS Number to be used.
                        type: str
                        required: false
        required: true
author: Aruba Networks (@ArubaNetworks)
"""

EXAMPLES = r"""
-   name: Create a VLAN Group in HPE ANW Fabric Composer using username
          and password
    arubanetworks.afc.afc_vlan:
        afc_ip: "10.10.10.10"
        afc_username: "admin"
        afc_password: "password"
        operation: create
        data:
            type: vlan_group
            name: Test-VLANGroup
            description: New VLAN Group
            vlans: "23,56-58"

-   name: Delete a VLAN Group in HPE ANW Fabric Composer using username
          and password
    arubanetworks.afc.afc_vlan:
        afc_ip: "10.10.10.10"
        afc_username: "admin"
        afc_password: "password"
        operation: "delete"
        data:
            name: Test-VLANGroup

-   name: Create a VLAN Group in HPE ANW Fabric Composer using token
    arubanetworks.afc.afc_vlan:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        operation: create
        data:
            type: vlan_group
            name: Test-VLANGroup
            description: New VLAN Group
            vlans: "23,56-58"

-   name: Delete a VLAN Group in HPE ANW Fabric Composer using token
    arubanetworks.afc.afc_vlan:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        operation: "delete"
        data:
            name: Test-VLANGroup

-   name: Create a Stretched VLAN in HPE ANW Fabric Composer using username
          and password
    arubanetworks.afc.afc_vlan:
        afc_ip: "10.10.10.10"
        afc_username: "admin"
        afc_password: "password"
        operation: create
        data:
            type: stretched_vlan
            fabrics:
                - DC1
                - DC2
            stretched_vlans: 301
            global_route_targets:
                - rt_type: NN:VLAN
                  administrative_number: 1

-   name: Create a VLAN Group in HPE ANW Fabric Composer using token
    arubanetworks.afc.afc_vlan:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        operation: create
        data:
            type: stretched_vlan
            fabrics:
                - DC1
                - DC2
            stretched_vlans: 301
            global_route_targets:
                - rt_type: NN:VLAN
                  administrative_number: 1
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
from pyafc.ports import vlan_group


def main():
    module_args = {
        "afc_ip": {"type": "str", "required": True},
        "afc_username": {"type": "str", "required": False},
        "afc_password": {"type": "str", "required": False},
        "auth_token": {"type": "str", "required": False},
        "operation": {"type": "str", "required": True},
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

    if afc_instance.afc_connected:
        if operation == "create":
            if data["type"] == "vlan_group":
                vlan_instance = vlan_group.VlanGroup(
                    afc_instance.client,
                    **data,
                )
                message, status, changed = vlan_instance.create_vlan_group(
                    **data,
                )
            elif data["type"] == "stretched_vlan":
                fabric_instance = fabric.Fabric(
                    afc_instance.client,
                    name=data["fabrics"][0],
                )
                message, status, changed = (
                    fabric_instance.create_vlan_stretching(**data)
                )
            else:
                message = "Type not supported - No action taken"
        elif operation == "update":
            if data["type"] == "stretched_vlan":
                fabric_instance = fabric.Fabric(
                    afc_instance.client,
                    name=data["fabrics"][0],
                )
                message, status, changed = (
                    fabric_instance.update_vlan_stretching(**data)
                )
            else:
                message = "Type not supported - No action taken"
        elif operation == "delete":
            if data["type"] == "vlan_group":
                vlan_instance = vlan_group.VlanGroup(
                    afc_instance.client,
                    **data,
                )
                message, status, changed = vlan_instance.delete_vlan_group()
            else:
                message = "Type not supported - No action taken"
        else:
            message = "Operation not supported - No action taken"
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
