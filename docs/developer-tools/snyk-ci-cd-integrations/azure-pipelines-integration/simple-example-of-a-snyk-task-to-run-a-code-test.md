---
description: Review a minimal YAML example of a Snyk Security Scan task configured to run a Snyk Code test in Azure Pipelines.
---

# Simple example of a Snyk task to run a code test

The following is a simple example of a Snyk task to run a Snyk Code test.

```yaml
- task: SnykSecurityScan@1
  inputs:
    serviceConnectionEndpoint: 'snykToken'
    testType: 'code'
    codeSeverityThreshold: 'medium'
    failOnIssues: true
```