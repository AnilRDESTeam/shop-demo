# Rules for AI assistants working in this repo

- Money uses `Decimal` (rounded half up to 2 places). Pricing rules live only in `app/pricing/`; constants live only in `app/config.py`.
- Never rename API fields, routes or `data-testid` values. They are a contract other tools depend on.
- `app/payments/` and `app/customers/` are high-risk areas: change them only when the task explicitly requires it.
- Always run `scripts\test.ps1` before committing, and add or adjust tests with every behaviour change.
- No network calls, no real payment or email code, no secrets.
- Keep code simple and readable; the team is beginner level.
