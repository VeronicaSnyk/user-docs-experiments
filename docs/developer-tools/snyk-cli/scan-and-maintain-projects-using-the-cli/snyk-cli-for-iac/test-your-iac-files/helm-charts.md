---
description: Test Helm chart templates for Kubernetes misconfigurations using the Snyk CLI.
---

# Helm charts

You scan a Helm chart by rendering the Helm templates into Kubernetes manifest files and then scanning these using the Snyk CLI `snyk iac` command.

For example, if you have a Helm Project located in a `./helm` directory, you would run the following command to output the templated files into a directory called `./output`:

{% tabs %}
{% tab title="macOS/Linux/Unix" %}
```bash
helm template ./helm --output-dir ./output
snyk iac test ./output
```
{% endtab %}

{% tab title="Windows PowerShell" %}
```bash
helm template .\helm\ --output-dir .\output\
snyk iac test .\output\
```
{% endtab %}
{% endtabs %}

For Unix-based terminals, you can also pipe the output of `helm template` directly into a single file:

```bash
helm template ./helm > output.yaml
snyk iac test output.yaml
```

The Snyk CLI cannot read from standard input at this time; Snyk is working on this feature.