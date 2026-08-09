## 2025-02-27 - N+1 Query in reply_whatsapp List Comprehension
**Learning:** The `reply_whatsapp` function evaluated `c.campania.estado` inside a list comprehension for a queryset missing `select_related`. This triggers an N+1 query issue for every campaign linked to a user.
**Action:** Always eagerly load related nested properties (e.g., `.select_related('campania', 'campania__estado')`) before iterating over them.
