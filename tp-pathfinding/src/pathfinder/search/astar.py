from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class AStarSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using A* Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Función Heurística que devuelve la distancia de
        # Manhattan desde el nodo actual al 'grid.end'
        def heuristica(nodo_act: Node) -> int:
            return abs(nodo_act.state[0] - grid.end[0]) + abs(nodo_act.state[1] - grid.end[1])
        
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)

        # Inicializa la frontera como una cola de prioridad
        frontera = PriorityQueueFrontier()

        # Agrega el nodo y la suma de su costo más 
        # su heurística a la frontera
        frontera.add(node, node.cost + heuristica(node))
        
        # Inicializa alcanzados como diccionario vacío
        alcanzados = {} 

        # Agrega el estado y el costo a alcanzados
        alcanzados[node.state] = node.cost

        # Mientras la frontera no esté vacía:
        while frontera:

            # Quita al nodo de menor costo de la frontera
            nodo = frontera.pop()
            
            # Verifica si el estado del nodo es el 
            # estado-objetivo
            if nodo.state == grid.end:
                return Solution(nodo, alcanzados)
            
            # Alamacena las posibles acciones en el
            # diccionario vecinos
            vecinos = grid.get_neighbours(nodo.state)

            # Evalúa las acciones guardadas en vecinos
            for accion in vecinos:
                nuevo_estado = vecinos[accion]
                nuevo_costo = nodo.cost + grid.get_cost(nuevo_estado)
                # Descarta únicamente los nodos que fueron alcanzados con
                # un consto de camino menor
                if nuevo_estado not in alcanzados or nuevo_costo < alcanzados[nodo.state]:
                    nuevo_nodo = Node('', nuevo_estado, nuevo_costo, nodo, accion)
                    alcanzados[nuevo_estado] = nuevo_costo
                    frontera.add(nuevo_nodo, nodo.cost + heuristica(nuevo_nodo)) 
        
        # Devuelve 'NoSolution' porque frontera está vacía
        return NoSolution(alcanzados)