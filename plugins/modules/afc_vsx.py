#!/usr/bin/python

# (C) Copyright 2020-2025 Hewlett Packard Enterprise Development LP.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: afc_vsx
version_added: "0.0.1"
short_description: >
    Create or delete a VSX configuration in the specified fabric.
description: >
    This module creates or deletes a VSX configuration in the specified fabric.
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
            Operation to be performed on the VSX, create or reapply, delete not
            supported.
        type: str
        choices:
            - create
            - reapply
            - delete
        required: true
    data:
        description: >
            VSX configuration data as specified in the example below.
        type: dict
        suboptions:
            name:
                description: VSX Config name
                type: str
                required: true
            fabric:
                description: Fabric on which the VSX worflow will be applied
                type: str
                required: true
            system_mac_range:
                description: MAC Resource Pool used for VSX System Mac
                type: str
                required: true
            keepalive_ip_pool_range:
                description: IPv4 Resource Pool used for KeepAlive
                type: str
                required: false
            keep_alive_interface_mode:
                description: >
                    IP interface mode used for Keep alive interface
                type: str
                choices:
                    - routed
                    - loopback
                required: true
        required: true
author: Aruba Networks (@ArubaNetworks)
"""

EXAMPLES = r"""
-   name: Create VSX using username and password
    arubanetworks.afc.afc_vsx:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        operation: "create"
        data:
            name: "Test-VSX"
            fabric: "Aruba-Fabric"
            system_mac_range: "MAC POOL"
            keepalive_ip_pool_range: "IP POOL"
            keep_alive_interface_mode: "loopback"

-   name: Reapply VSX using username and password
    arubanetworks.afc.afc_vsx:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        operation: "reapply"
        data:
            name: "Test-VSX"
            fabric: "Aruba-Fabric"

-   name: Delete VSX using username and password
    arubanetworks.afc.afc_vsx:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        operation: "delete"
        data:
            name: "Test-VSX"
            fabric: "Aruba-Fabric"

-   name: Create VSX using token
    arubanetworks.afc.afc_vsx:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        operation: "create"
        data:
            name: "Test-VSX"
            fabric: "Aruba-Fabric"
            system_mac_range: "MAC POOL"
            keepalive_ip_pool_range: "IP POOL"
            keep_alive_interface_mode: "loopback"

-   name: Reapply VSX using token
    arubanetworks.afc.afc_vsx:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        operation: "reapply"
        data:
            name: "Test-VSX"
            fabric: "Aruba-Fabric"

-   name: Delete VSX using token
    arubanetworks.afc.afc_vsx:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        operation: "delete"
        data:
            name: "Test-VSX"
            fabric: "Aruba-Fabric"
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

    afc_instance = instantiate_afc_object(data=auth_data)

    if afc_instance.afc_connected:

        fabric_instance = fabric.Fabric(
            afc_instance.client,
            name=data["fabric"],
        )

        if operation == "create":
            message, status, changed = fabric_instance.create_vsx(**data)
        elif operation == "reapply":
            message, status, changed = fabric_instance.reapply_vsx()
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
