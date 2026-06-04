# Visualizador de algoritmos de búsqueda en IA

Aplicación interactiva en Python + Streamlit para visualizar y comparar algoritmos de búsqueda aplicados a cuatro problemas clásicos.

| Tipo de búsqueda | Problema | Algoritmos incluidos |
|---|---|---|
| Búsqueda no informada | Frozen Lake determinista | BFS, DFS, UCS |
| Búsqueda informada | Sokoban | A*, Greedy Best-First Search |
| Búsqueda local | 8 reinas | Hill Climbing, Simulated Annealing |
| Búsqueda adversaria | Gato / Tic-Tac-Toe | Minimax, Alpha-Beta Pruning |

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

- **Frozen Lake**: explicar frontera, visitados y camino encontrado.
- **Sokoban**: explicar `g(n)`, `h(n)` y `f(n)` en A*.
- **8 reinas**: explicar conflictos y óptimos locales.
- **Tic-Tac-Toe**: explicar MAX, MIN, utilidad y poda alfa-beta.

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
