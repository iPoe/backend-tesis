## 2024-05-24 - Initializing Bolt Journal
**Learning:** Establishing the journal to record critical learnings in the codebase.
**Action:** Will add entries here when discovering performance bottlenecks specific to this codebase's architecture.

## 2024-05-24 - Resolve N+1 query bottleneck in statistics calculation
**Learning:** Using loop-based `.get()` queries for related models (like Contacto) creates significant performance bottlenecks when processing serialized statistics data.
**Action:** Bulk fetch `.in_bulk()` maps before the loop to handle this in O(1) memory time without losing specific error handling like `DoesNotExist`.
