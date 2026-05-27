
## 2024-05-18 - Optimize Campaign List View N+1 Issue
**Learning:** Found an N+1 query issue in the `list` method of `CampaignViewSet`. It was looping through serialized campaigns and querying `mediosxcampania` for each individual campaign. This scales poorly as the number of campaigns increases.
**Action:** Replaced the loop-based querying with an optimized bulk fetch using `campania_id__in=campaign_ids` and grouped the results in memory using `defaultdict(list)`. Applied `select_related('medio_id__tipo_medio')` to avoid subsequent N+1 queries when accessing related properties during serialization. Tests continue to pass.
