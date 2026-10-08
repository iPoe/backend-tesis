## 2023-10-27 - [Optimizing DRF list serialization]
**Learning:** When optimizing DRF list serialization by bulk fetching related objects into an in-memory map based on `serializer.data` IDs, wrapping the query logic in an `if ids:` block instead of using an early return (e.g., `return Response(data)`) prevents bypassing downstream logic while avoiding unnecessary database queries with an empty `__in=[]` filter.
**Action:** When bulk fetching related data to add to serialized items, use conditional `if ids:` blocks for the bulk logic rather than early returns.

## 2023-10-27 - [Testing locally with sqlite and module shadowing]
**Learning:** Running `pytest campaigns/tests.py` fails with an 'import file mismatch' collection error due to a naming collision with the `campaigns/tests/` directory.
**Action:** Rely on standalone sqlite test scripts (like `run_tests_sqlite.py`) for local verification since renaming the file or deleting the directory are forbidden.
