# Stripe API Automation (Python + Pytest + Requests)

API test automation for the **Stripe API (Test Mode)**, built with **Python**, **Requests** and
**Pytest**. Covers positive & negative flows, JSON **schema validation**, and **response-time**
assertions, with secrets handled through environment variables.
---

## Coverage at a glance

| Requirement | Where |
| --- | --- |
| **Positive** flows (valid responses + correct data) | `tests/test_customers.py`, `tests/test_payment_intents.py` |
| **Negative** flows (invalid key, missing params) | `tests/test_authentication.py`, `tests/test_payment_intents.py` |
| **Schema validation** (consistent JSON structure) | `tests/test_schema_validation.py` + `src/schemas/*.json` |
| **Performance** (response time < threshold) | `tests/test_performance.py` |
| **Auth via config/.env, no committed secrets** | `src/config/settings.py` + `.env` (git-ignored) |

### Why Stripe

Stripe's Test Mode offers a production-grade REST API with rich resources (customers, payment
intents), predictable error responses (401 for a bad key, 400 for missing params) and stable JSON
shapes — ideal for demonstrating positive, negative, schema and performance testing in one suite.

---

## Architecture

```
pytest-api-stripe/
├── src/
│   ├── api/client.py         # StripeClient: requests.Session, base URL, auth, timing log
│   ├── config/settings.py    # loads .env (python-dotenv), fails fast if key missing
│   └── schemas/              # JSON Schema per resource + validate_schema() helper
│       ├── customer.json
│       ├── list.json
│       └── payment_intent.json
├── tests/
│   ├── conftest.py           # fixtures: settings, api_client, bad_key_client, created_customer
│   ├── test_customers.py         # @positive
│   ├── test_payment_intents.py   # @positive + @negative
│   ├── test_authentication.py    # @negative (invalid key → 401)
│   ├── test_schema_validation.py # @schema
│   └── test_performance.py       # @performance
├── .env.example
├── pytest.ini                # markers, pythonpath, HTML report, live logging
├── requirements.txt
└── .github/workflows/ci.yml
```

**Design principles**

- **Layered:** a thin HTTP client (`StripeClient`) keeps `requests` details out of the tests; tests
  read as intent + assertions.
- **Config over hard-coding:** the base URL, key and performance budget all come from the
  environment via `src/config/settings.py`.
- **Declarative schemas:** response structure is described in `.json` files and enforced with the
  `jsonschema` library, so a shape change is caught immediately.
- **Isolated, repeatable data:** the `created_customer` fixture creates a customer per test and
  deletes it on teardown; emails are unique per call.
- **Every call is timed:** the client logs `METHOD path -> status in N ms` for visibility, and the
  performance tests assert against a configurable budget.

---

## Prerequisites

- **Python ≥ 3.10** (developed on 3.12)
- A free **Stripe account** to obtain a **test** secret key
  (Dashboard → Developers → API keys → *Secret key*, starts with `sk_test_`)

---

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
# Windows (PowerShell):  .venv\Scripts\Activate.ps1
# Windows (Git Bash):    source .venv/Scripts/activate
# macOS/Linux:           source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure your key (never commit this file)
cp .env.example .env
#   then edit .env and set STRIPE_SECRET_KEY=sk_test_...your key...
```

`.env` (git-ignored):

```
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxxxxxxxxx
STRIPE_BASE_URL=https://api.stripe.com/v1
PERF_THRESHOLD_MS=1000
```

> **Secrets never touch git.** `.env` is git-ignored; only `.env.example` (a placeholder) is
> committed. In CI the key is provided via a repository secret (see below).

---

## Running the tests

```bash
# Whole suite (HTML report written to reports/report.html)
pytest

# By coverage type (markers)
pytest -m positive
pytest -m negative
pytest -m schema
pytest -m performance

# A single file
pytest tests/test_customers.py -v
```

The negative auth test (`test_authentication.py`) needs **no valid key** — it deliberately uses a
bad key and asserts a 401, so it verifies connectivity and error handling on its own.

---

## Reports

An HTML report is generated on every run (configured in `pytest.ini`):

```
reports/report.html
```

Open it in a browser to see each test's outcome, captured logs and the per-request timings.

Live logs (including `... -> 200 in 84 ms` timing lines) are printed to the console during the run.

---

## Continuous Integration

`.github/workflows/ci.yml` installs dependencies and runs the suite on every push / pull request.
The Stripe test key is read from a **repository secret** named `STRIPE_SECRET_KEY`
(Settings → Secrets and variables → Actions), so no secret is ever stored in the repo.
