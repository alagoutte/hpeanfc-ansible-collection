#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (C) Copyright 2020-2025 Hewlett Packard Enterprise Development LP.
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

REQUESTS_IMP_ERR = None

from pyafc.afc import afc


def instantiate_afc_object(data=None):
    afc_instance = afc.Afc(data=data)
    return afc_instance
