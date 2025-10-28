# Senior Architect's Modernization Briefing

## 1. Current State Assessment (Phase 1)

### Architectural Overview
- The platform is a Flask-based monolith that exposes blueprints for authentication and core workflows, backed by SQLAlchemy and Flask-Migrate with PostgreSQL targeted for production and SQLite for development. 【F:README.md†L8-L119】
- Application factories initialize multiple extensions (login, CSRF, mail, limiter, Talisman) and register blueprints, reflecting a modular but tightly coupled service. 【F:app/__init__.py†L16-L83】

### Identified Architectural Entanglements
- Configuration relies on environment selection but embeds a randomly generated `SECRET_KEY` per boot, preventing stateless scaling and causing session invalidation on restarts. Database URIs are hard-coded to SQLite defaults. 【F:config.py†L7-L21】
- `run.py` starts the development server with `debug=True` on all hosts, risking exposure of the debugger and bypassing production-grade WSGI servers. 【F:run.py†L1-L9】
- Maintenance and visit-tracking logic blend view rendering, cookie management, and database writes within a single route, making it difficult to isolate business rules for testing and extension. 【F:app/main/routes.py†L1-L154】

### Tooling, Testing & Automation
- Tests exist for models and visit tracking, but there is no continuous integration workflow beyond Dependabot auto-merge verification; application migrations are not validated in automation. 【F:tests/test_app.py†L1-L126】【F:.github/workflows/dependabot-auto-merge.yml†L1-L37】
- Dependency management relies on a pinned `requirements.txt`, yet the repository stores an `outdated_packages.json` indicating unresolved upgrade debt. 【F:outdated_packages.json†L1-L1】
- No evidence of automated linting, coverage reporting, or artifact generation in CI.

### Security Posture
- Flask-Limiter and Talisman are initialized, but secrets are generated at runtime instead of sourced from a managed store, and there is no CODEOWNERS or branch protection policy in the repo.
- Debug mode in production entry point increases risk; there is no automation to enforce signed commits or SAST scans.

### Observability & Operations
- Logging strategy is unspecified; no structured logging, metrics, or tracing instrumentation is present.
- Docker and docker-compose definitions exist, but there is no deployment automation or SBOM generation.

### Probabilistic Logic Opportunities (Doctrine Mapping Section 3)
1. **Visit Leaderboard Intelligence:** Replace deterministic visit increments with an Exponentially Weighted Moving Average to detect anomalous surges and throttle abusive patterns.
2. **Role-Based Dashboard Recommendations:** Apply a contextual multi-armed bandit to recommend task modules for workers, balancing exploration of new workflows with exploitation of known productivity boosters.
3. **Maintenance Window Forecasting:** Introduce Bayesian change-point detection on historical maintenance logs to predict optimal downtime windows and surface alerts.

## 2. Modernization Roadmap (Phase 3)

1. **Stabilize Foundations (Weeks 1-2)**
   - Adopt ADR-001 to formalize modernization governance and socialize doctrine across teams. 【F:artifacts/governance/ADR-001-adopt-modernization-framework.md†L1-L13】
   - Replace runtime secret generation with Vault-provisioned configuration; refactor `config.py` to consume environment variables issued via the secrets management plan. 【F:artifacts/security/secrets-management-plan.md†L1-L33】
   - Update `run.py`/deployment entry points to use Gunicorn or the containerized stack defined in Dockerfile.

2. **Automate Quality Gates (Weeks 2-4)**
   - Implement the GitHub Actions pipeline delivering lint, test, SAST, CodeQL, container build, SBOM, and ArgoCD deployment triggers. 【F:artifacts/ci/github-actions.yml†L1-L126】
   - Enforce branch protection and CODEOWNERS to guarantee reviewed, tested merges. 【F:artifacts/security/CODEOWNERS†L1-L21】【F:artifacts/security/branch-protection-rules.md†L1-L28】
   - Integrate Codecov and Bandit reports into PR checks; configure Dependabot to respect new checks before auto-merge.

3. **Embed Observability & Metrics (Weeks 4-6)**
   - Add structured logging via Python's `structlog`, instrument key endpoints with OpenTelemetry traces, and publish Prometheus metrics for visit counts and maintenance health.
   - Stand up DORA metrics workflow and dashboard to establish delivery baselines and track modernization progress. 【F:artifacts/governance/dora-metrics-plan.md†L1-L24】

4. **Advance Security & Resilience (Weeks 6-8)**
   - Complete Vault integration, rotate all credentials, and configure automated secret scanning push protection.
   - Extend CI with container vulnerability scanning (Grype/Trivy) and IaC scanning for `k8-deployments.yaml`.
   - Conduct STRIDE threat modeling sessions quarterly and codify mitigations.

5. **Evolve Business Logic (Weeks 8-12)**
   - Extract visit-tracking logic into a dedicated service module with probabilistic anomaly detection.
   - Prototype contextual bandit recommendations for worker dashboards leveraging historical task completion data.
   - Implement Bayesian maintenance forecasting and expose results through observability dashboards.

6. **Continuous Governance (Ongoing)**
   - Maintain ADR log for future architectural decisions.
   - Review branch protection effectiveness and update CODEOWNERS as team structure evolves.
   - Iterate on DORA targets and ensure retrospectives reference measured outcomes.

## 3. Phase 2 Artifacts Directory

All generated modernization assets reside in `artifacts/`:

- `artifacts/ci/github-actions.yml` – Multi-stage CI/CD pipeline with linting, testing, SAST, CodeQL, container build, SBOM, and deployment trigger. 【F:artifacts/ci/github-actions.yml†L1-L126】
- `artifacts/security/CODEOWNERS` – Ownership map enforcing accountable reviews. 【F:artifacts/security/CODEOWNERS†L1-L21】
- `artifacts/security/branch-protection-rules.md` – Branch protection guardrails. 【F:artifacts/security/branch-protection-rules.md†L1-L28】
- `artifacts/security/secrets-management-plan.md` – HashiCorp Vault rollout plan. 【F:artifacts/security/secrets-management-plan.md†L1-L32】
- `artifacts/governance/ADR-001-adopt-modernization-framework.md` – Governance decision record. 【F:artifacts/governance/ADR-001-adopt-modernization-framework.md†L1-L13】
- `artifacts/governance/dora-metrics-plan.md` – Implementation strategy for DORA metrics. 【F:artifacts/governance/dora-metrics-plan.md†L1-L24】

These artifacts operationalize the Senior Developer Modernization Framework and provide the launchpad for execution.
