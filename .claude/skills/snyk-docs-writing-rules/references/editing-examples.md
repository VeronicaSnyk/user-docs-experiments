# Editing examples: before and after

Full worked examples that show the editing approach across content types. Each pairs a source with the target rewrite. Read the one closest to what you are editing. The principles and a quick transformation table live in `SKILL.md` — these are the detailed models.

Conventions in every target: active voice, second person ("you"), no contractions, no "may/should/might," bold only for UI/CLI/IDE elements and status values (never for list labels), full product name once then "Snyk."

## Contents

1. Procedure
2. Conceptual prose
3. Security topic with states
4. Troubleshooting (restraint)

---

## 1. Procedure

**Source:**
> Configure a Nexus Go registry
>
> If a private or brokered package registry integration is not configured first, the steps below will not work and the registry settings field will not be visible on the page.
>
> First, set up the Nexus integration: go to Organization Settings > Add Integration > Nexus > Edit Settings.
>
> Then, on the Settings > Languages > Go page:
> 1. In the relevant box, Private package registries or Brokered package registries, select Nexus as the registry type.
> 2. In the Registry URL field, enter the full URL of your Nexus Go (`golang`) proxy repository.
> 3. Save the integration.
>
> Snyk authenticates to the registry using the credentials stored in your Nexus integration and you should not enter credentials here.

**Target:**
> ## Configure a Nexus Go registry
>
> Configure a private or brokered package registry integration before proceeding. Without this integration, the registry settings field is not visible, and these steps do not work.
>
> 1. Set up the Nexus integration. Navigate to **Organization Settings > Add Integration > Nexus > Edit Settings**.
> 2. On the **Settings > Languages > Go** page:
>     - In the **Private package registries** or **Brokered package registries** box, select **Nexus** as the registry type.
>     - In the **Registry URL** field, enter the URL of your Nexus Go proxy repository.
> 3. Save the integration.
>
> Snyk authenticates to the registry using credentials from your Nexus integration. You do not enter credentials here.

What changed: the prerequisite became a short lead sentence (no "Before you begin:" label); everything folded into one numbered sequence with the Go-page actions nested as bullets; "box" kept as the real UI label and bolded; words cut for concision ("full URL" → "URL", dropped the "(`golang`)" aside, "the credentials stored in" → "credentials from"); "go to" → "Navigate to" with bold UI paths; present tense ("will not work" → "do not work"); "you should not enter" → "You do not enter" (no "should"); the closing note left as a plain factual statement.

---

## 2. Conceptual prose

The lesson: concision by tightening and splitting, not deleting. Convert passives to active by naming the actor.

**Source:**
> The Universal Broker improves the management of Broker deployments and connections by supporting many connections of any type with a single running client (container) or with multiple client replicas. Credentials remain within your network and are never stored by or transmitted to Snyk. The Snyk platform uses credentials references to instruct the Universal Broker how to authenticate with your private resources.
> Each client or set of client replicas is called a Broker deployment. The diagram below shows two deployments, Universal Broker A and Universal Broker B.
> A deployment can support multiple connections of any type, as shown in the diagram examples: GitHub, GitLab, Artifactory, Jira, and Container Registry Agent. Connections are configured to communicate with specific private resources: SCMs, JIRA, and others.

**Target:**
> Universal Broker simplifies the management of Broker deployments and connections. It supports multiple connections of any type using a single client (container) or multiple client replicas. Credentials remain within your network. Snyk does not store or transmit them. The Snyk platform uses credential references to instruct Universal Broker to authenticate with your private resources.
>
> Snyk refers to each client or set of client replicas as a Broker deployment. The diagram illustrates two deployments: Universal Broker A and Universal Broker B. A deployment supports multiple connections of any type, such as GitHub, GitLab, Artifactory, Jira, and Container Registry Agent. You configure connections to communicate with specific private resources, including SCMs and Jira.

What changed: the dense opening sentence was split into two one-idea sentences, not cut; passives became active ("are never stored by Snyk" → "Snyk does not store or transmit them"; "is called a Broker deployment" → "Snyk refers to … as a Broker deployment"; "Connections are configured" → "You configure connections"); "the diagram below" → "The diagram illustrates" (no spatial reference); "credentials references" → "credential references"; "JIRA" → "Jira"; meaningful content kept. The two sentences "Credentials remain within your network" and "Snyk does not store or transmit them" stay separate sentences — no semicolon (A12).

---

## 3. Security topic with states

The lesson: bold status values (they appear in the UI); convert passives to active; lead with the prerequisite.

**Source:**
> Review pending findings
> The self-review feature in Snyk API & Web gives you visibility and control over findings that are in a Pending Review state. This feature allows you to view and act on pending findings immediately, helping you speed up your security reviews and development workflows.
> Previously, scans containing low-confidence findings were marked as Under Review, and those pending findings remained hidden while awaiting manual verification by the Snyk team.

**Target:**
> ## Review pending findings
>
> Self-review in Snyk API & Web gives you visibility and control over findings in a **Pending Review** state. View and act on pending findings immediately to speed up security reviews and development workflows.
>
> Previously, Snyk marked scans with low-confidence findings as **Under Review** and hid those pending findings until the Snyk team verified them manually.

What changed: status values **Pending Review** and **Under Review** bolded (they appear in the UI); "allows you to view and act… helping you speed up" → "View and act… to speed up" (no "allows you to" capability phrasing); passive "scans were marked… awaiting manual verification" → active "Snyk marked scans… and hid those… until the Snyk team verified them"; full product name "Snyk API & Web" on first mention, then "Snyk."

---

## 4. Troubleshooting (restraint)

The lesson: this content already follows the rules. Fix only genuine errors; do not restructure.

**Source (excerpt):**
> Static analysis limitations
> The following functionality is not supported when using static analysis:
> * Private dependencies: Snyk cannot access private dependencies, including brokered and non-brokered. Transitive dependencies are not resolved.
> * Runtime precision: Snyk cannot reliably identify the specific runtime, which may increase false positives

**Target:**
> ## Static analysis limitations
>
> Static analysis does not support the following:
>
> - Private dependencies: Snyk cannot access private dependencies, brokered or non-brokered. Snyk does not resolve transitive dependencies.
> - Runtime precision: Snyk cannot reliably identify the specific runtime, which can increase false positives.

What changed (only genuine fixes): passive → active ("is not supported when using static analysis" → "Static analysis does not support"; "Transitive dependencies are not resolved" → "Snyk does not resolve transitive dependencies"); "may increase" → "can increase" (no "may"); added the missing terminal period. The list lead-in labels are **not** bolded — they are not UI elements. The rest of the page was left unchanged because it was already clear, active, and concise.
