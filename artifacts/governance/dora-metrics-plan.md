# DORA Metrics Implementation Plan

## Tooling
- **Data sources:** GitHub REST & GraphQL APIs, GitHub Actions logs, ArgoCD deployment events.
- **Storage:** Time-series database (InfluxDB or Prometheus) feeding Grafana dashboards.
- **Automation:** Nightly GitHub Action scheduled workflow calling a Python script to calculate metrics.

## Metrics
1. **Deployment Frequency**
   - Count successful `deploy` job executions targeting production per day/week.
   - Emit metrics via GitHub Actions step using `curl` to push to the metrics gateway.

2. **Lead Time for Changes**
   - Measure elapsed time between first commit on PR and merge timestamp.
   - Use GitHub GraphQL API to retrieve `createdAt` for commits and `mergedAt` for PRs.

3. **Change Failure Rate**
   - Track failed deployments by parsing ArgoCD sync status and GitHub Actions failures after deployment.
   - Tag incidents in PagerDuty with deployment IDs to correlate with rollbacks.

4. **Mean Time to Restore (MTTR)**
   - Monitor incident creation and resolution timestamps in PagerDuty.
   - Automate data ingestion through PagerDuty Events API and store in metrics backend.

## Roadmap
1. Build Python CLI under `tools/dora_metrics.py` that fetches data and outputs JSON payloads.
2. Schedule nightly GitHub Action to execute CLI and push metrics to storage.
3. Create Grafana dashboard with four panels reflecting each metric's trailing 7/30-day trends.
4. Set SLOs (e.g., deploy at least daily, MTTR < 1 hour) and alert when metrics breach thresholds.
5. Review metrics during weekly engineering sync and feed insights into quarterly OKRs.
