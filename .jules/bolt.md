## 2024-05-18 - Select Related in List Comprehensions
**Learning:** When evaluating related model properties inside a Python list comprehension (e.g. checking `c.campania.estado` where `c` is a queryset item), Django executes an N+1 query if `select_related` or `prefetch_related` is missing on the initial queryset.
**Action:** Always verify if a list comprehension or loop accesses foreign keys, and chain `.select_related()` to the parent queryset to fetch them eagerly.
