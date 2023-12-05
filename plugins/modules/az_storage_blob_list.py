#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2023 Olivier Bernard (@pytoccaz)
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# Credits: Jose Angel Munoz (@imjoseangel) for his module community.docker.docker_stack_info.py of which this programm is an adaptation

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = '''
---
module: az_storage_blob_list
author: "Olivier Bernard (@pytoccaz)"
short_description: Lists blobs under azure storage containers
description:
  - Lists blobs under azure storage containers using the C(az storage blob list) command

version_added: 1.0.0

options:
    account_name:
        description:
            - Storage account name
        type: str
        aliases:
            - account
    blob_endpoint:
        description:
            - Storage data service endpoint. Must be used in conjunction with storage account key
        type: str
        aliases:
            - endpoint
    account_key:
        description:
            - Storage account key
        type: str
        aliases:
            - key
    connection_string:
        description:
            - Storage account connection string
        type: str
    container_name:
        description:
            - The container name
        required: true
        type: str
        aliases:
            - container
    prefix:
        description:
            - Filter the results to return only blobs whose name begins with the specified prefix
        type: str
'''

RETURN = '''
results:
    description: |
        A List of blobs dictionary
    sample:
        - container: "backups"
          name: "test.tar.gz"
          creationTime: "2023-12-04T23:00:05+00:00"
    returned: success
    type: list
    elements: dict
'''

EXAMPLES = '''
- name: List blobs containers inside backups
  pytoccaz.azure_cli.az_storage_blob_list:
    container: backups
  register: blobs_list
'''
from ansible.module_utils.basic import AnsibleModule
import json


def parse_output(data):
    return json.loads(data)


def az_storage_list(module):

    az_bin = module.get_bin_path("az", required=True)

    command = [az_bin, "storage", "blob", "list", "--only-show-errors"]

    command.append("--container-name={0}".format(module.params["container_name"]))

    if module.params["account_name"] is not None:
        command.append("--account-name={0}".format(module.params["account_name"]))

    if module.params["blob_endpoint"] is not None:
        command.append("--blob-endpoint={0}".format(module.params["blob_endpoint"]))

    if module.params["account_key"] is not None:
        command.append("--account-key={0}".format(module.params["account_key"]))

    if module.params["connection_string"] is not None:
        command.append("--connection-string={0}".format(module.params["connection_string"]))

    if module.params["prefix"] is not None:
        command.append("--prefix={0}".format(module.params["prefix"]))

    rc, out, err = module.run_command(command)

    return rc, out.strip(), err.strip()


def main():
    module = AnsibleModule(
        argument_spec=dict(
            container_name=dict(required=True, type="str", aliases=["container"]),
            account_key=dict(required=False, type="str", aliases=["key"], no_log=True),
            connection_string=dict(required=False, type="str"),
            account_name=dict(required=False, type="str", aliases=["account"]),
            blob_endpoint=dict(required=False, type="str", aliases=["endpoint"]),
            prefix=dict(required=False, type="str"),
        ),
        mutually_exclusive=[("account_name", "blob_endpoint"), ("account_key", "connection_string")],
        supports_check_mode=True
    )

    rc, out, err = az_storage_list(module)

    if rc != 0:
        module.fail_json(msg="Error running az storage blob list. {0}".format(err),
                         rc=rc, stdout=out, stderr=err)
    else:
        if out:
            ret = parse_output(out)

        else:
            ret = []

    module.exit_json(
        changed=False,
        rc=rc,
        stdout=out,
        stderr=err,
        results=ret
    )


if __name__ == "__main__":
    main()
