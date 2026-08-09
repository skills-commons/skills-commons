Sprint log, week 32. Migrated 3 of 5 endpoints to the new auth service;
/orders and /invoices still on the old one. Wrote the migration tests, they pass
locally, never ran in CI. Tried the staging rollout Tuesday, rolled back after 20
minutes, 502s on /orders. Root cause not found yet. Meant to update the runbook,
did not get to it. Ana is out until Monday and owns the invoice path.
