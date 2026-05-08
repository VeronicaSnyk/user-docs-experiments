---
description: Disable TLS verification or provide a custom CA certificate to troubleshoot SSL issues in your Snyk Broker Helm installation.
---

# Parameters for troubleshooting and providing your own certificate with Helm

To troubleshoot SSL inspection issues, you can set the `tlsRejectUnauthorized` parameter to `disable`.

```bash
--set tlsRejectUnauthorized=disable
```

To trust your own Certificate Authority, you can pass a certificate file name to the `caCert` parameter. The file must reside within the Helm chart directory.

```bash
--set caCert=<CERT_NAME>
```

Alternatively, provide the content of the certificate to the `caCertFile` parameter.

```bash
--set caCertFile="-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----"
```

To troubleshoot CA trust issues, you can set the `disableCaCertTrust` parameter to `true`.

```bash
--set disableCaCertTrust=true
```

If you want your Broker to run as an HTTPS server, you can pass the files to the `httpsCert` and `httpsKey` parameters. The files must reside within the Helm chart directory.

```bash
--set httpsCert=<CERT_NAME> --set httpsKey=<CERT_KEY>
```

For more information about using your own certificate, see [Backend requests with an internal certificate for Docker](../advanced-configuration-for-snyk-broker-docker-installation/backend-requests-with-an-internal-certificate-for-docker.md) and [HTTPS for Broker Client with Docker](../../../https-for-broker-client-with-docker.md).
