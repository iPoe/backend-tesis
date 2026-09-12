## 2024-05-24 - CampaignViewSet.list N+1 Optimization
**Learning:** The `CampaignViewSet.list` action in `campaigns/viewsets.py` suffers from an N+1 query problem by fetching related `mediosxcampania` items individually for each campaign in a loop.
**Action:** Optimize this by bulk fetching `mediosxcampania` mapped by `campania_id_id` via a `defaultdict`, combined with `.select_related('medio_id', 'medio_id__tipo_medio')`.
