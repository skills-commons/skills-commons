Called: POST https://api.internal/v2/reports with body {"range":"2026-07"}
Response: HTTP 504, body empty, after 30 seconds.
Retried twice, same result. Worked yesterday. Other endpoints on the same host
respond in 200ms. No deploy since Friday.
