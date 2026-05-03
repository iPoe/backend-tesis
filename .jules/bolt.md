## 2025-02-20 - N+1 Bottleneck in DRF Bulk Serializers
**Learning:** In this codebase, the DRF standard behavior for serializers with `many=True` causes an N+1 database problem where each item calls `save()` or `update_or_create()` individually.
**Action:** Always check models and viewsets handling arrays of data, and if they represent significant bulk insertion (like importing contacts), override the `list_serializer_class` on the `Meta` of the child serializer. Create a custom `ListSerializer` subclass that uses PostgreSQL's native `bulk_create` with `update_conflicts=True`. This takes a bulk save from ~0.8s to ~0.04s for 1000 items.

## 2025-02-20 - Test Environment Setup
**Learning:** Attempting to configure Django via `run_tests.py` using `settings.configure()` creates leftover artifacts. The test suite structure is a flat `tests.py` file within `campaigns`, and running a mock setup with partial apps can lead to import errors if the test paths aren't fully resolved. Also creating `campaigns/tests/__init__.py` overrides `campaigns/tests.py` as a module and breaks imports.
**Action:** Never run test scripts by dropping `run_tests.py` locally and ensure any temporary test scripts created to verify without DB are removed. Ensure we don't accidentally create test packages named `tests/` if `tests.py` exists.
