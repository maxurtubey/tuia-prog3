from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Uniform Cost Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)

        # Inicializa la frontera como una cola de prioridad
        frontera = PriorityQueueFrontier()

        # Agrega el nodo y su costo a la frontera
        frontera.add(node, node.cost)

        # Inicializa alcanzados como diccionario vacío
        alcanzados = {}

        # Agrega el estado y el costo a alcanzados
        alcanzados[node.state] = node.cost

        while True:

            # Falla si la frontera está vacía
            if frontera.is_empty():
                return NoSolution(alcanzados)
            
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
                    frontera.add(nuevo_nodo, nuevo_costo)
