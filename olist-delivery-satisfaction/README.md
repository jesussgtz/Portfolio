# Retraso en la entrega vs. satisfacción del cliente — Olist E-Commerce

## 1. Información general
- **Nombre del proyecto:** Retraso y Satisfacción — Análisis logístico del e-commerce brasileño (Olist)
- **Especialidad:** Data Analysis (DA)
- **Fuente del proyecto:** Dataset (Kaggle)
- **Link a la fuente original:** https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
- **Link al proyecto publicado:** [Dashboard interactivo](https://claude.ai/code/artifact/8cceafe6-73a9-4491-bb9f-0b61b5e57a03) · también incluido como `dashboard.html` en esta carpeta (ábrelo directo en tu navegador, no necesita internet)

## 2. Objetivo
Determinar si los retrasos en la entrega (tiempo real vs. tiempo estimado) impactan negativamente la satisfacción del cliente (`review_score`), y en qué categorías de producto ese efecto es más severo. Esto apoya una decisión de negocio concreta: en qué categorías o rutas logísticas vale la pena invertir para proteger la reputación de los vendedores en la plataforma.

## 3. Plan de trabajo
1. **Exploración inicial** — Perfilado de 5 tablas (orders, reviews, items, products, customers): tamaños, nulos, duplicados, rangos de fechas y distribución de `review_score`.
2. **Preparación** — Filtrado a pedidos "delivered" con fecha de entrega válida, cálculo de `delivery_delay_days`, deduplicación de reseñas (quedándose con la más reciente por pedido) y asignación de categoría de producto por pedido (traducida a inglés).
3. **Construcción** — Análisis de correlación y segmentación por categoría; dashboard interactivo (HTML autocontenido) con KPIs, gráfica de reviews por rango de retraso y ranking de categorías más afectadas.
4. **Evaluación** — Validación de hallazgos con tamaños de muestra mínimos por categoría (100+ pedidos a tiempo, 20+ tarde) para evitar conclusiones sobre grupos muy pequeños.
5. **Conclusiones y próximos pasos** — Ver secciones 6 y 7.

## 4. Preguntas clave
1. ¿El retraso de entrega correlaciona con una caída medible en `review_score`, o hay otros factores que pesan más? → Sí correlaciona (r = −0.27), pero la relación no es lineal: existe un punto de quiebre claro (ver sección 6).
2. ¿Qué tan vigente es este dataset (2016–2018) y qué tanto se puede generalizar la conclusión a operaciones actuales? → Es un dataset histórico; la magnitud exacta puede haber cambiado, pero el patrón (retraso → caída de satisfacción) es un mecanismo de comportamiento del cliente que sigue siendo relevante.
3. ¿Un vendedor con retrasos frecuentes concentra sus malas reseñas en pocas categorías, o es un problema transversal? → Es mayormente transversal: 34 categorías con volumen suficiente muestran caída, aunque el tamaño de la caída varía bastante entre ellas.

## 5. Qué se hizo y cómo
- **Manejo de nulos:** se excluyeron los pedidos no entregados (3% del total) y los 8 pedidos "delivered" sin fecha de entrega registrada, ya que el retraso no se puede calcular sin esa fecha.
- **Deduplicación:** 551 pedidos tenían más de una reseña asociada; se conservó la reseña con `review_creation_date` más reciente por pedido.
- **Transformaciones:** se calculó `delivery_delay_days` (fecha real de entrega − fecha estimada), y se agrupó en 7 buckets (desde "7+ días antes" hasta "15+ días tarde") para visualizar el efecto de forma no lineal en vez de solo correlación.
- **Categorización:** cada pedido se etiquetó con la categoría de su primer producto (la mayoría de pedidos tiene un solo producto), traduciendo el nombre de categoría al inglés con la tabla de traducción oficial del dataset.
- **Herramientas:** Python (pandas) para limpieza y análisis; HTML/CSS/JS puro (sin librerías externas) para el dashboard, para que funcione sin conexión a internet y sin dependencias.

## 6. Resultados
- **95,824 pedidos** entregados y con reseña válida entraron al análisis final.
- Los pedidos **a tiempo o antes** tienen un review promedio de **4.29 ★**; los pedidos **tarde** caen a **2.57 ★** — una diferencia de casi 1.7 estrellas.
- **Hallazgo principal — punto de quiebre:** la caída no es gradual. Hasta 3 días de retraso, el review promedio se mantiene arriba de 3.7 (relativamente tolerado). A partir de 4 días de retraso, cae abruptamente a 2.3 y sigue empeorando con más días.
- **Categorías más afectadas** por el retraso (mayor caída en review promedio): instrumentos musicales (−2.27), audio (−2.15), juguetes (−1.99) y productos de bebé (−1.97) — categorías con una carga emocional o de regalo más alta, donde el tiempo de entrega parece importar más.
- Correlación general entre días de retraso y `review_score`: **r = −0.27** (moderada, consistente con que el efecto es más un "umbral" que una relación lineal continua).

## 7. Conclusiones
- El aprendizaje central: en logística, **no todo el retraso es igual de malo** — hay un margen de tolerancia (~3 días) y luego un colapso rápido en satisfacción. Esto es más accionable para un negocio que decir "menos retraso es mejor": sugiere fijar una alerta operativa específica en el día 4 de retraso, no solo monitorear el promedio general.
- Con más tiempo, profundizaría con una prueba de hipótesis formal (no solo comparación de promedios) para confirmar que la caída en el punto de quiebre es estadísticamente significativa y no ruido de muestra, y cruzaría con el precio del producto (quizás las categorías más afectadas también son las de mayor ticket promedio).
- Lo que mencionaría en una entrevista: el proceso de ir de "¿hay correlación?" a "¿dónde exactamente se rompe la tolerancia del cliente?" — ese es el tipo de pregunta de seguimiento que convierte un análisis genérico en un insight accionable para el negocio.
- Limitación reconocida: el dataset es de 2016-2018 y de un solo país (Brasil), así que la conclusión es un patrón de comportamiento a validar, no una cifra a aplicar directamente a otro contexto.

## 8. Checklist antes de publicar
- [x] README explica el proyecto sin necesidad de revisar todo el detalle
- [x] Archivos organizados, sin pruebas sueltas o versiones viejas
- [x] Sin credenciales ni datos sensibles en el repositorio
- [x] Link a la fuente original incluido y funcionando
- [x] Proyecto publicado y accesible (dashboard interactivo)
- [ ] Link compartido con tu coach

## Cómo reproducir este análisis
Los CSV originales de Kaggle (~120MB) no están incluidos en este repo por su tamaño. Para correr los scripts desde cero:

1. Descarga el dataset desde [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) y descomprímelo en una carpeta `data/` al mismo nivel que `scripts/`.
2. Instala dependencias: `pip install pandas`
3. Corre los scripts en orden: `python scripts/01_explore.py` (perfilado inicial) y luego `python scripts/02_prepare_and_analyze.py` (limpieza + análisis; regenera los CSV de `output/`).
4. `dashboard.html` ya trae los datos agregados embebidos — no depende de `data/` ni de conexión a internet para funcionar; ábrelo directo en el navegador.

## Estructura de la carpeta
```
olist-delivery-satisfaction/
├── README.md
├── dashboard.html          ← dashboard interactivo (autocontenido)
├── scripts/
│   ├── 01_explore.py       ← perfilado de datos
│   └── 02_prepare_and_analyze.py   ← limpieza, cálculo de retraso, análisis
├── output/
│   ├── delay_bucket_summary.csv    ← review promedio por rango de retraso
│   └── category_delay_impact.csv   ← impacto del retraso por categoría
└── data/                   ← (no incluida — descárgala de Kaggle, ver arriba)
```
