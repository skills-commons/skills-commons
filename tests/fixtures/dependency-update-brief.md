Bot PR: bump the HTTP client library from 2.28.1 to 2.32.0. Our code uses its
Session object with a custom adapter, and disables certificate verification in
one place (scripts/legacy_sync.py). Release notes not read yet.
