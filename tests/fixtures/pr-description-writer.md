Branch adds rate limiting to the public API. Commits: add token bucket
middleware; wire it into the router; config for per-key limits; tests. Motivated
by the incident last Tuesday where one client retry loop took down the search
endpoint. Limits are 100 requests per minute per key, configurable. No migration
needed.
