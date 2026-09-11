# Prompts

A record of the prompts and decisions that went into building this framework with Claude Code, in
the order they happened.

## 1. The original brief

> Senior QA Engineer Take-Home Exercise
> Create an automated testing framework using AI-assisted development.
>
> Test Targets
> Web application: SauceDemo - https://www.saucedemo.com/
> API: JSONPlaceholder - https://jsonplaceholder.typicode.com/
>
> Objective
> Demonstrate how you use AI to design and generate a test automation framework covering both the
> web application and API. You are responsible for determining: the language and automation tools;
> the framework structure; what scenarios to automate; how tests are organized and executed; how
> the framework is validated; what improvements are needed after reviewing the AI-generated output.
>
> Repository Requirement
> The repository must be created from scratch specifically for this exercise. Do not clone, fork,
> copy, or repurpose an existing automation framework or repository. Using libraries, packages,
> official documentation, and public examples for reference is allowed, but the submitted repository
> and framework structure must be created by you for this exercise.
>
> Deliverables: a link to a GitHub/GitLab/Bitbucket repo; a working automation framework covering
> both test targets; all prompts used during development; any requirements/notes/documentation used
> to refine prompts; an evaluation of the AI-generated framework (what worked, what didn't, what was
> changed).
>
> Time limit: approximately four hours.

## 2. Clarifying questions and answers

Two decisions were left to me and were hard to walk back later, so I asked before writing any code:

**Tech stack.** Options: Playwright + TypeScript (one framework, unified UI+API), Cypress + a
separate API plugin, or Python (Pytest + Selenium + Requests).
Picked: Python (Pytest + Selenium + Requests).

**Repository hosting.** `gh` wasn't installed, so repo creation/push couldn't happen on its own.
Options: pre-create an empty repo and hand over the URL, have the assistant install and
authenticate `gh` and create the repo itself, or keep everything local for now.
Picked: assistant creates it. That meant installing GitHub CLI via `winget`. The device-code browser
login (`gh auth login --web`) expired unused three times in a row before it could be completed, so
I switched to a personal access token (`gh auth login --with-token`) instead, and the repo was
created and pushed with `gh repo create`.

## 3. Build instructions

The working prompts used to generate the framework, in order:

1. Scaffold a Python project with a clear split between web (Selenium, Page Object Model) and API
   (a `requests`-based client), a shared env-driven config layer, and pytest as the runner for both.
2. Generate page objects for SauceDemo: login, inventory/product listing, cart, and the three-step
   checkout flow (info -> overview -> complete). Centralize locators per page, put shared
   find/click/type helpers in a `BasePage` instead of duplicating wait logic everywhere.
3. Write web test scenarios: valid login, locked-out user, invalid-credential/validation errors
   (parametrized), logout, product sorting in all four orders, add/remove from cart with badge
   count, cart contents and removal from the cart page, a full checkout happy path with a
   subtotal+tax=total check, and checkout field-validation errors (parametrized per field).
4. Write an API client wrapping `requests.Session` for JSONPlaceholder with convenience methods for
   posts/comments/users, plus JSON Schema definitions so response shape gets checked, not just
   status codes.
5. Write API test scenarios: list + get by id + schema validation, 404 on a missing resource,
   query-param filtering, POST/PUT/PATCH/DELETE on `/posts`, nested `/posts/{id}/comments`, an
   email-uniqueness check across `/users`, a basic response-time check.
6. Add pytest markers (`web`, `api`, `smoke`, `regression`) so either suite can run on its own or
   together, and set `pythonpath = .` so imports work without packaging boilerplate.
7. Add a Selenium driver fixture using `webdriver-manager` (headless Chrome by default, toggleable
   via env var) and a `pytest_runtest_makereport` hook to save a screenshot on any failed web test.
   (`webdriver-manager` got pulled out later once it turned out to be the reason every web test was
   failing - see EVALUATION.md.)
8. Add a GitHub Actions workflow with two independent jobs (api-tests, web-tests), installing
   Chrome for the web job, running each marker set separately, and uploading the HTML report (and
   screenshots) as build artifacts.
9. Run the full suite locally, fix whatever's actually broken against the real sites, and write up
   the failures and fixes honestly instead of quietly patching around them.
10. Write the README and evaluation doc, init git, create the remote repo via `gh`, and push.

## 4. Notes that shaped the prompts

- The brief leaves language, structure, scenario choice, and validation approach up to the
  candidate, so prompts 1-8 were written to make actual decisions (Page Object Model for web, schema
  validation for API, marker-based organization) instead of just asking for "some tests."
- ~4 hour time box, so scenario coverage stayed to the high-value paths per page/resource rather
  than trying to be exhaustive.
- JSONPlaceholder is a fake REST API - it echoes/validates payloads but doesn't actually persist
  writes. That was known going in and is why the write-endpoint tests check the echoed response
  rather than a follow-up `GET` (see the README's "Notes on JSONPlaceholder").
