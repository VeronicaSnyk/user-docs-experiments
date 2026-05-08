---
description: Test Kubernetes manifest files for security misconfigurations using the Snyk CLI.
---

# Kubernetes files

With Snyk Infrastructure as Code, you can test your configuration files with the CLI. Snyk Infrastructure as Code for Kubernetes supports the following:

* Deployments, Pods, and Services
* CronJobs, Jobs, StatefulSet, ReplicaSet, DaemonSet, and ReplicationController

Use the following Snyk CLI command to test for an issue on specified files:

```bash
snyk iac test
```

Example:

```bash
snyk iac test deploy.yaml
```

You can also specify multiple files by appending the file names after each other, for example:

```bash
snyk iac test file-1.yaml file-2.yaml
```

For the steps to scan a Helm chart using the Snyk CLI, see [Helm charts](helm-charts.md).

For the steps to scan a Kustomize template using the Snyk CLI, see [Kustomize files](kustomize-files.md).