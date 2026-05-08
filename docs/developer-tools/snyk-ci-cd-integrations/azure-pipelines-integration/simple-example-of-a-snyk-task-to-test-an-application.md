---
description: Review a minimal YAML example of a Snyk Security Scan task configured to test open-source dependencies in Azure Pipelines.
---

# Simple example of a Snyk task to test an application

The following is a simple example of a Snyk task to test an application's open-source dependencies (SCA).

```yaml
- task: SnykSecurityScan@1
  inputs:
    serviceConnectionEndpoint: 'snykToken'
    testType: 'app'
    monitorWhen: 'always'
    failOnIssues: true
```