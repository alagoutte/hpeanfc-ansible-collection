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
    disable_tls_verification:
        description: >
            Disable TLS certificate verification when connecting to AFC.
            Only enable this for AFC instances using self-signed
            certificates.
        type: bool
        required: false
        default: false
    operation:
        description: >
            Operation to be performed with the VLAN, create, update or delete
        type: str
        choices:
            - create
            - update
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
                    - vlan
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
            fabric:
                description: >
                    VLAN specific.
                    Name of the Fabric on which the VLAN(s) are managed.
                type: str
                required: false
            vlan_id:
                description: >
                    VLAN specific.
                    VLAN range(s), e.g. "10" or "10,20-30".
                type: str
                required: false
            vlan_name:
                description: >
                    VLAN specific.
                    Name given to the VLAN(s). Renaming an existing VLAN is
                    dependent on the AFC version and may be a no-op on some
                    releases; assigning devices always applies.
                type: str
                required: false
            switches:
                description: >
                    VLAN specific.
                    List of devices (IP address or name) to which the VLAN(s)
                    are assigned or from which they are unassigned.
                type: list
                elements: str
                required: false
            fabric_scope:
                description: >
                    VLAN specific.
                    Alternative to switches to scope the VLAN creation.
                type: str
                choices:
                    - include_spine
                    - exclude_spine
                required: false
            strict_firewall_bypass_enabled:
                description: >
                    VLAN specific.
                    Enable strict firewall bypass on the VLAN(s).
                type: bool
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
-   name: Create VLANs and assign them to devices using username and password
    arubanetworks.afc.afc_vlan:
        afc_ip: "10.10.10.10"
        afc_username: "admin"
        afc_password: "password"
        operation: create
        data:
            type: vlan
            fabric: DC1
            vlan_id: "100,200-202"
            vlan_name: Production
            switches:
                - 10.149.2.10
                - Leaf-1

-   name: Assign an existing VLAN to additional devices and rename it
    arubanetworks.afc.afc_vlan:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        operation: update
        data:
            type: vlan
            fabric: DC1
            vlan_id: "100"
            vlan_name: Prod-Renamed
            switches:
                - Leaf-2

-   name: Unassign a VLAN from specific devices
    arubanetworks.afc.afc_vlan:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        operation: delete
        data:
            type: vlan
            fabric: DC1
            vlan_id: "100"
            switches:
                - Leaf-2

-   name: Delete VLANs from the whole Fabric
    arubanetworks.afc.afc_vlan:
        afc_ip: "10.10.10.10"
        afc_username: "admin"
        afc_password: "password"
        operation: delete
        data:
            type: vlan
            fabric: DC1
            vlan_id: "100,200-202"

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
    afc_argument_spec,
    build_auth_data,
    instantiate_afc_object,
)
from pyafc.fabric import fabric
from pyafc.ports import vlan_group


def main():
    module_args = {
        **afc_argument_spec(),
        "operation": {"type": "str", "required": True},
        "data": {"type": "dict", "required": True},
    }

    ansible_module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    # Get playbook's arguments
    username = ansible_module.params["afc_username"]
    password = ansible_module.params["afc_password"]
    operation = ansible_module.params["operation"]
    data = ansible_module.params["data"]

    auth_data = build_auth_data(ansible_module)

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
            elif data["type"] == "vlan":
                fabric_instance = fabric.Fabric(
                    afc_instance.client,
                    name=data["fabric"],
                )
                message, status, changed = fabric_instance.create_vlan(**data)
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
            if data["type"] == "vlan":
                fabric_instance = fabric.Fabric(
                    afc_instance.client,
                    name=data["fabric"],
                )
                message, status, changed = fabric_instance.update_vlan(**data)
            elif data["type"] == "stretched_vlan":
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
            elif data["type"] == "vlan":
                fabric_instance = fabric.Fabric(
                    afc_instance.client,
                    name=data["fabric"],
                )
                message, status, changed = fabric_instance.delete_vlan(**data)
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
