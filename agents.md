# Codex Agent: OrderBot


## Purpose
Automates cross‑site order ingestion:
1. Partner → scrape orders
2. Our Site → create order
3. ArtServer → create folders + download files


## Agent Inputs
- Partner credentials (username, password)
- Our site credentials
- Root path to art server


## Agent Outputs
- Orders created
- Assets downloaded into correct job folders
- Ledger entries (CSV + JSONL)


## Codex Task Hints
- Use Playwright for navigation
- Wrap selectors in `selectors.py`
- CLI with Typer; GUI with CustomTkinter
- Logging with Rich + Tenacity retries
- Always sanitize job numbers for folder names


## Example Prompt for Codex
> "Add a new mapping in `oursite.py` to support customer notes field. Use Playwright to fill `#notes` in the form if `order.notes` exists."
