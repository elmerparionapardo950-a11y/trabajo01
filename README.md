# 🤖 Estimador de pedidos de kits de robótica

Página web estática en **HTML + CSS + JavaScript** (sin servidor, publicada con **GitHub Pages**) que estima los pedidos semanales de kits de robótica a partir de las consultas web, la inversión en publicidad y si hay campaña escolar.
Proyecto del taller de Machine Learning y Deep Learning — SENATI (Caso 01).

🔗 **Demo:** _pega aquí tu enlace_

## Modelo
Regresión lineal múltiple (scikit-learn) entrenada con 110 semanas **simuladas** (80 % entrenamiento / 20 % prueba, `random_state=42`):

```
pedidos ≈ 1.54 + 0.346·consultas_web + 0.0067·inversion_publicidad_soles + 5.02·campana_escolar
```

| Métrica (prueba) | Valor |
|---|---|
| MAE | ≈ 2.95 pedidos |
| R² | ≈ 0.79 |

Los coeficientes están en `modelo.json`, por lo que la web **no necesita scikit-learn ni servidor**: el cálculo se hace en el navegador.

## Ejecutar en local
Abrir el archivo `index.html` con doble clic en cualquier navegador.

## Estructura del repositorio
```
├── index.html          # página + cálculo en JavaScript
├── estilos.css         # estilos (CSS)
├── modelo.json         # coeficientes, rangos y métricas del modelo
├── capturas/           # capturas de las pruebas
└── README.md
```

## Pruebas
| Entrada | Resultado |
|---|---|
| 20 consultas · S/ 200 · sin campaña | ≈ 10 pedidos (9.8) |
| 55 consultas · S/ 800 · con campaña | ≈ 31 pedidos |

![Prueba 1](capturas/prueba1_20consultas_S200_sin_campana.png)
![Prueba 2](capturas/prueba2_55consultas_S800_con_campana.png)

## Validación y límites
- Rangos válidos: consultas 5–70, publicidad S/ 0–1100, campaña 0 o 1. La validación se hace en el navegador (JavaScript).
- Es una **estimación**, no una cifra exacta (error típico ±3 pedidos).
- Datos simulados; no incluye precio, competencia, feriados ni stock.
- Los coeficientes describen asociaciones, no causas.

## Publicar gratis en GitHub Pages
1. En el repositorio: **Settings → Pages**.
2. En *Build and deployment* elige **Deploy from a branch**, rama `main`, carpeta `/ (root)` y pulsa **Save**.
3. En 1–2 minutos aparece el enlace `https://TU_USUARIO.github.io/NOMBRE-DEL-REPOSITORIO/`.
