# Branch Protection Strategy

Apply these rules to the `main` branch to enforce secure delivery:

1. **Require pull request reviews**
   - Minimum of 2 approving reviews.
   - Dismiss stale approvals on new commits.
   - Require review from code owners.

2. **Status checks must pass**
   - `CI / Lint & Formatting Gate`
   - `CI / Unit & Integration Tests`
   - `CI / Static Application Security Tests`
   - `CI / Build Container Image`
   - Require status checks to be up to date before merging.

3. **Signed commits**
   - Enforce GPG or SSH signed commits for all contributors.

4. **Branch hygiene**
   - Require branches to be up to date with `main` before merging.
   - Prevent force pushes.
   - Prevent deletion of the `main` branch.

5. **Secrets management guardrails**
   - Enable secret scanning and push protection in the repository settings.
   - Add `*.env` and other secret patterns to GitHub's custom pattern rules.

6. **Deployment safeguards**
   - Require manual approval for the `production` environment.
   - Restrict deployment reviewers to `@devops-leads` team.
