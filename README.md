# Ansible Collection - pytoccaz.azure_cli

 Ansible modules wrapping `azure storage blob ` command 

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.13.13**.

<!--end requires_ansible-->

This collection has been tested against [azure cli](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) version **2.52.0**.

## Installation

Azure cli `az` is required on the target machine. 

Download from Galaxy:

```bash
ansible-galaxy collection install pytoccaz.azure_cli
```

## Collection content

<!--start collection content-->
### Modules
Name | Description
--- | ---
[pytoccaz.azure_cli.az_storage_blob_download](https://github.com/pytoccaz/ansible_azure_cli/blob/main/docs/pytoccaz.azure_cli.az_storage_blob_download_module.rst)|Downloads a blob from an azure storage container
[pytoccaz.azure_cli.az_storage_blob_list](https://github.com/pytoccaz/ansible_azure_cli/blob/main/docs/pytoccaz.azure_cli.az_storage_blob_list_module.rst)|Lists blobs under azure storage containers
[pytoccaz.azure_cli.az_storage_blob_upload](https://github.com/pytoccaz/ansible_azure_cli/blob/main/docs/pytoccaz.azure_cli.az_storage_blob_upload_module.rst)|Uploads a blob to an azure storage container

<!--end collection content-->

