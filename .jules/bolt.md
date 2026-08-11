
## 2025-03-04 - Fix N+1 Query in CampaignViewSet.statistics
**Learning:** The `CampaignViewSet.statistics` action iterated over the serialized data to manually resolve nested objects using `.get(identidad=contacantiguo)` inside a loop, resulting in a severe N+1 query problem scaling linearly with the number of campaign results.
**Action:** To resolve Django N+1 query problems within loops over serialized data or viewsets, bulk fetch related instances using `.in_bulk(id_list)` (specifying `field_name` if it differs from the default PK) or `.filter(id__in=ids)` before the loop and construct an in-memory dictionary for O(1) lookups.
