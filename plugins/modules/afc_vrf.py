#!/usr/bin/python

# (C) Copyright 2020-2025 Hewlett Packard Enterprise Development LP.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: afc_vrf
version_added: "0.0.1"
short_description: Create or delete a VRF in the specified fabric.
description: >
    This module creates or deletes a VRF in the specified fabric.
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
            Operation to be performed on the VRF, create delete or reapply.
        type: str
        choices:
            - create
            - reapply
            - delete
        required: true
    data:
        description: >
            VRF specific data. Structure provided in the example.
        type: dict
        suboptions:
            name:
                description: VRF Name
                type: str
                required: true
            fabric:
                description: Fabric Name
                type: str
                required: true
            vni:
                description: L3VNI attached to the VRF
                type: int
                required: false
            route_distinguisher:
                description: Route Distinguisher.
                type: str
                default: 'loopback1:1'
                required: false
            max_cps_mode:
                description: >
                    Specific to HPE ANW 10000.
                    Maximum Connections per Seconds mode.
                type: str
                choices:
                    - unlimited
                    - enabled
                default: unlimited
                required: false
            max_cps:
                description: >
                    Specific to HPE ANW 10000.
                    Maximum Connections per Seconds.
                type: int
                required: false
            max_sessions_mode:
                description: >
                    Specific to HPE ANW 10000.
                    Maximum Sessions mode.
                type: str
                choices:
                    - unlimited
                    - enabled
                default: unlimited
                required: false
            max_sessions:
                description: >
                    Specific to HPE ANW 10000.
                    Maximum number of Sessions.
                type: int
                required: false
            allow_session_reuse:
                description: >
                    Specific to HPE ANW 10000.
                    Allow Session Reuse.
                type: bool
                default: false
                required: false
            connection_tracking_mode:
                description: >
                    Specific to HPE ANW 10000.
                    Connection tracking enabled.
                type: bool
                default: false
                required: false
            route_target:
                description: >
                    Route Target specific data.
                type: dict
                required: false
                suboptions:
                    primary_route_target:
                        description: >
                            Primary Route Target
                        type: dict
                        suboptions:
                            as_number:
                                description: AS Number
                                type: str
                                required: false
                            address_family:
                                description: Address Family
                                type: str
                                choices:
                                    - evpn
                                    - ipv4_unicast
                                    - ipv6_unicast
                                required: false
                            route_mode:
                                description: Route Mode
                                type: str
                                choices:
                                    - import
                                    - export
                                    - both
                                required: false
                        required: false
                    secondary_route_targets:
                        description: >
                            Secondary Route Targets, as a list
                        type: list
                        elements: dict
                        suboptions:
                            as_number:
                                description: AS Number
                                type: str
                                required: false
                            address_family:
                                description: Address Family
                                type: str
                                choices:
                                    - evpn
                                    - ipv4_unicast
                                    - ipv6_unicast
                                required: false
                            route_mode:
                                description: Route Mode
                                type: str
                                choices:
                                    - import
                                    - export
                                    - both
                                required: false
                        required: false
        required: true
author: Aruba Networks (@ArubaNetworks)
"""

EXAMPLES = r"""
-   name: Create VRF using username and password
    arubanetworks.afc.afc_vrf:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        operation: "create"
        data:
            name: "Aruba-VRF"
            fabric: "Aruba-Fabric"
            vni: 10000
            route_target:
                primary_route_target:
                    as_number: "65000:1"
                    address_family: "evpn"
                    route_mode: "both"
                secondary_route_targets:
                    -   as_number: "1:1"
                        address_family: "evpn"
                        route_mode: "both"

-   name: Reapply VRF using username and password
    arubanetworks.afc.afc_vrf:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        operation: "reapply"
        data:
            name: "Aruba-VRF"
            fabric: "Aruba-Fabric"

-   name: Delete VRF using username and password
    arubanetworks.afc.afc_vrf:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        operation: "delete"
        data:
            name: "Aruba-VRF"
            fabric: "Aruba-Fabric"

-   name: Create VRF using token
    arubanetworks.afc.afc_vrf:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        operation: "create"
        data:
            name: "Aruba-VRF"
            fabric: "Aruba-Fabric"
            vni: 10000
            route_target:
                primary_route_target:
                    as_number: "65000:1"
                    address_family: "evpn"
                    route_mode: "both"
                secondary_route_targets:
                    -   as_number: "1:1"
                        address_family: "evpn"
                        route_mode: "both"

-   name: Reapply VRF using username and password
    arubanetworks.afc.afc_vrf:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        operation: "reapply"
        data:
            name: "Aruba-VRF"
            fabric: "Aruba-Fabric"

-   name: Delete VRF using token
    arubanetworks.afc.afc_vrf:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        operation: "delete"
        data:
            name: "Aruba-VRF"
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
                name=data["name"],
                fabric_uuid=fabric_instance.uuid,
            )
            if operation == "create":
                message, status, changed = vrf_instance.create_vrf(**data)
            elif operation == "reapply":
                message, status, changed = vrf_instance.reapply_vrf()
            elif operation == "delete":
                message, status, changed = vrf_instance.delete_vrf()
            else:
                message = "Operation not supported - No action taken"
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
