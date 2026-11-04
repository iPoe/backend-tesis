## 2025-02-28 - Optimizando actualizaciones en bucle
**Learning:** Las actualizaciones de Django dentro de un bucle `for` (`.update()`) pueden causar el problema N+1. La solución es recopilar las identificaciones utilizando `.values_list()` y hacer una única llamada a la base de datos combinando objetos `Q()`.
**Action:** Utilice objetos `Q` para combinaciones dinámicas `OR` al convertir bucles N+1 en actualizaciones masivas o recuperaciones.
