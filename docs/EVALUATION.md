# Evaluation

Notes on what the AI-generated code got right, what broke when it actually ran against the live
sites, and what I changed. See PROMPTS.md for the prompts behind each stage.

## Summary

The overall structure (page objects, API client, test scenarios, CI config) was solid from the
first pass and didn't need a redesign. But of the two suites, only the API suite passed unmodified
on the first real run - 16/16 against the live JSONPlaceholder API. The web suite needed several
rounds of actual bug fixes before all 20 tests passed reliably against SauceDemo, and none of those
bugs showed up just from reading the code - only from running it. That's really the main takeaway
here: generated Selenium code can look complete and idiomatic while still hiding race conditions
that only show up under real browser/network conditions.

## What worked out of the box

- **Project structure.** The web/api split, Page Object Model, shared `BasePage` helpers, env-driven
  `config/settings.py`, and marker-based organization (`web`/`api`/`smoke`/`regression`) all held up
  fine and needed no changes.
- **API suite.** All 16 tests (list/get/404/filter/POST/PUT/PATCH/DELETE, comments, users) passed
  against the live API without any changes. Validating response shape with `jsonschema`, not just
  status codes, was a good call that caught more than a status-code-only check would.
- **SauceDemo locators.** The add/remove-to-cart button IDs are derived from the product name
  (`add-to-cart-<slugified-name>`), including the one product with punctuation in it
  (`Test.allTheThings() T-Shirt (Red)`). Checked this against the real DOM and it matched exactly.
- **CI shape.** Splitting API and web into separate GitHub Actions jobs, each uploading its own HTML
  report/screenshots, worked fine and only needed a `--reruns` flag added later.

## What didn't work, and what I changed

Found all of these by actually running the suite against the live sites and reading the failures
and screenshots, not by re-reading the code. These are real bugs, not flakiness you can wave away
with a retry.

### 1. webdriver-manager resolved a stale ChromeDriver version

The first version pulled in `webdriver-manager` to handle the ChromeDriver, which is the standard
approach in most Selenium tutorials. In practice it resolved a cached, version-mismatched driver -
an old cached entry instead of the one matching the installed Chrome 152 - so every single web test
failed at driver startup with `SessionNotCreatedException`.

Fix: dropped `webdriver-manager` and let Selenium 4's built-in Selenium Manager handle driver
resolution instead (just `webdriver.Chrome(options=options)`, no explicit `Service`). It
auto-detects the installed browser and is the currently recommended approach for Selenium 4.6+.
This is a case of reaching for the well-known third-party tool when the platform already has a
newer built-in answer - and here the third-party tool was actively causing the failure.

### 2. find_all() raised instead of returning [] for an empty result

`BasePage.find_all()` was built on `presence_of_all_elements_located`, which raises
`TimeoutException` if zero elements match. But an empty cart is a valid state -
`item_names() == []` after removing the only item - and that case wasn't handled: "no matches" was
treated as a failure to find something rather than a legitimate result.

Fix: `find_all()` now catches the timeout and returns `[]`.

### 3. Cart/inventory badge assertions raced ahead of the app's re-render

`add_item_to_cart_by_name()` clicked the button and returned right away; the test then read the
cart badge on the next line. Classic UI automation race - `click()` returns once the command
completes, not once the SPA finishes re-rendering, so the assertion sometimes ran a moment before
the badge/button actually updated.

Fix: these actions now wait for a state that actually confirms the click was processed (the button
flipping from "Add to cart" to "Remove" and back, or the cart row disappearing) instead of assuming
the UI is settled as soon as click() returns.

### 4. Selenium's native click intermittently never reached the page in headless Chrome

This one took the longest to track down. After fixing #3, a couple of tests still failed, but the
failure mode was odd: the target button's state genuinely never changed, even several seconds after
the click, across repeated attempts with the same driver/browser version each time. Digging in:

- `document.elementFromPoint()` confirmed the click was landing on the correct element - nothing
  was covering it.
- Selenium's native `.click()` (a synthetic input event sent through Chrome DevTools Protocol)
  intermittently just didn't register. Not slow - dropped.
- Dispatching the same click via JavaScript (`element.click()`) on the same element worked reliably
  every time.

This is a known class of flakiness in headless Chrome's input-event simulation, and it wouldn't
have shown up from re-reading the code - only from scripting a side-by-side comparison of the two
click methods against the live site and watching the difference directly.

Fix: added `BasePage.click_until()`, which tries a normal click first (closer to how a real user
would interact) and falls back to a JS-dispatched click on retry if the expected UI state doesn't
show up. Keeps the realistic path as the default but gives the suite a working fallback for this
specific flake.

### 5. A stale-element race on rapid re-renders

Related but separate issue: `.text` was occasionally read off an element that had already been
replaced in the DOM by the time the read happened (`StaleElementReferenceException`), both on the
click path (locate then click) and the list-reading path (locate all, then read text off each one).

Fix: `click_until()` now also retries on `StaleElementReferenceException`, and a new `texts_of()`
helper retries the whole locate-and-read cycle as a unit instead of assuming an element stays valid
between locating it and reading it.

### 6. Network flakiness in this environment (unrelated to the framework)

Separately from all of the above, this sandbox has intermittent TLS/network stalls - confirmed
directly with plain `curl` against both target sites, where some requests finished in ~2s and
others just hung until timeout. That's an environment issue, not a bug in the framework, but the
framework should still tolerate it.

Change: added an explicit Selenium page-load timeout (30s instead of Selenium's 300s default, so a
stalled navigation fails fast rather than stalling the whole run), and added `pytest-rerunfailures`
(`--reruns 2 --reruns-delay 3`) to the web suite, both locally and in CI.

## Takeaways

- Structure and idioms were fine from the start - this is the kind of boilerplate-shaped work AI
  assistance is genuinely good at.
- Every real bug found was a runtime behavior issue (driver resolution, timing, race conditions, an
  engine-level input flake), and none of them would have been caught by reading the code. They only
  showed up by actually running the suite against the real target, repeatedly.
- The click-drop bug (#4) needed more than "just add a wait" - it took an actual side-by-side
  experiment (JS click vs. native click on the same element) to find the real mechanism before
  deciding on a fix. Flaky-looking failures are worth a real root-cause pass instead of a longer
  timeout or a blind retry.
