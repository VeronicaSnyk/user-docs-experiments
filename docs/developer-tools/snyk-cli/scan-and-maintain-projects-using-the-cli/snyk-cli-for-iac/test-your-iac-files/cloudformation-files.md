---
description: Scan AWS CloudFormation templates for security misconfigurations using the Snyk CLI.
---

# CloudFormation files

With Snyk Infrastructure as Code, you can test your CloudFormation files using the CLI. You can test files in both YAML and JSON formats. You can also scan AWS CDK applications; see [AWS CDK files](aws-cdk-files.md).

Test for an issue in specified files using the following command:

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