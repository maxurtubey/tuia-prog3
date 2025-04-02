from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Breadth First Search

        Args:
            grid (Grid): Grid of points
            
        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)

        # Verifica si el nodo es un nodo-objetivo y
        # en caso afirmativo devuelve la solución.
        if node.state == grid.end:
            return Solution(node, alcanzados)
        
        # Inicializa la frontera como una cola
        frontier = QueueFrontier()
        # Agrega el nodo a la frontera
        frontier.add(node)

        # Inicializa el diccionario alcanzados 
        # como un diccionario vacío
        alcanzados = {} 
        # Agrega el nodo al diccionario
        alcanzados[node.state] = True

        while True:

            # Falla si la frontera está vacía
            if frontier.is_empty():
                return NoSolution(alcanzados)
            
            # Quita un nodo de la frontera
            node = frontier.remove()
        
            # Alamacena las posibles acciones en el
            # diccionario vecinos
            vecinos = grid.get_neighbours(node.state)

            # Evalúa las acciones guardadas en vecinos
            for accion in vecinos:
                n_estado = vecinos[accion]

                # Verifica que el nuevo estado no fue alcanzado
                if n_estado not in alcanzados:
                    n_nodo = Node('', n_estado,
                                  node.cost + grid.get_cost(n_estado),
                                  parent=node, action=accion)
                    
                    # Verifica que sea un nodo objetivo
                    if n_nodo.state == grid.end:
                        return Solution(n_nodo, alcanzados)
                    
                    # Agrega el nuevo nodo a alcanzados
                    alcanzados[n_nodo.state] = True

                    # Agrega el nodo a la frontera
                    frontier.add(n_nodo)