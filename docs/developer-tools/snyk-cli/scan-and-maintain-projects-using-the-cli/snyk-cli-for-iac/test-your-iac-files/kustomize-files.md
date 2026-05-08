---
description: Scan Kustomize overlays and base configurations for Kubernetes misconfigurations using the Snyk CLI.
---

# Kustomize files

You can scan a Kustomize template by building the Kubernetes manifest file and then scanning it using the Snyk CLI `iac test` command.

```bash
kustomize build > kubernetes.yaml
snyk iac test kubernetes.yaml
```

Depending on your Kustomize templates, you may need to provide a name after the build argument.