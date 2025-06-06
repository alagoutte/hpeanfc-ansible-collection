#!/usr/bin/python

# (C) Copyright 2020-2025 Hewlett Packard Enterprise Development LP.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: afc_overlay
version_added: "0.0.1"
short_description: >
    Apply an overlay configuration in the specified fabric and vrf.
description: >
    This module applies an overlay configuration in the specified fabric
    and vrf.
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
            Operation to be performed on the Overlay, create or reapply.
        type: str
        choices:
         - create
         - delete
        required: true
    data:
        description: >
            Overlay configuration data.
            The mandatory key bgp_type within the dict ca
            have value "internal" or "external".
            Structure is provided in the example.
        type: dict
        suboptions:
            name:
                description: Overlay Workflow Name
                type: str
                required: true
            fabric:
                description: Fabric Name
                type: str
                required: true
            vrf:
                description: VRF Name
                type: str
                required: true
            ipv4_address:
                description: IPv4 Resource Pool used for Loopbacks
                type: str
                required: true
            spine_leaf_asn:
                description: AS Number used for BGP configuration
                type: str
                required: true
            bgp_type:
                description: BGP Type used for Overlay configuration
                type: str
                choices:
                 - internal
                 - external
                required: true
        required: true
author: Aruba Networks (@ArubaNetworks)
"""

EXAMPLES = r"""
-   name: Create an overlay configuration using username and password
    arubanetworks.afc.afc_overlay:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        operation: "create"
        data:
            name: "Test-Overlay"
            fabric: "Aruba-Fabric"
            vrf: "Aruba-VRF"
            ipv4_address: 'IP POOL'
            spine_leaf_asn: "65001"
            bgp_type: 'internal'

-   name: Reapply an overlay configuration using username and password
    arubanetworks.afc.afc_overlay:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        operation: reapply
        data:
            name: "Test-Overlay"
            fabric: "Aruba-Fabric"
            vrf: "Aruba-VRF"

-   name: Create an overlay configuration using token
    arubanetworks.afc.afc_overlay:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        operation: "create"
        data:
            name: "Test-Overlay"
            fabric: "Aruba-Fabric"
            vrf: "Aruba-VRF"
            ipv4_address: 'IP POOL'
            spine_leaf_asn: "65001"
            bgp_type: 'internal'

-   name: Reapply an overlay configuration using token
    arubanetworks.afc.afc_overlay:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        operation: reapply
        data:
            name: "Test-Overlay"
            fabric: "Aruba-Fabric"
            vrf: "Aruba-VRF"
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
        "data": {"type": "dict", "required": True},
        "operation": {"type": "str", "required": True},
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
    operation = ansible_module.params["operation"]

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
        if fabric_instance.uuid:
            vrf_instance = vrf.Vrf(
                afc_instance.client,
                name=data["vrf"],
                fabric_uuid=fabric_instance.uuid,
            )
            if vrf_instance.uuid:
                if operation == "create":
                    message, status, changed = vrf_instance.create_overlay(
                        **data,
                    )
                elif operation == "reapply":
                    message, status, changed = vrf_instance.reapply_overlay(
                        data["name"],
                    )
                else:
                    message = "Operation not supported - No action taken"
            else:
                message = "VRF does not exist - No action taken"
        else:
            message = "Fabric does not exist - No action taken"
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
