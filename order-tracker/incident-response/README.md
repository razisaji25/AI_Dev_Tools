# Incident responder

Receives Grafana webhook payloads at `POST /alerts` on port `8001`. It stores each
alert together with recent Order Tracker logs from Loki and traces from Tempo, then
runs Codex CLI in headless mode and saves its response with the incident record.

Start from the `order-tracker` directory after starting its Docker Compose stack:

```powershell
uv run --frozen python incident-response/responder.py
```

The listener binds to `127.0.0.1` by default. Codex CLI must be available in `PATH`.
The Grafana datasource proxy is used for Loki and Tempo, so no separate ports or
credentials for those data sources are needed. Codex CLI must be authenticated in the
environment where the responder runs. Set `GRAFANA_URL`, `CODEX_BIN`, or
`AGENT_TIMEOUT_SECONDS` to override defaults.

Incident payloads and assistant responses are written to `incident-response/incidents/`.
Test alerts (`labels.test=true` or a summary containing `no incident to fix`) use Codex
with the `read-only` sandbox. Other firing alerts use Codex's `workspace-write` sandbox.
The service does not configure Grafana notifications; that is a separate contact-point
step.

Health check: `GET /healthz`.
