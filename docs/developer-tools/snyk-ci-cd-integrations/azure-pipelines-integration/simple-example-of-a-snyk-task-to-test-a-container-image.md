---
description: Review a minimal YAML example of a Snyk Security Scan task configured to test a container image in Azure Pipelines.
---

# Simple example of a Snyk task to test a container image

The following is a simple example of a Snyk task to test a container image.

```yaml
- task: SnykSecurityScan@1
  inputs:
    serviceConnectionEndpoint: 'snykToken'
    testType: 'container'
    dockerImageName: 'goof'
    dockerfilePath: 'Dockerfile'
    monitorWhen: 'always'
    failOnIssues: true
```