# Project Velocity — Sprint 1 Execution Plan

## 1. Sprint Objective
Establish the modernization program's execution rhythm by delivering the first slice of production-ready improvements that unlock secure, observable CI/CD and harden the runtime foundation for subsequent feature expansion. Sprint 1 is time-boxed to two weeks.

## 2. Quantum Backlog Extraction
The following backlog items are decomposed from the Expansion Blueprint's highest priority tracks across Features, Optimization, UI/UX, and Deployment:

| ID | Blueprint Trace | Backlog Item | Definition of Done |
| --- | --- | --- | --- |
| F-1 | Features → Stabilize Foundations → Configuration hardening | Externalize Flask secret key & database URIs to Vault-issued environment variables; update `config.py` and container runtime to consume them. | * `config.py` only reads secrets from environment variables; no random generation.* Vault secret path and retrieval process documented in repo. * Unit tests updated for new configuration expectations. * Configuration docs updated (README + secrets plan).
| O-1 | Optimization → Automate Quality Gates → CI pipeline implementation | Instantiate GitHub Actions workflow from blueprint artifact; ensure lint/test/CodeQL/SAST/container build/SBOM jobs execute successfully against repo. | * `artifacts/ci/github-actions.yml` migrated under `.github/workflows/` and passes dry-run validation.* Pipeline runs on pull request and main.* Bandit SARIF upload and CodeQL exit handling validated via docs.* README gains "CI" badge and contributor instructions.
| U-1 | UI/UX → Observability enablement → Structured logging | Introduce `structlog` based logging wrapper with consistent context for HTTP requests and jobs. | * Logging initialized in Flask app factory.* All blueprints use contextual logger.* Logging docs added to modernization briefing addendum.* Basic unit test verifies request logging middleware.
| D-1 | Deployment → Advanced deployment playbook → Container & release automation | Align Dockerfile and deployment manifests with pipeline outputs, adding SBOM export and ArgoCD hook definitions. | * Dockerfile updated for production WSGI server (Gunicorn) and non-root user.* `k8-deployments.yaml` receives annotations for ArgoCD sync waves and SBOM provenance.* Deployment runbook snippet added to artifacts.* Smoke test script validates container boot.

## 3. Sprint 1 Plan

### 3.1 Sprint Backlog Commitments
1. **Secrets Externalization (F-1)**
   - Implement Vault-backed configuration injection for Flask secrets and database credentials.
   - Update `artifacts/security/secrets-management-plan.md` with operational runbook for dynamic secrets renewal.
   - Regression tests: run existing unit suite and add dedicated config test case.
2. **Pipeline Operationalization (O-1)**
   - Relocate CI workflow into repository `.github/workflows/ci.yml`, referencing CodeQL CLI exit codes guidance to guard failure propagation.
   - Integrate CodeQL troubleshooting best practices to ensure language-specific build steps are conditioned for Python.
   - Configure SARIF uploads for Bandit and CodeQL with artifact retention.
3. **Structured Logging Enablement (U-1)**
   - Introduce logging module, update app factory, and thread contextual logging through key routes.
   - Document logging schema and observability expectations in the briefing and README.
4. **Deployment Alignment (D-1)**
   - Harden Dockerfile with production-grade server and create SBOM artifact stage invoked by pipeline.
   - Update `k8-deployments.yaml` annotations and add ArgoCD promotion steps to deployment docs.

### 3.2 Definition of Done (Per Item)
- **F-1:**
  - Secrets sourced exclusively from Vault-synced environment variables during runtime.
  - Configuration instructions documented; developer setup script or `.env.example` updated with placeholders.
  - Automated tests cover configuration loading; CI green.
- **O-1:**
  - CI workflow executes successfully in test run (manual `act` or GitHub dry run screenshot/log).
  - CodeQL build matrix respects exit codes per GitHub documentation, with failure leading to job failure.
  - SARIF reports uploaded and visible in security tab.
- **U-1:**
  - Logging produces structured JSON with request metadata.
  - Observability docs updated; sample log output included.
  - Unit tests verifying logger middleware.
- **D-1:**
  - Container builds produce SBOM artifact attached to workflow run.
  - Gunicorn-based image passes smoke test (`docker run` health check script).
  - ArgoCD hooks documented and manifests annotated.

### 3.3 Sprint Metrics Target
- **Deployment Frequency:** ≥1 successful pipeline run on main.
- **Lead Time for Change:** Demonstrate end-to-end CI duration under 15 minutes.
- **Change Failure Rate:** 0 failed deployments due to Sprint 1 changes.
- **MTTR:** Document rollback procedure within deployment runbook.

## 4. Sprint Ceremony & Feedback Loop
- **Daily Quantum Standup:** Review telemetry from logging rollout and pipeline health; adjust backlog tasks accordingly.
- **Mid-sprint Review:** Inspect CodeQL scan results for regressions; rerank backlog if vulnerabilities arise.
- **Sprint Review & Demo:** Present running CI pipeline, Vault-injected configuration, structured logging sample, and updated deployment plan.
- **Sprint Retrospective:** Capture learning on CodeQL exit code handling, Vault integration friction, and adjust processes for Sprint 2.

## 5. Observability Hooks for Feedback Loop
- Enable OpenTelemetry exporters alongside structured logging to feed traces to monitoring stack.
- Configure Prometheus scraping for new metrics introduced by logging middleware (request counts, latency buckets).
- Update DORA dashboard to ingest CI run data and pipeline status checks.

## 6. Risks & Mitigations
- **Vault Availability Risk:** Mitigate with local development fallback using sealed secret injection for tests.
- **Pipeline Flakiness:** Utilize GitHub CLI dry runs and caching strategy to reduce runtime volatility.
- **Logging Overhead:** Benchmark request latency before/after instrumentation; optimize formatter if regression >5%.

## 7. Sprint 1 Exit Criteria
- All backlog items meet Definition of Done.
- No Sev-1/Sev-2 incidents introduced by Sprint changes.
- DORA metrics dashboard reflects new pipeline data.
- Product owner sign-off on structured logging output and deployment runbook.

## 8. Next Steps Preparation
- Groom follow-up backlog for probabilistic visit anomaly detection and contextual bandits based on Sprint 1 telemetry.
- Draft Spike stories for integrating Trivy scans and Bayesian maintenance forecasting in Sprint 2.

