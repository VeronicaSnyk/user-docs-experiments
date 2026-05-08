---
description: Configure your Snyk Broker Helm chart to use an existing Kubernetes service account instead of creating a new one.
---

# Service accounts for Helm Chart installation

To use an existing service account, add the following parameters to the install command:

```bash
--set serviceAccount.create=false \
--set serviceAccount.name=<ENTER_EXISTING_SERVICE_ACCOUNT> \
```
