#!/usr/bin/python

# (C) Copyright 2020-2025 Hewlett Packard Enterprise Development LP.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
module: afc_dss
version_added: "0.0.1"
short_description: Create a DSS configuration item.
description: >
    This module creates a DSS configuration item.
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
            Operation to be performed on the DSS configuration,
            create or update (only network).
        type: str
        choices:
            - create
            - delete
            - update
        required: true
    data:
        description: >
            Object specific data for policy, endpoint_group, rule, qualifier
            or network. Structure is provided in the example.
        type: dict
        suboptions:
            name:
                description: DSS Object Name
                type: str
                required: true
            type:
                description: DSS Object type
                type: str
                choices:
                    - network
                    - qualifier
                    - endpoint_group
                    - rule
                    - policy
                required: true
            policy_subtype:
                description: >
                    DSS Policy specific. Subtype
                type: str
                choices:
                    - firewall
                    - layer3
                    - layer2
                required: true
            enforcers:
                description: >
                    DSS Policy specific.
                    Policy Enforcers
                type: list
                elements: dict
                required: false
                suboptions:
                    direction:
                        description: >
                            Apply the policy in this direction on the enforcer
                        type: str
                        choices:
                            - ingress
                            - egress
                        required: true
                    fabric:
                        description: Fabric on which to apply the Policy
                        type: str
                        required: true
                    enforcer_type:
                        description: Type of the enforcer.
                        type: str
                        choices:
                            - network
                            - vrf
                        required: true
                    vrf:
                        description: VRF on which to apply the Policy
                        type: str
                        required: true
                    network:
                        description: Network on which to apply the Policy
                        type: str
                        required: false
            priority:
                description: >
                    DSS Policy specific.
                    Priority is used to determine ordering of Policies
                    applied to the same direction of a specific Enforcer
                type: int
                required: true
            rules:
                description: >
                    DSS Policy specific.
                    List of rules to be used in that policy.
                    Rules order will be used.
                type: list
                elements: str
                required: false
            action:
                description: >
                    DSS Rule specific.
                    Action to be used on that Rule
                type: str
                choices:
                    - allow
                    - drop
                    - reject
                required: false
            source_endpoint_groups:
                description: >
                    DSS Rule specific.
                    List of sources
                type: list
                elements: str
                required: false
            destination_endpoint_groups:
                description: >
                    DSS Rule specific.
                    List of destination
                type: list
                elements: str
                required: false
            service_qualifiers:
                description: >
                    DSS Rule specific.
                    List of qualifiers
                type: list
                elements: str
                required: false
            eg_type:
                description: >
                    Endpoint Group specific.
                    Type of Endpoint Group
                type: str
                choices:
                    - layer3
                    - layer2
                    - firewall
                required: false
            endpoints:
                description: >
                    DSS Endpoint Group specific.
                    List of Endpoint Groups
                type: list
                elements: dict
                required: false
                suboptions:
                    vm_name:
                        description: Name of the VM
                        type: str
                        required: false
                    vnic_name:
                        description: Name of the vNic
                        type: str
                        required: false
                    vmkernel_adapter_name:
                        description: Name of the VMK
                        type: str
                        required: false
                    vm_tag:
                        description: VMs' tag
                        type: str
                        required: false
            protocol_identifier:
                description: >
                    DSS Qualifier specific.
                    List of Qualifiers
                type: list
                elements: dict
                required: false
                suboptions:
                    src_port:
                        description: Source Port
                        type: str
                        required: false
                    dst_port:
                        description: Destination Port
                        type: str
                        required: false
                    ip_protocol:
                        description: IP Protocol
                        type: str
                        required: false
            vlan_id:
                description: >
                    DSS Network specific.
                    VLAN ID to be mapped to the Network
                type: str
                required: true
            service_bypass:
                description: >
                    DSS Network specific.
                    Enable Service Bypass on this Network
                type: str
                required: true
        required: true

author: Aruba Networks (@ArubaNetworks)
"""

EXAMPLES = r"""
-   name: Create policy using username and password using Network
    arubanetworks.afc.afc_dss:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        data:
            name: "test_policy"
            type: "policy"
            policy_subtype: "firewall"
            enforcers:
                - direction: egress
                  fabric: Aruba-Fabric
                  enforcer_type: vrf
                  vrf: Aruba-VRF
                  network: VLAN100
            priority: 1
            rules:
                - DropICMP
                - AllowAll
        operation: "create"

-   name: Create policy using username and password using VRF
    arubanetworks.afc.afc_dss:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        data:
            name: "test_policy"
            type: "policy"
            policy_subtype: "firewall"
            enforcers:
                - direction: egress
                  enforcer_type: vrf
                  fabric: Aruba-Fabric
                  vrf: Aruba-VRF
            priority: 1
            rules:
                - DropICMP
                - AllowAll
        operation: "create"

-   name: Delete policy using username and password
    arubanetworks.afc.afc_dss:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        operation: "delete"
        data:
            name: "test_policy"
            type: "policy"

-   name: Create rule using username and password
    arubanetworks.afc.afc_dss:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        data:
            name: "test_rule"
            type: "rule"
            action: "drop"
            source_endpoint_groups:
                - "test_eg"
            destination_endpoint_groups:
                - "test_eg"
            service_qualifiers:
                - "icmp"
                - "bgp"
                - "test_sq"
        operation: "create"

-   name: Delete rule using username and password
    arubanetworks.afc.afc_dss:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        operation: "delete"
        data:
            name: "test_rule"
            type: "rule"

-   name: Create endpoint group using username and password
    arubanetworks.afc.afc_dss:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        data:
            name: "test_eg"
            type: "endpoint_group"
            eg_type: "layer3"
            endpoints:
                -   vm_name: "VM1"
                    vnic_name: "Network adapter 1"
        operation: "create"

-   name: Delete endpoint group using username and password
    arubanetworks.afc.afc_dss:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        operation: "delete"
        data:
            name: "test_eg"
            type: "endpoint_group"

-   name: Create qualifier using username and password
    arubanetworks.afc.afc_dss:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        data:
            name: "test_sq"
            type: "qualifier"
            qualifier_type: "layer3"
            protocol_identifier:
                -   src_port: "32"
                    dst_port: "32"
                    ip_protocol: "tcp"
        operation: "create"

-   name: Delete qualifier using username and password
    arubanetworks.afc.afc_dss:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        operation: "delete"
        data:
            name: "test_sq"
            type: "qualifier"

-   name: Create network using username and password
    arubanetworks.afc.afc_dss:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        data:
            name: "test_network"
            type: "network"
            fabric: "Aruba-Fabric"
            vrf: "Aruba-VRF"
            vlan_id: 100
            service_bypass: true
        operation: "create"

-   name: Update network using username and password
    arubanetworks.afc.afc_dss:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        data:
            name: "test_network"
            type: "network"
            fabric: "Aruba-Fabric"
            vrf: "Aruba-VRF"
            vlan_id: 1080
            service_bypass: true
        operation: "update"

-   name: Delete network using username and password
    arubanetworks.afc.afc_dss:
        afc_ip: "10.10.10.10"
        afc_username: "afc_admin"
        afc_password: "afc_password"
        data:
            name: "test_network"
            type: "network"
            fabric: "Aruba-Fabric"
            vrf: "Aruba-VRF"
        operation: "delete"

-   name: Create policy using token
    arubanetworks.afc.afc_dss:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        data:
            name: "test_policy"
            type: "policy"
            policy_subtype: "firewall"
            enforcers:
                - direction: egress
                  enforcer_type: vrf
                  fabric: Aruba-Fabric
                  vrf: Aruba-VRF
            priority: 1
            rules:
                - DropICMP
                - AllowAll
        operation: "create"

-   name: Delete policy using token
    arubanetworks.afc.afc_dss:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        operation: "delete"
        data:
            name: "test_policy"
            type: "policy"

-   name: Create rule using token
    arubanetworks.afc.afc_dss:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        data:
            name: "test_rule"
            type: "rule"
            action: "drop"
            source_endpoint_groups:
                - "test_eg"
            destination_endpoint_groups:
                - "test_eg"
            service_qualifiers:
                - "icmp"
                - "bgp"
                - "test_sq"
        operation: "create"

-   name: Delete rule using token
    arubanetworks.afc.afc_dss:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        data:
            name: "test_rule"
            type: "rule"
        operation: "delete"

-   name: Create endpoint group using token
    arubanetworks.afc.afc_dss:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        data:
            name: "test_eg"
            type: "endpoint_group"
            eg_type: "layer3"
            endpoints:
                -   vm_name: "VM1"
                    vnic_name: "Network adapter 1"
        operation: "create"

-   name: Delete endpoint group using token
    arubanetworks.afc.afc_dss:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        operation: "delete"
        data:
            name: "test_eg"
            type: "endpoint_group"

-   name: Create qualifier using token
    arubanetworks.afc.afc_dss:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        data:
            name: "test_sq"
            type: "qualifier"
            qualifier_type: "layer3"
            protocol_identifier:
                -   src_port: "32"
                    dst_port: "32"
                    ip_protocol: "tcp"
        operation: "create"

-   name: Delete qualifier using token
    arubanetworks.afc.afc_dss:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        operation: "delete"
        data:
            name: "test_sq"
            type: "qualifier"

-   name: Create network using token
    arubanetworks.afc.afc_dss:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        data:
            name: "test_network"
            type: "network"
            fabric: "Aruba-Fabric"
            vrf: "Aruba-VRF"
            vlan_id: 1080
            service_bypass: true
        operation: "update"

-   name: Update network using token
    arubanetworks.afc.afc_dss:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        data:
            name: "test_network"
            type: "network"
            fabric: "Aruba-Fabric"
            vrf: "Aruba-VRF"
            vlan_id: 1080
            service_bypass: true
        operation: "update"

-   name: Delete network using token
    arubanetworks.afc.afc_dss:
        afc_ip: "10.10.10.10"
        auth_token: "xxlkjlsdfluwoeirkjlkjsldjjjlkj23423ljlkj"
        data:
            name: "test_network"
            type: "network"
            fabric: "Aruba-Fabric"
            vrf: "Aruba-VRF"
        operation: "delete"
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
from pyafc.dss import endpoint_groups, policies, qualifiers, rules
from pyafc.fabric import fabric
from pyafc.vrf import vrf


def main():
    module_args = {
        "afc_ip": {"type": "str", "required": True},
        "afc_username": {"type": "str", "required": False},
        "afc_password": {"type": "str", "required": False},
        "auth_token": {"type": "str", "required": False},
        "operation": {"type": "str", "required": True},
        "data": {"type": "dict", "required": False},
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

        if operation == "create":
            if data["type"] == "policy":
                policy_instance = policies.Policy(
                    afc_instance.client,
                    name=data["name"],
                )
                message, status, changed = policy_instance.create_policy(
                    **data,
                )
            elif data["type"] == "rule":
                rule_instance = rules.Rule(
                    afc_instance.client,
                    name=data["name"],
                )
                message, status, changed = rule_instance.create_rule(**data)
            elif data["type"] == "endpoint_group":
                eg_instance = endpoint_groups.EndpointGroup(
                    afc_instance.client,
                    **data,
                )
                message, status, changed = eg_instance.create_eg(**data)
            elif data["type"] == "qualifier":
                qualifier_instance = qualifiers.Qualifier(
                    afc_instance.client,
                    **data,
                )
                message, status, changed = qualifier_instance.create_qualifier(
                    **data,
                )
            elif data["type"] == "network":
                fabric_instance = fabric.Fabric(
                    afc_instance.client,
                    name=data["fabric"],
                )
                vrf_instance = vrf.Vrf(
                    afc_instance.client,
                    name=data["vrf"],
                    fabric_uuid=fabric_instance.uuid,
                )
                message, status, changed = vrf_instance.create_network(
                    **data,
                )
        elif operation == "update":
            if data["type"] == "network":
                fabric_instance = fabric.Fabric(
                    afc_instance.client,
                    name=data["fabric"],
                )
                vrf_instance = vrf.Vrf(
                    afc_instance.client,
                    name=data["vrf"],
                    fabric_uuid=fabric_instance.uuid,
                )
                message, status, changed = vrf_instance.update_network(
                    **data,
                )
        elif operation == "delete":
            if data["type"] == "policy":
                policy_instance = policies.Policy(
                    afc_instance.client,
                    **data,
                )
                message, status, changed = policy_instance.delete_policy()
            elif data["type"] == "rule":
                rule_instance = rules.Rule(afc_instance.client, **data)
                message, status, changed = rule_instance.delete_rule()
            elif data["type"] == "endpoint_group":
                eg_instance = endpoint_groups.EndpointGroup(
                    afc_instance.client,
                    **data,
                )
                message, status, changed = eg_instance.delete_eg()
            elif data["type"] == "qualifier":
                qualifier_instance = qualifiers.Qualifier(
                    afc_instance.client,
                    **data,
                )
                message, status, changed = (
                    qualifier_instance.delete_qualifier()
                )
            elif data["type"] == "network":
                fabric_instance = fabric.Fabric(
                    afc_instance.client,
                    **data,
                )
                vrf_instance = vrf.Vrf(
                    afc_instance.client,
                    name=data["vrf"],
                    fabric_uuid=fabric_instance.uuid,
                )
                message, status, changed = vrf_instance.delete_network(
                    **data,
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
