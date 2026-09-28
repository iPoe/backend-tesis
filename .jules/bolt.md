## 2024-05-24 - Bulk Query Pattern in DRF Serialization
**Learning:** The `CampaignViewSet.statistics` action has an N+1 query problem due to iterating over `resultados` and using `.get()` to look up `Contacto` objects individually based on `contacto_cc`.
**Action:** Optimize this by using `.in_bulk()` with `field_name='identidad'` (since `Contacto` uses `identidad` as its primary key).
