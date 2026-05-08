---
description: Route your Snyk Broker Helm deployment through an HTTP or HTTPS proxy by setting the proxy environment variables.
---

# Proxy settings for Broker Helm chart installation

To use the Helm chart behind a proxy, set the `httpProxy` and `httpsProxy` values.

```bash
--set httpsProxy=<PROXY_URL>
```
