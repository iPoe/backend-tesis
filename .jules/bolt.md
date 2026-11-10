
## 2024-11-10 - Optimizing bulk state changes across multiple related campaigns
**Learning:** The `_cambiar_estado_bulk` function in `campaigns/views.py` iterated through campaigns to query `mediosxcampania` and update `resultadosxcampania` for each, causing an N+1 query problem. Also, constructing Q objects on fields named explicitly with `_id` suffix requires using `field_id=X` instead of expecting Django to handle the instance vs integer correctly in all cases.
**Action:** Bulk fetch `mediosxcampania` using `.values_list()` grouped by campaign, reducing DB reads from O(N) to O(1). Individual `.update()` calls are maintained per campaign within `try/except` blocks to preserve fault tolerance.
