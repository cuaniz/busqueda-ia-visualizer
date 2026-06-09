# Visualizador de algoritmos de búsqueda en IA

Aplicación interactiva en Python + Streamlit para visualizar y comparar algoritmos de búsqueda aplicados a cuatro problemas clásicos.

| Tipo de búsqueda | Problema | Algoritmos incluidos |
|---|---|---|
| Búsqueda no informada | Frozen Lake determinista | BFS, DFS |
| Búsqueda informada | Sokoban (2 cajas, 2 objetivos) | A*, Greedy Best-First Search |
| Búsqueda local | 8 reinas | Hill Climbing, Simulated Annealing |
| Búsqueda adversaria | Gato / Tic-Tac-Toe | Alpha-Beta Pruning (interactivo humano vs máquina) |

## Características

- **Etiquetas numéricas**: todos los tableros muestran el identificador numérico de cada celda (row-major: `fila * ancho + columna`).
- **Tic-Tac-Toe interactivo**: el humano juega con O, la máquina responde con X usando poda Alpha-Beta.
- **Metadatos de búsqueda no informada**: BFS y DFS muestran listas de IDs de celdas visitadas (`visitados`), frontera (`frontera`), nodo actual y longitud del camino.
- **Criterio antihorario**: en Frozen Lake, los vecinos se evalúan en orden antihorario (Arriba, Izquierda, Abajo, Derecha).
- **Sokoban con 2 cajas y 2 objetivos**: el puzzle tiene exactamente dos cajas y dos objetivos distintos; se considera resuelto solo cuando ambas cajas están sobre objetivos.

## Instalación

```bash
cd C:\Users\dgcua\Documents\busqueda-ia-visualizer
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución

```bash
streamlit run app.py
```

La aplicación abrirá una página local en el navegador.

## Cómo explicar la práctica

La app está separada en tres partes:

1. `search_visualizer/problems/`: define problemas, estados, acciones y sucesores.
2. `search_visualizer/algorithms/`: implementa los algoritmos de búsqueda.
3. `app.py`: muestra los pasos visualmente con Streamlit.

La idea importante es que la interfaz NO contiene la lógica central del algoritmo. La UI solo muestra los pasos que devuelven las funciones de búsqueda.

## Guía rápida de exposición

- **Frozen Lake**: explicar frontera, visitados y camino encontrado. Mostrar los IDs numéricos de cada celda. Señalar el orden antihorario de selección de vecinos.
- **Sokoban**: explicar `g(n)`, `h(n)` y `f(n)` en A*. Mostrar que el estado es resuelto solo con las 2 cajas en los 2 objetivos.
- **8 reinas**: explicar conflictos y óptimos locales. Las filas tienen etiquetas verticales 1..8.
- **Tic-Tac-Toe**: juego interactivo humano (O) vs máquina (X) con Alpha-Beta. Explicar MAX, MIN, utilidad y poda.

## Estructura

```text
app.py
requirements.txt
search_visualizer/
  algorithms/
    adversarial.py
    informed.py
    local.py
    uninformed.py
  problems/
    frozen_lake.py
    sokoban.py
  ui/
    renderers.py
  models.py
```
