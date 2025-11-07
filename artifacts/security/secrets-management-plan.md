# Secrets Management Implementation Plan

## Objective
Centralize application secrets in HashiCorp Vault to eliminate plaintext credentials in the repository and deployment pipelines.

## Milestones
1. **Stand up Vault cluster**
   - Deploy an HA Vault instance via managed service or on Kubernetes using the official Helm chart.
   - Integrate with organization SSO (OIDC) for operator authentication.

2. **Create secret engines**
   - Enable KV v2 engine at `secret/garage-app` for application configuration.
   - Enable database secrets engine to manage dynamic PostgreSQL credentials.
   - Enable transit engine for encryption-as-a-service (token signing, GDPR data at rest).

3. **Bootstrap policies & roles**
   - Define Vault policies for `app-server`, `ci-runner`, and `ops` personas with least privilege.
   - Configure GitHub OIDC auth method for the CI workflow with bound claims on repository and environment.

4. **Integrate with CI/CD**
   - Update `artifacts/ci/github-actions.yml` to request short-lived tokens via Vault's OIDC workflow.
   - Replace static secrets in GitHub with dynamic retrieval steps.
   - Store database migration credentials under Vault and inject them at runtime.

5. **Application integration**
   - Add a configuration bootstrap module that fetches secrets at startup using Vault's HTTP API and caches them in memory.
   - Rotate Flask `SECRET_KEY` and mail credentials through Vault; remove generated default secrets from `config.py`.

6. **Monitoring & auditing**
   - Enable Vault audit device streaming logs to the central SIEM.
   - Implement alerting for high-risk events (seal/unseal, policy changes, excessive 403s).

## Deliverables
- Vault deployment manifest and Terraform scripts (tracked in infrastructure repo).
- Onboarding documentation for developers covering CLI usage and secret request workflow.
- Runbook for rotating credentials and responding to Vault outages.
