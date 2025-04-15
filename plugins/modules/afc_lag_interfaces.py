#!/usr/bin/python

# (C) Copyright 2020-2025 Hewlett Packard Enterprise Development LP.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: afc_lag_interfaces
version_added: "0.0.1"
short_description: Configure LAG Interfaces.
description: >
    This module is used to configure LAG Interfaces.
options:
    afc_ip:
        description: >
            IP address of the HPE ANW Fabric Composer.
        type: str
        required: true
    afc_username:
        description:
            User account having write permission on the HPE ANW Fabric Composer
        type: str
        required: false
    afc_password:
        description:
            Password of the user account
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
    data:
        description: >
            Port configuration data. Structure is provided in the example.
        type: dict
        suboptions:
            lag_name:
                description: LAG Name
                type: str
                required: true
            lag_id:
                description: LAG ID
                type: int
                required: true
            ports:
                description: >
                    Physical ports to ne mapped to the LAG
                type: list
                elements: dict
                suboptions:
                    switch:
                        description: Switch IP Address
                        type: str
                        required: true
                    ports:
                        description: List of physical ports on that switch
                        type: list
                        elements: str
                        required: true
            global_config:
                description: >
                    Global LAG configuration
                type: dict
                suboptions:
                    ungrouped_vlans:
                        description: set of VLANs to be configured
                        type: str
                        required: true
                    native_vlan:
                        description: Native VLAN
                        type: int
                        required: true
                    tagged:
                        description: tagged Native VLAN
                        type: bool
                        required: true
                    lacp_fallback:
                        description: LACP Fallback Enabled
                        type: bool
                        required: true
                    enable_lossless:
                        description: Lossless enabled
                        type: bool
                        required: true
            lacp_config:
                description: >
                    LACP-related configuration
                type: dict
                suboptions:
                    interval:
                        description: LACP Rate
                        type: str
                        choices:
                            - slow
                            - fast
                        required: true
            speed_config:
                description: >
                    Speed-related configuration
                type: dict
                suboptions:
                    speed:
                        description: LAG's speed Rate
                        type: str
                        required: true
        required: true
author: Aruba Networks (@ArubaNetworks)
"""

EXAMPLES = r"""
-   name: Configure LAG using username and password
    arubanetworks.afc.afc_lag_interfaces:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        data:
            lag_name: 'lag15'
            lag_id: 15
            ports:
                - switch: "10.10.10.7"
                  ports:
                    - "1/1/10"
                    - "1/1/11"
            global_config:
                ungrouped_vlans: "1253-1254"
                native_vlan: 1
                lacp_fallback: False
            lacp_config:
                interval: "fast"

-   name: Configure VSX LAG using username and password
    arubanetworks.afc.afc_lag_interfaces:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        data:
            lag_name: 'lag15'
            lag_id: 15
            ports:
                - switch: "10.10.10.7"
                  ports:
                    - "1/1/10"
                - switch: "10.10.10.8"
                  ports:
                    - "1/1/10"
            global_config:
                ungrouped_vlans: "1253-1254"
                native_vlan: 1
                lacp_fallback: False
            lacp_config:
                interval: "fast"

-   name: Configure LAG using token
    arubanetworks.afc.afc_lag_interfaces:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        data:
            lag_name: 'lag15'
            lag_id: 15
            ports:
                - switch: "10.10.10.7"
                  ports:
                    - "1/1/10"
                    - "1/1/11"
            global_config:
                ungrouped_vlans: "1253-1254"
                native_vlan: 1
                lacp_fallback: False
            lacp_config:
                interval: "fast"

-   name: Configure VSX LAG using token
    arubanetworks.afc.afc_lag_interfaces:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        data:
            lag_name: 'lag15'
            lag_id: 15
            ports:
                - switch: "10.10.10.7"
                  ports:
                    - "1/1/10"
                - switch: "10.10.10.8"
                  ports:
                    - "1/1/10"
            global_config:
                ungrouped_vlans: "1253-1254"
                native_vlan: 1
                lacp_fallback: False
            lacp_config:
                interval: "fast"
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
from pyafc.ports import ports


def main():
    module_args = {
        **afc_argument_spec(),
        "data": {"type": "dict", "required": True},
    }

    ansible_module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    # Get playbook's arguments
    username = ansible_module.params["afc_username"]
    password = ansible_module.params["afc_password"]
    data = ansible_module.params["data"]

    result = {"changed": False}

    if ansible_module.check_mode:
        ansible_module.exit_json(**result)

    status = False
    changed = False
    message = ""

    auth_data = build_auth_data(ansible_module)

    afc_instance = instantiate_afc_object(data=auth_data)

    if afc_instance.afc_connected:
        message, status, changed = ports.PORT.configure_lags(
            afc_instance.client,
            data,
        )

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
