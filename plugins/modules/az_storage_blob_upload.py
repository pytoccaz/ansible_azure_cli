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
module: az_storage_blob_upload
author: "Olivier Bernard (@pytoccaz)"
short_description: Uploads a blob to an azure storage container
description:
  - Uploads a blob to an azure storage container with the C(az storage blob upload) command

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
    name:
        description:
            - The blob name to upload
        required: true
        type: str
        aliases:
            - blob
            - blob_name
    file:
        description:
            - Path of the file to upload as the blob content
        required: true
        type: str
        aliases:
            - output
            - output_file
    chgdir:
        description:
            - If given, working directory to run the command inside
        type: str
        aliases:
            - change_directory
            - change_dir
            - wkdir
            - working_directory
            - working_dir
            - output_directory
            - output_dir
    overwrite:
        description:
            - Whether the blob to be uploaded should overwrite the current data
        default: false
        type: bool
'''

RETURN = '''
result:
    description: |
        A blob dictionary
    sample:
        client_request_id: "adc084ac-937f-11ee-b470-5bde3ad7bd9d"
        content_md5: "Dyc9lNk7qLvLcPCC0kJe5g=="
        date: "2023-12-05T15:05:09+00:00"
        encryption_key_sha256: null
        encryption_scope: null
        lastModified: "2023-12-05T15:05:10+00:00"
        request_id: "a8baa9b1-001e-0068-6b8c-27e634000000"
        request_server_encrypted: true
        version: "2022-11-02"
        version_id: null
    returned: success
    type: dict
'''

EXAMPLES = '''
- name: Upload NOTICE file to test container
  pytoccaz.azure_cli.az_storage_blob_upload:
    container: test
    account_name: account000
    blob_name: NOTICE.txt
    output_file: NOTICE.txt
  register: command
'''
import json
from ansible.module_utils.basic import AnsibleModule


def parse_output(data):
    return json.loads(data)


def az_storage_upload(module):

    az_bin = module.get_bin_path("az", required=True)

    command = [az_bin, "storage", "blob", "upload",
               "--no-progress", "--only-show-errors"]

    command.append(
        "--container-name={0}".format(module.params["container_name"]))
    command.append("--name={0}".format(module.params["name"]))
    command.append("--file={0}".format(module.params["file"]))

    if module.params["account_name"] is not None:
        command.append(
            "--account-name={0}".format(module.params["account_name"]))

    if module.params["blob_endpoint"] is not None:
        command.append(
            "--blob-endpoint={0}".format(module.params["blob_endpoint"]))

    if module.params["account_key"] is not None:
        command.append(
            "--account-key={0}".format(module.params["account_key"]))

    if module.params["connection_string"] is not None:
        command.append(
            "--connection-string={0}".format(module.params["connection_string"]))

    if module.params["overwrite"] is True:
        command.append("--overwrite")

    rc, out, err = module.run_command(command, cwd=module.params["chgdir"])

    return rc, out.strip(), err.strip()


def main():
    module = AnsibleModule(
        argument_spec=dict(
            container_name=dict(required=True, type="str",
                                aliases=["container"]),
            account_key=dict(required=False, type="str", aliases=["key"], no_log=True),
            connection_string=dict(required=False, type="str"),
            account_name=dict(required=False, type="str", aliases=["account"]),
            blob_endpoint=dict(required=False, type="str",
                               aliases=["endpoint"]),
            name=dict(required=True, type="str",
                      aliases=["blob", "blob_name"]),
            file=dict(required=True, type="str",
                      aliases=["output", "output_file"]),
            overwrite=dict(default=False, type="bool"),
            chgdir=dict(required=False, type="str", aliases=["change_directory", "change_dir", "wkdir",
                                                             "working_directory", "working_dir",
                                                             "output_directory", "output_dir"]),
        ),
        mutually_exclusive=[("account_name", "blob_endpoint"),
                            ("account_key", "connection_string")],
        supports_check_mode=True
    )

    result = dict(
        changed=False,
        result=dict()
    )

    if module.check_mode:
        module.exit_json(**result)

    rc, out, err = az_storage_upload(module)

    if rc != 0:
        module.fail_json(msg="Error running az storage blob upload. {0}".format(err),
                         rc=rc, stdout=out, stderr=err)
    else:
        ret = parse_output(out)

    module.exit_json(
        changed=True,
        rc=rc,
        stdout=out,
        stderr=err,
        result=ret
    )


if __name__ == "__main__":
    main()
