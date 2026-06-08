# audit-tool-cis-nist

CLI-first starter project for an administrator-oriented audit tool that uses a structured CIS Controls v8.1 dataset and NIST CSF mappings.

## What is included

- Full CIS Controls v8.1 starter dataset: 18 controls and 153 safeguards
- Interactive command-line assessment mode
- Non-interactive assessment mode using a JSON answers file
- Optional FastAPI backend for future integrations
- Optional React dashboard scaffold using Recharts
- GitHub Actions workflow for a basic test

## Quick start

### 1) Open in VS Code

```bash
git clone <your-repo-url>
cd audit-tool-cis-nist
code .
```

### 2) Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

- Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

- macOS/Linux:

```bash
source .venv/bin/activate
```

### 3) Install Python dependencies

```bash
pip install -r requirements.txt
pip install pytest
```

### 4) Run the CLI

List controls:

```bash
python -m audit_tool.main list-controls
```

Show one control:

```bash
python -m audit_tool.main show-control 12
```

Run a sample assessment:

```bash
python -m audit_tool.main assess --answers audit_tool/data/sample_answers.json --output reports/sample_report.json
```

Run the interactive administrator-friendly assessment:

```bash
python -m audit_tool.main interactive --output reports/interactive_report.json
```

Export the flat dataset:

```bash
python -m audit_tool.main export-dataset --format csv --output exports/cis_v8_1_flat.csv
```

### 5) Run the API (optional)

```bash
uvicorn audit_tool.api:app --reload
```

API docs:

- http://127.0.0.1:8000/docs

### 6) Run the dashboard (optional)

```bash
cd dashboard
npm install
npm run dev
```

The dashboard expects the API to be running locally on port 8000.

## Recommended next steps

1. Add your own evidence model (screenshots, config files, notes)
2. Add custom risk weights per safeguard and asset class
3. Add actual technical checks later (for example Nmap integration) only when you have permission and access
4. Extend the React dashboard for findings, trends, and exportable reports
