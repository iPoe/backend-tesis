## 2023-10-17 - N+1 Query Fix in CampaignViewSet.statistics()
**Learning:** Found an N+1 query issue in the `CampaignViewSet.statistics()` method where `Contacto.objects.get(identidad=contacantiguo)` was called inside a loop over campaign results, causing numerous queries for campaigns with many contacts. Using `.in_bulk(field_name='identidad')` significantly reduces the number of database roundtrips.
**Action:** Always prefer batch fetching related items using `.in_bulk` or `.filter(id__in=...)` instead of iterating and calling `.get()` repeatedly on objects.
