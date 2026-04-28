## 2026-04-28 - PostgreSQL bulk_create and test discovery in Django
**Learning:**
1. `bulk_create` returns objects with their `id` fields populated when using PostgreSQL. But if you plan to rely on `id`, ensure you iterate using a method that doesn't make brittle assumptions (like `zip` instead of index lookups).
2. Never delete `__init__.py` in test directories (like `campaigns/tests/__init__.py`) to 'reset' tests, as this breaks Django's test discovery which relies on tests being in a valid Python module.
3. Be careful not to commit temporary standalone test runner scripts (like `run_tests.py`) with mock configs to the repository.

**Action:**
Next time performing a database insertion optimization, verify that any loop iterating over created records correctly pairs with the target data (e.g., using `zip()`). Also, ensure any temporary test scaffolding or configuration mock files are deleted before submission.
