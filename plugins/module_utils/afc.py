#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (C) Copyright 2020-2025 Hewlett Packard Enterprise Development LP.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

try:
    from pyafc.afc import afc

    HAS_PYAFC = True
    PYAFC_IMPORT_ERROR = None
except ImportError as import_error:
    HAS_PYAFC = False
    PYAFC_IMPORT_ERROR = import_error


def instantiate_afc_object(data=None):
    afc_instance = afc.Afc(data=data)
    return afc_instance


def afc_argument_spec():
    """Return the argument_spec entries shared by every AFC resource module."""
    return {
        "afc_ip": {"type": "str", "required": True},
        "afc_username": {"type": "str", "required": False},
        "afc_password": {"type": "str", "required": False, "no_log": True},
        "auth_token": {"type": "str", "required": False, "no_log": True},
        "disable_tls_verification": {
            "type": "bool",
            "required": False,
            "default": False,
        },
    }


def build_auth_data(ansible_module):
    """Build the pyafc authentication data from a module's parameters.

    Uses the auth_token when provided, otherwise falls back to the
    username/password pair, and always threads the TLS verification flag
    (verify=True unless disable_tls_verification is set).
    """
    params = ansible_module.params
    token = params.get("auth_token")
    if token is not None:
        auth_data = {"ip": params["afc_ip"], "auth_token": token}
    else:
        auth_data = {
            "ip": params["afc_ip"],
            "username": params["afc_username"],
            "password": params["afc_password"],
        }
    auth_data["verify"] = not params["disable_tls_verification"]
    return auth_data
