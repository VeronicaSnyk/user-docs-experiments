import re
from pathlib import Path
f = "docs/developer-tools/snyk-ci-cd-integrations/terraform-cloud-integration-for-snyk-iac-using-run-tasks/set-up-the-terraform-cloud-integration-for-iac.md"
content = open(f).read()
IMAGE_MD_RE = re.compile(r'!\[[^\]]*\]\(<([^>]+)>|!\[[^\]]*\]\(([^)<>][^)]*)\)')
SRC_RE = re.compile(r'src=["\']([^"\']+)["\']')
print("MD matches:")
for m in IMAGE_MD_RE.finditer(content):
    print(" g1:", repr(m.group(1)), "g2:", repr(m.group(2)))
print("SRC matches:")
for m in SRC_RE.finditer(content):
    print(" ", repr(m.group(1)))
