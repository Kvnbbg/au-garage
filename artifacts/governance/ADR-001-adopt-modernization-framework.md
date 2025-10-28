# ADR-001: Adopt Senior Developer Modernization Framework

- **Status:** Proposed
- **Date:** 2025-01-28
- **Context:** The Garage V. Parrot system has grown organically with minimal automation and governance. Security controls are ad hoc, CI is limited to Dependabot verification, and documentation does not capture architectural decisions. Upcoming feature expansions and customer onboarding require resilient delivery practices.
- **Decision:** Adopt the Senior Developer Modernization Framework as the guiding doctrine for engineering work. The framework mandates comprehensive CI/CD, observability, DevSecOps practices, probabilistic enhancements to business logic, and living documentation including ADRs and DORA metrics tracking.
- **Consequences:**
  - Immediate investment in pipeline automation, security hardening, and governance artifacts.
  - Teams must document future architectural decisions using ADR templates and review them quarterly.
  - Engineering OKRs will incorporate DORA metrics improvements and observability baselines.
  - Product delivery may slow temporarily while modernization tasks are completed, but long-term velocity, reliability, and audit readiness improve.
