# HPE Aruba Networking Fabric Composer — Ansible collection docs

Reference documentation for every module of the `arubanetworks.afc`
collection. Each page is generated from the module's own `DOCUMENTATION`
and `EXAMPLES`, so it always reflects the real, supported argument spec.

## Standard playbook format

Almost every module (except `afc_session`) follows the same calling
convention:

- Connection is done either with `afc_username` / `afc_password`, **or** by
  re-using an `auth_token` obtained from `afc_session`.
- The action is selected with the top-level `operation` key
  (for example `create`, `update`, `assign`, `delete`).
- The object configuration goes into the top-level `data` dictionary.
  When a module manages several object kinds, `data.type` selects the kind.
- `disable_tls_verification: true` is required when AFC uses a self-signed
  certificate. It must be set on **every** task that talks to AFC, not only
  on the `afc_session` task.

> Common mistake: passing object fields (such as `fabric`, `vlan_id`,
> `type`) at the task top level. They must be nested under `data`.

### Recommended pattern — one session re-used by all tasks

```YAML
- name: Configure AFC
  hosts: localhost
  gather_facts: false
  vars:
    afc_ip: "10.10.10.10"
  tasks:
    - name: Open a session and capture the auth_token
      arubanetworks.afc.afc_session:
        afc_ip: "{{ afc_ip }}"
        afc_username: "admin"
        afc_password: "password"
        disable_tls_verification: true
      register: reg_afc_session

    - name: Create VLANs and assign them to devices
      arubanetworks.afc.afc_vlan:
        afc_ip: "{{ afc_ip }}"
        auth_token: "{{ reg_afc_session.auth_token }}"
        disable_tls_verification: true
        operation: create
        data:
          type: vlan
          fabric: DC1
          vlan_id: "100,200-202"
          vlan_name: Production
          switches:
            - Leaf-1
            - Leaf-2
```

### Alternative — standalone task with username and password

```YAML
- name: Create VLANs (no shared session)
  arubanetworks.afc.afc_vlan:
    afc_ip: "10.10.10.10"
    afc_username: "admin"
    afc_password: "password"
    disable_tls_verification: true
    operation: create
    data:
      type: vlan
      fabric: DC1
      vlan_id: "100"
      switches:
        - Leaf-1
```

> When re-using an `auth_token`, do not also pass `afc_username` /
> `afc_password`: the session would be closed after the task.

## Modules

### Session and system

- [afc_session](afc_session.md) — open/close a session, capture `auth_token`
- [afc_licenses](afc_licenses.md) — manage licenses
- [afc_cli](afc_cli.md) — run CLI commands
- [afc_integrations](afc_integrations.md) — third-party integrations (vSphere, PSM)

### Fabric, underlay and overlay

- [afc_fabric](afc_fabric.md) — create fabrics and assign switches/roles
- [afc_multifabrics](afc_multifabrics.md) — multi-fabric configuration
- [afc_discovery](afc_discovery.md) — device discovery
- [afc_leaf_spine](afc_leaf_spine.md) — leaf/spine configuration
- [afc_underlay](afc_underlay.md) — underlay configuration
- [afc_overlay](afc_overlay.md) — overlay configuration
- [afc_evpn](afc_evpn.md) — EVPN configuration
- [afc_evpn_settings](afc_evpn_settings.md) — global (fabric-wide) EVPN settings
- [afc_vsx](afc_vsx.md) — VSX configuration

### Switches and interfaces

- [afc_switches](afc_switches.md) — switch configuration
- [afc_ports](afc_ports.md) — port configuration
- [afc_physical_interfaces](afc_physical_interfaces.md) — physical interfaces
- [afc_lag_interfaces](afc_lag_interfaces.md) — LAG interfaces

### Layer 2

- [afc_vlan](afc_vlan.md) — VLANs, VLAN groups and stretched VLANs
- [afc_stp](afc_stp.md) — spanning-tree configuration

### Layer 3 and routing

- [afc_vrf](afc_vrf.md) — VRF configuration
- [afc_vrf_bgp](afc_vrf_bgp.md) — BGP configuration in a VRF
- [afc_ip_interface](afc_ip_interface.md) — IP interfaces
- [afc_ospf](afc_ospf.md) — OSPF configuration
- [afc_route_policy](afc_route_policy.md) — route maps and prefix/AS-path/community lists

### Network services

- [afc_dns](afc_dns.md) — DNS configuration
- [afc_ntp](afc_ntp.md) — NTP configuration
- [afc_dhcp_relay](afc_dhcp_relay.md) — DHCP relay configuration
- [afc_snmp](afc_snmp.md) — SNMP configuration
- [afc_syslog](afc_syslog.md) — Syslog configuration
- [afc_sflow](afc_sflow.md) — sFlow configuration
- [afc_aaa](afc_aaa.md) — AAA/RADIUS configuration
- [afc_remote_file_server](afc_remote_file_server.md) — Remote File Transfer Server (SFTP/SCP) configuration

### Policy and resources

- [afc_dss](afc_dss.md) — distributed security (DSS) policies
- [afc_resource_pool](afc_resource_pool.md) — resource pools

### Sample variables

- [afc_sample_vars](afc_sample_vars.md) — example variable files
