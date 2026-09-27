# Contributing to the workshop

Keep the participant path UI-led and the facilitator preparation separate. Every runnable module needs an objective, prerequisites/opening state, console actions, expected evidence, customer value, fallback, checkpoint and cleanup boundary. Cloud provisioning is a planned CAPA/CAPZ extension; do not add executable ROSA instructions in this revision.

Use Antora xrefs and attributes for reusable names. Add complete, nonsecret YAML to attachments only when participants need it. Explain exactly which cluster and namespace receive it. Declare cluster-scoped changes. Never include real kubeconfigs, tokens, generated Secrets, cloud credentials or a personalized profile.

Validate source with `npm run check`, build with `npm run build`, and check output with `python3 tools/check-site.py`. Inspect the rendered page in a browser. For a functional change, record the tested versions, actual observed result and cleanup in the acceptance page. A passing site build is not a live-cluster test.

Keep the public application source in `rh-aelgendy/acm-applications-demo`. The facilitator implementation currently remains in the original presenter repository; do not describe a fresh-fleet installer as complete until it is shareable and passes the documented acceptance gates. Existing presenter guides are a separate maintained artifact.
