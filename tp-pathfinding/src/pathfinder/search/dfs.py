from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search

        Args:
            grid (Grid): Grid of points
            
        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)

        # Verifica si el nodo es un estado-objetivo
        # y en caso afirmativo devuelve la solución.
        if node.state == grid.end:
            return Solution(node, expandidos)
        
        # Inicializa la frontera como una pila
        frontier = StackFrontier()
        # Agrega el nodo a la frontera
        frontier.add(node)

        # Inicializa el diccionario expandidos 
        # como un diccionario vacío
        expandidos = {} 
                
        while True:

            # Falla si la frontera está vacía
            if frontier.is_empty():
                return NoSolution(expandidos)
            
            # Quita un nodo de la pila frontera
            node = frontier.remove()

            # Evalúa si el estado del nodo 
            # está an expandidos
            if node.state in expandidos:
                continue

            # Agrega el estado del nodo a expandidos
            expandidos[node.state] = True

            # Alamacena las posibles acciones en el
            # diccionario vecinos
            vecinos = grid.get_neighbours(node.state)

            # Evalúa las acciones guardadas en vecinos
            for accion in vecinos:
                n_estado = vecinos[accion]
                # Verifica que el nuevo estado no 
                # esté en expandidos
                if n_estado not in expandidos:
                    n_nodo = Node('', n_estado,
                                  node.cost + grid.get_cost(n_estado),
                                  parent=node, action=accion)
                    
                    # Verifica que sea un nodo objetivo
                    if n_nodo.state == grid.end:
                        return Solution(n_nodo, expandidos)
                    # Agrega el nodo a la frontera
                    frontier.add(n_nodo)            