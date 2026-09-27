# ACM Fleet Operations workshop

An Antora/AsciiDoc participant guide using the same versioned Showroom theme as [Snakewell](https://github.com/rh-mobb/snakewell). Existing presenter guides and live cluster resources remain in the separate ACM demo repository. This is a draft for fresh-environment acceptance, not a universal installer.

## Read and build

Use an active Node.js LTS and npm, plus Python 3. From this directory:

```sh
npm ci
npm run check
npm run build
npm run preview
```

Open `http://localhost:8088`. Build output is `www/`; it contains only the curated guide and attachments. Antora 3.1.10 is pinned to match the reference workshop build. The Showroom UI bundle is pinned to release `v0.0.1`; the first build needs access to GitHub. No live cluster access is used by the build.

For environment-specific instructions:

```sh
python3 tools/configure.py
npm exec -- antora --log-failure-level warn antora.local.yml
npm run preview
```

The questionnaire accepts nonsecret names/URLs only, writes ignored local files, and does **not** configure or deploy the demo. For repeatable input use `--profile /path/to/profile.json`; add `--validate` for a read-only check. Do not publish a locally personalized build unless its names/URLs are intended for that audience. Generic builds intentionally use placeholders.

## Structure and authoring

- `content/antora.yml`: reusable environment attributes and component metadata.
- `content/modules/ROOT/pages/`: welcome, modules 0–10 and facilitator appendices.
- `content/modules/ROOT/nav.adoc`: sidebar and pagination order.
- `content/modules/ROOT/partials/`: shared environment and console guidance.
- `content/modules/ROOT/attachments/`: curated complete YAML examples; no generated credentials.
- `tools/configure.py`: document-only environment questionnaire.
- `tools/check-content.py`: local cross-reference, attachment and structure checks.
- `antora-playbook.yml`: standalone static site with the Showroom theme.
- `ui-config.yml`: future Showroom host integration metadata, with no embedded terminals configured.

Each executable module must state objective/time/starting state, actual console actions, expected evidence, value, fallback, checkpoint and cleanup. Use attributes for cluster identities and namespaces. Keep scripts in facilitator preparation, not as the customer-facing proof. Include complete YAML when users are asked to import it; clearly identify fragments as edits to an existing object. Never infer AKS/provider support from Kubernetes API similarity.

Module 9 is a **CAPA/CAPZ provisioning placeholder** by request. ROSA-specific procedures are intentionally excluded; existing legacy ROSA guides are untouched.

## Publication and acceptance

The guide is built locally first. No public Pages site is enabled automatically, and the private presenter repository is not a runtime dependency for the public GitOps apps. Publish only the `www/` output after review, or host this repository with GitHub Pages. Do not upload the whole presenter checkout or ignored local profiles.

Fresh-environment preparation still needs validation and generalization; the questionnaire does not solve every installer assumption. The Environment setup, Compatibility and Acceptance pages enumerate those gates. The original repository’s `docs/` remains the current-fleet operational reference; new portable workshop editorial changes belong here. Review both guides when the underlying demo behavior changes.

## Reference

Format inspiration: Snakewell public source, inspected 2026-09-27. We reuse its Antora/Showroom conventions, not its application or exploit content. The external theme retains its own license. This community workshop is not an assertion of Red Hat certification.
