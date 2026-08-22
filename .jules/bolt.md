## 2025-05-18 - Eliminating Redundant Foreign Key Queries
**Learning:** Found an N+1 anti-pattern where a newly created model instance (Campaign) was re-queried (`.objects.get(pk=id)`) inside a loop for every related object (Contact) being prepared for a bulk insert.
**Action:** When preparing related objects for `bulk_create` inside a loop, directly assign the already available parent instance to the foreign key field instead of executing a redundant database lookup for each iteration.
