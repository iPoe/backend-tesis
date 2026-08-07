## 2024-05-18 - N+1 query in CampaignViewSet.statistics
**Learning:** In `campaigns/viewsets.py`, the `statistics` action iterated over results and used `.get()` for each unique contact, causing an N+1 query.
**Action:** Use `.in_bulk(..., field_name='identidad')` to bulk fetch objects by a custom primary key/field before the loop to avoid querying in the loop. Always raise a `Model.DoesNotExist` explicitly if a record is not found in the dictionary to maintain original behavior.
