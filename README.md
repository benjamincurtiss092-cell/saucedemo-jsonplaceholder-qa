# SauceDemo + JSONPlaceholder Test Automation Framework

Test automation covering:

- **Web UI** - [SauceDemo](https://www.saucedemo.com/), using Selenium with the Page Object Model.
- **API** - [JSONPlaceholder](https://jsonplaceholder.typicode.com/), using `requests` with JSON
  Schema validation on responses.

Both suites run under a single Pytest runner and can be selected independently via markers.

This was built with AI-assisted development. `docs/PROMPTS.md` has the prompt log and
`docs/EVALUATION.md` covers what the generated code got wrong and how it was fixed.

## Stack

| Concern           | Choice                                 |
|-------------------|-----------------------------------------|
| Language          | Python 3.11+                            |
| Test runner       | Pytest                                  |
| Web automation    | Selenium 4 (built-in Selenium Manager)  |
| API client        | `requests`                              |
| Schema validation | `jsonschema`                            |
| Reporting         | `pytest-html`                           |
| CI                | GitHub Actions                          |

## Project structure

```
.
├── api/
│   ├── client.py              # requests-based client for JSONPlaceholder
│   ├── schemas.py              # JSON Schemas for response validation
│   └── tests/                  # API test suite
├── web/
│   ├── pages/                  # Page Object Model for SauceDemo
│   └── tests/                  # Web UI test suite
├── config/
│   └── settings.py              # env-driven configuration
├── docs/
│   ├── PROMPTS.md               # AI prompts used during development
│   └── EVALUATION.md            # evaluation of AI-generated output
├── .github/workflows/ci.yml     # CI pipeline (separate API/web jobs)
├── conftest.py                  # shared fixtures (Selenium driver, screenshot-on-fail hook)
├── pytest.ini
└── requirements.txt
```

## Setup

```bash
python -m venv .venv
source .venv/Scripts/activate      # Windows Git Bash; use .venv\Scripts\Activate.ps1 in PowerShell
pip install -r requirements.txt
cp .env.example .env                # optional, defaults already point at the public sites
```

Chrome needs to be installed locally for the web suite. Selenium's built-in Selenium Manager
resolves a matching ChromeDriver automatically, no extra setup needed.

## Running tests

```bash
# Everything
pytest

# Only API tests
pytest -m api

# Only web tests (--reruns helps with transient network blips against the public site)
pytest -m web --reruns 2 --reruns-delay 3

# Fast smoke subset
pytest -m smoke

# Full regression set
pytest -m regression

# With an HTML report
pytest --html=reports/report.html --self-contained-html

# Run web tests with a visible browser (debugging)
HEADLESS=false pytest -m web
```

## Test scenarios

### Web (SauceDemo)

- **Login** - valid login, locked-out user, empty/invalid credential errors (parametrized), logout.
- **Inventory** - add/remove item updates the cart badge, product sorting in all four orders
  (name A-Z/Z-A, price low-high/high-low), adding multiple items.
- **Cart** - item shows up in cart, removal from the cart page, "continue shopping" navigation.
- **Checkout** - full happy-path checkout (info -> overview -> complete) with a subtotal + tax =
  total check, plus per-field validation errors.

### API (JSONPlaceholder)

- **Posts** - list all, get by id + schema validation, 404 on a missing id, filter by `userId`,
  create (`POST`), full update (`PUT`), partial update (`PATCH`), delete (`DELETE`), nested
  comments for a post.
- **Users** - list all, get by id + schema validation, 404 on a missing id, email uniqueness across
  all users.
- **Comments** - filter by `postId` query param + schema validation, well-formed emails, a basic
  response time check.

## CI

`.github/workflows/ci.yml` runs on every push/PR to `main` with two independent jobs (`api-tests`,
`web-tests` on headless Chrome), each uploading its HTML report (and screenshots for the web job)
as a build artifact.

## Validation

Both suites were run against the live sites, not just written and assumed to work: 16/16 API tests
passed unmodified on the first run, while the web suite needed a few rounds of real bug fixes
(driver resolution, a UI race condition, an intermittent headless-Chrome click issue, a
stale-element race) before reaching 20/20. Details in `docs/EVALUATION.md`. All 36 tests currently
pass, both locally and in CI.

## Notes on JSONPlaceholder

JSONPlaceholder is a fake REST API - it validates and echoes back whatever you `POST`/`PUT`/`PATCH`,
including plausible status codes and IDs, but nothing is actually persisted server-side. Tests
against write endpoints assert against the echoed response, not a follow-up `GET`, since that would
just show the write never happened.
