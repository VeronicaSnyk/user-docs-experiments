---
description: >-
  Build a custom rules bundle from your Rego rules using the snyk-iac-rules SDK build command.
---

# Bundling rules

When you are ready, you can **build a custom rules bundle** by running the following command:

```bash
snyk-iac-rules build
```

If you have more than your generated rules in the current folder, consider using the `--ignore` option to exclude the folders and files irrelevant to a production-ready bundle. This can both speed up the process and ensure the size of the generated bundle stays small.

You can override the default entry point. If you have chosen to name the rule that evaluates something different from **`deny`**, for example, `allow`,`violation`and so on, you can override it by running:

```bash
snyk-iac-rules build --entrypoint "<package name>/<function name>"
```

Finally, you can check the contents of the bundle without extracting it by running:

```bash
tar -tf bundle.tar.gz
```

The output will be all the files included in the bundle:

```text
/data.json
/lib/main.rego
/rules/MY_RULE/main.rego
/policy.wasm
/.manifest
```

You can now [run snyk iac test with your newly built custom bundle.](../use-iac-custom-rules-with-cli/)
