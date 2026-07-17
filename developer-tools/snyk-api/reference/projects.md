# Projects

{% hint style="info" %}
This document uses the REST API. For more details, see the [Authentication for API](../authentication-for-api/) page.
{% endhint %}

For a list of Project types, visit [Project type responses from the API](../api-endpoints-index-and-tips/project-type-responses-from-the-api.md).

## Required permissions

| Operation | Required permissions |
|---|---|
| List projects | `View Organization (org.read)`, `View Projects (org.project.read)` |
| Get a project | `View Organization (org.read)`, `View Projects (org.project.read)` |
| Update a project | `View Organization (org.read)`, `View Projects (org.project.read)`, `Edit Projects (org.project.edit)` |
| Delete a project | `View Organization (org.read)`, `View Projects (org.project.read)`, `Remove Projects (org.project.delete)` |

The `meta.latest_issue_counts` and `meta.latest_dependency_total` query parameters on the list projects endpoint do not require additional permissions beyond `View Projects`.

## Filtering projects

### Tags filter format

Specify tags using the format `key:value` (colon-separated, no spaces around the colon). To require multiple tags to match, pass the `tags` parameter more than once. All specified tags must match (AND logic):

```
GET /orgs/{org_id}/projects?tags=team:backend&tags=env:production&version=2024-10-15
```

### Filter by project status

The REST API does not include a `status` query parameter on `GET /orgs/{org_id}/projects`.

> [!NEEDS INPUT] Confirm whether a `status` or activation-state filter exists for `GET /orgs/{org_id}/projects` — not found in `rest-spec.json`. If unavailable in REST, add a cross-reference to the v1 deactivate endpoint here.

To deactivate a project, use the v1 API. Visit [Deactivating a project (v1 API)](#deactivating-a-project-v1-api).

### Limit values

The `limit` parameter accepts only multiples of 10, from 10 to 100 (for example, 10, 20, 30). The default is 10.

## Setting a project owner

Use `PATCH /orgs/{org_id}/projects/{project_id}` with the `relationships.owner` field. The user must be a member of the same organization as the project. Set `id` to `null` to remove ownership.

You must include both `data.attributes` and `data.relationships` in the request body, even when updating only one of them.

Request body example:

```json
{
  "data": {
    "type": "project",
    "id": "<project_id>",
    "attributes": {},
    "relationships": {
      "owner": {
        "data": {
          "type": "user",
          "id": "<user_public_id>"
        }
      }
    }
  }
}
```

## Deactivating a project (v1 API)

The REST API does not support deactivating a project. Use the v1 API endpoint:

```
POST /org/{orgId}/project/{projectId}/deactivate
```

This endpoint requires no request body. Deactivating a project:

- Disables PR tests for new vulnerabilities.
- Disables Fix PRs for newly disclosed vulnerabilities.
- Disables recurring tests and email alerts.
- Removes webhooks for the repository if no other active projects exist.

Required permissions: `View Organization`, `View Project`, `Project Status`.

## Moving a project to a different organization (v1 API)

The REST API does not include a move endpoint. Use the v1 API endpoint:

```
PUT /org/{orgId}/project/{projectId}/move
```

The API key must have group admin permissions. If moving the project to a new group, use a personal API key.

Request body:

```json
{
  "targetOrgId": "<destination_org_id>"
}
```

Historical reporting data does not move with the project.

## Listing issues for a project

To list issues associated with a project, use `GET /orgs/{org_id}/issues`. Filter by project using the `scan_item_id` and `scan_item_type` query parameters.

Required permissions: `View Organization (org.read)`, `View Projects (org.project.read)`, `View Project history (org.project.snapshot.read)`.

The `include_deactivated` query parameter controls whether disabled issues are included in results.

---

## REST API reference

{% openapi src="../../.gitbook/assets/rest-spec.json" path="/orgs/{org_id}/projects" method="get" %}
[rest-spec.json](../../.gitbook/assets/rest-spec.json)
{% endopenapi %}

{% openapi src="../../.gitbook/assets/rest-spec.json" path="/orgs/{org_id}/projects/{project_id}" method="patch" %}
[rest-spec.json](../../.gitbook/assets/rest-spec.json)
{% endopenapi %}

{% openapi src="../../.gitbook/assets/rest-spec.json" path="/orgs/{org_id}/projects/{project_id}" method="get" %}
[rest-spec.json](../../.gitbook/assets/rest-spec.json)
{% endopenapi %}

{% openapi src="../../.gitbook/assets/rest-spec.json" path="/orgs/{org_id}/projects/{project_id}" method="delete" %}
[rest-spec.json](../../.gitbook/assets/rest-spec.json)
{% endopenapi %}
