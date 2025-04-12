#!/usr/bin/python

# (C) Copyright 2020-2025 Hewlett Packard Enterprise Development LP.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: afc_switches
version_added: "0.0.1"
short_description: Manage Switches on and through AFC.
description: >
    This module allows to manage switches on and through
    HPE ANW Fabric Composer.
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
            Operation to be performed on the switch - One of : update,
            reconcile, reboot, save.
        type: str
        choices:
            - update
            - save
            - reconcile
            - reboot
        required: true
    data:
        description: >
            Data used to act on switches. Structre is provided in the example.
        type: dict
        suboptions:
            boot_partition:
                description: >
                    Reboot specific. Partition which will be used by
                    device to reboot.
                type: list
                choices:
                    - primary
                    - secondary
                    - active
                    - non-active
                default: active
                required: false
            fabric:
                description: List of Fabrics
                type: list
                elements: str
                required: false
            switches:
                description: List of Switches
                type: list
                elements: str
                required: false
        required: true
author: Aruba Networks (@ArubaNetworks)
"""

EXAMPLES = r"""
-   name: Update switch data on AFC using username and password
    arubanetworks.afc.afc_switches:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        operation: "update"
        data:
            switches: "10.10.10.15"
            name: "Updated_Switch_Name"

-   name: Reconcile switch on AFC using username and password
    arubanetworks.afc.afc_switches:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        operation: "reconcile"
        data:
            switches:
                - "10.10.10.15"
                - "10.10.10.16"
            fabric:
                - "DC-Fabric"

-   name: Reboot a set of switches through AFC using username and password
    arubanetworks.afc.afc_switches:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        operation: "reboot"
        data:
            switches:
                - "10.10.10.15"
                - "10.10.10.16"
            boot_partition: 'active'

-   name: Reboot all switches in Fabric through AFC using username and password
    arubanetworks.afc.afc_switches:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        operation: "reboot"
        data:
            fabric:
                - "DC-Fabric"
            boot_partition: 'non-active'

-   name: Reboot all switches in DC-Fabric and a set of devices using username
    arubanetworks.afc.afc_switches:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        operation: "reboot"
        data:
            switches:
                - "10.10.10.15"
                - "10.10.10.16"
            fabric:
                - "DC-Fabric"
            boot_partition: 'non-active'

-   name: Save configuraton on switches through AFC using username and password
    arubanetworks.afc.afc_switches:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        operation: "save"
        data:
            switches:
                - "10.10.10.15"
                - "10.10.10.16"
            fabric:
                - "DC-Fabric"

-   name: Update switch data on AFC using token
    arubanetworks.afc.afc_switches:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        operation: "update"
        data:
            switches: "10.10.10.15"
            name: "Update_Switch_Name"

-   name: Reconcile switch on AFC using token
    arubanetworks.afc.afc_switches:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        operation: "reconcile"
        data:
            switches:
                - "10.10.10.15"
                - "10.10.10.16"
            fabric:
                - "DC-Fabric"

-   name: Reboot switch through AFC using token
    arubanetworks.afc.afc_switches:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        operation: "reboot"
        data:
            switches:
                - "10.10.10.15"
                - "10.10.10.16"
            fabric:
                - "DC-Fabric"
            boot_partition: 'non-active'

-   name: Save configuraton on switches through AFC using token
    arubanetworks.afc.afc_switches:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        operation: "save"
        data:
            switches:
                - "10.10.10.15"
                - "10.10.10.16"
            fabric:
                - "DC-Fabric"
"""

RETURN = r"""
message:
    description: The output generated by the module
    type: str
    returned: always
    sample: "Successfully completed action"
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
from pyafc.switches import switches


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

        if operation == "update":
            switches_instance = switches.Switch(
                afc_instance.client,
                device=data["switches"],
            )
            message, status, changed = switches_instance.update(data)
        elif operation == "reconcile":
            message, status, changed = switches.Switch.reconcile(
                afc_instance.client,
                data,
            )
        elif operation == "reboot":
            message, status, changed = switches.Switch.reboot(
                afc_instance.client,
                data,
            )
        elif operation == "save":
            message, status, changed = switches.Switch.save_config(
                afc_instance.client,
                data,
            )
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
