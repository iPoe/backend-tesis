## 2023-10-14 - Fix N+1 queries in CampaignViewSet list
**Learning:** Returning nested relations during Django REST Framework serialization can introduce N+1 query problems within loops over `.data` where `.filter()` or `.get()` calls occur.
**Action:** When optimizing DRF list serialization by bulk fetching related objects into an in-memory map based on `serializer.data` IDs, wrap the query logic in an `if ids:` block instead of using an early return to prevent bypassing downstream logic while avoiding unnecessary database queries.
