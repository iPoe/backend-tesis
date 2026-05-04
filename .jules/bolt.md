## 2024-05-30 - N+1 database queries in DRF nested objects
**Learning:** Initializing DRF Serializers with `many=True` runs child `create` functions in an explicit loop, which in the case of `ContactosSerializer` produces critical N+1 database bottlenecks during `update_or_create`.
**Action:** Always override `ListSerializer.create` alongside `list_serializer_class` meta attribute in standard `ModelSerializer` schemas so that Postgres native `bulk_create(update_conflicts=True)` eliminates performance bottlenecks.
