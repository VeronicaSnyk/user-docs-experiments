---
description: Disable TLS certificate verification in your Snyk Broker Docker container to support self-signed certificates.
---

# Disable certificate verification with Docker

To disable certificate verification, for example, in the case of self-signed certificates, add the following to the docker run command:

```bash
-e NODE_TLS_REJECT_UNAUTHORIZED=0
```
