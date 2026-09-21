## 2024-05-18 - Optimize DB Queries
**Learning:** Refined an N+1 query vulnerability when iterating over contacts by fetching an existing object instead of a fresh DB read.
**Action:** Reuse existing parent objects when building child relations to avoid repetitive lookups in loops.
