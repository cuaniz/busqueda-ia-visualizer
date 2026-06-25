# Visualizador de Algoritmos de Búsqueda en IA

Aplicación interactiva desarrollada con **Python** y **Streamlit** que permite visualizar y comparar algoritmos de búsqueda aplicados a cuatro problemas clásicos de Inteligencia Artificial.

## Objetivo

Desarrollar una herramienta interactiva que permita seleccionar un problema, elegir el algoritmo de búsqueda correspondiente, ejecutar el proceso y visualizar paso a paso los estados principales de la búsqueda.

## Problemas y Algoritmos

| Tipo de búsqueda | Problema | Algoritmos |
|---|---|---|
| Búsqueda no informada | Laberinto tipo Frozen Lake (determinista) | BFS, DFS |
| Búsqueda informada | Sokoban (2 cajas, 2 objetivos) | A*, Greedy Best-First Search |
| Búsqueda local | 8 Reinas | Hill Climbing, Simulated Annealing |
| Búsqueda adversaria | Gato / Tic-Tac-Toe | Alpha-Beta Pruning |

## Requisitos

- Python 3.10 o superior
- Streamlit >= 1.35

## Instalación

```bash
cd busqueda-ia-visualizer
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Ejecución

```bash
streamlit run app.py
```

La aplicación abrirá automáticamente una página en el navegador.

## Estructura del proyecto

```
busqueda-ia-visualizer/
├── app.py                              # Punto de entrada y UI principal
├── requirements.txt                    # Dependencias del proyecto
└── search_visualizer/
    ├── models.py                       # Modelo SearchStep (estado de cada paso)
    ├── algorithms/
    │   ├── uninformed.py               # BFS y DFS
    │   ├── informed.py                 # A* y Greedy Best-First Search
    │   ├── local.py                    # Hill Climbing y Simulated Annealing
    │   └── adversarial.py              # Alpha-Beta Pruning (Minimax con poda)
    ├── problems/
    │   ├── frozen_lake.py              # Definición del laberinto Frozen Lake
    │   └── sokoban.py                  # Definición del puzzle Sokoban
    └── ui/
        └── renderers.py                # Renderizado visual de tableros (HTML/SVG)
```

## Descripción por módulo

### Problemas (`search_visualizer/problems/`)

Define el estado inicial, la función de meta, los sucesores y (cuando aplica) la heurística de cada problema. La lógica del problema está completamente separada de la interfaz.

- **Frozen Lake**: cuadrícula 4×4 con inicio (S), meta (G), hielo transitable (F) y huecos (H). Los vecinos se evalúan en orden antihorario.
- **Sokoban**: cuadrícula 6×6 con un jugador (P), 2 cajas (B) y 2 objetivos (G). El puzzle se resuelve cuando ambas cajas están sobre los objetivos.

### Algoritmos (`search_visualizer/algorithms/`)

Implementan los algoritmos de búsqueda y devuelven una lista de `SearchStep` con el estado completo en cada paso.

- **Búsqueda no informada** (`uninformed.py`): BFS (cola FIFO) y DFS (pila LIFO). Registran visitados, frontera, nodo actual y camino parcial.
- **Búsqueda informada** (`informed.py`): A* con f(n) = g(n) + h(n) y Greedy Best-First Search con solo h(n). Usan cola de prioridad con desempate.
- **Búsqueda local** (`local.py`): Hill Climbing (selecciona el mejor vecino) y Simulated Annealing (acepta movimientos peores según la temperatura).
- **Búsqueda adversaria** (`adversarial.py`): Minimax con poda Alpha-Beta para Tic-Tac-Toe. La máquina juega con X, el humano con O.

### Interfaz (`app.py` + `search_visualizer/ui/`)

- `app.py`: orquesta la selección de problema y algoritmo, ejecuta la búsqueda y muestra controles paso a paso.
- `renderers.py`: genera las representaciones HTML/SVG de cada tablero con iconografía y colores diferenciados por estado.

## Uso de la aplicación

1. Seleccionar el **problema** en el menú desplegable.
2. Seleccionar el **algoritmo** correspondiente.
3. Usar los controles (Inicio, Retroceder, Avanzar, Final) o el slider para navegar entre pasos.
4. Revisar las secciones de **Trazabilidad** (visitados, frontera, nodo actual) y **Camino parcial**.
5. En Tic-Tac-Toe, hacer clic en las celdas para jugar contra la máquina.
