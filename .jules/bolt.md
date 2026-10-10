## 2025-02-28 - Bulk fetching with explicitly named ForeignKey id suffixes
**Learning:** When optimizing N+1 query loops that rely on explicit model relationships (e.g. `campania_id`), you should extract the foreign key suffix attribute `_id` like `mxc.campania_id_id` when grouping querysets via `defaultdict` to preserve relationship mappings without hitting the DB.
**Action:** When extracting grouped relationships mapped by a `ForeignKey` attribute that's explicitly named with an `_id` suffix, access it via `_id_id` to reliably fetch the integer ID in-memory.
