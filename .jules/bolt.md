
## 2024-05-18 - [Bulk Serializer Upsert with update_conflicts]
**Learning:** Using `update_or_create` within the child serializer of a DRF bulk insertion leads to N+1 query bottlenecks as it triggers a round trip to the DB for each item.
**Action:** Overriding `ListSerializer.create` when `many=True` is passed allows you to use PostgreSQL's native `bulk_create(update_conflicts=True)` functionality to perform bulk upserts via `unique_fields` and `update_fields`, significantly minimizing database round trips.
