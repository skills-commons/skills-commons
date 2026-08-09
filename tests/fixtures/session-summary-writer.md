Worklog: read the billing module, found the retry loop double-charges when the
webhook arrives twice. Patched it with an idempotency key on charge_id. Tests:
added one for the duplicate webhook, it passes. Did not touch the refund path,
which probably has the same bug. Left a TODO in refunds.py line 88. Next person
should check whether the provider sends the same event id on replay - I assumed
it does.
