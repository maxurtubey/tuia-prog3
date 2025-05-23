"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo. Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from time import time
from problem import OptProblem
from collections import deque


class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)

        while True:

            # Buscamos la acción que genera el sucesor con mayor valor objetivo
            act, succ_val = problem.max_action(actual)

            # Retornar si estamos en un maximo local:
            # el valor objetivo del sucesor es menor o igual al del estado actual
            if succ_val <= value:

                self.tour = actual
                self.value = value
                end = time()
                self.time = end-start
                return

            # Sino, nos movemos al sucesor
            actual = problem.result(actual, act)
            value = succ_val
            self.niters += 1


class HillClimbingReset(LocalSearch):
    """Algoritmo de ascension de colinas con reinicio aleatorio."""

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas con reinicio aleatorio.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Iniciamos el reloj
        start = time()

        # Definimos las variables con los valores del estado inicial.
        best_state = problem.init
        best_value = problem.obj_val(problem.init)
        # Definimos variables para guardar la mejor solución
        # best_state = None
        # best_value = float("-inf")

        # Contabilizamos los reinicios
        reinicios = 0
        
        while reinicios < 10:

            # Reiniciamos aleatoriamente el problema
            actual = problem.random_reset()
            value = problem.obj_val(actual)
            
            # Para cada reinicio aplicamos HillClimbing
            while True:

                # Buscamos la acción que genera el sucesor con mayor valor objetivo
                act, succ_val = problem.max_action(actual)

                # Si estamos en un máximo local interrumpimos la ejecución del bucle while
                if succ_val <= value:
                    break

                # Sino, nos movemos al sucesor
                actual = problem.result(actual, act) #(devuelve el estado resultante de aplicar la acción act al estado actual)
                value = succ_val #(actualiza la variable value)
                self.niters += 1

            # Verificamos si la solución obtenida es mejor que la guardada
            if value > best_value:
                best_value = value
                best_state = actual

            reinicios += 1

        end = time()
        self.tour = best_state
        self.value = best_value
        self.time =  end - start


class Tabu(LocalSearch):
    """Algoritmo de busqueda tabu."""

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas usando lista tabu.
        Criterio de parada: cantidad de iteraciones
        La lista tabu almacena acciones

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)

        # Definimos variables para guardar la mejor solución
        best_state = actual
        best_value = value


        # Inicializamos la lista tabú, guardará acciones con enfoque de capacidad limitada
        tabu = deque()

        # Inicializamos contador (para criterio de parada por cantidad de iteraciones)
        iter = 1

        while iter < 1000:

            # Buscamos la acción que genera el sucesor con mayor valor objetivo, teniendo en cuenta la lista tabú con criterio de aspiración
            act, succ_val = problem.max_action(actual, tabu, best_value)

            # Verificamos si el valor de la función objetivo en el sucesor es mejor que el guardado en best_value
            if best_value < succ_val:
                best_state = problem.result(actual, act)
                best_value = succ_val

            # Actualizamos la lista tabu, teniendo en cuenta la limitación de capacidad
            if len(tabu) > 12:
                tabu.popleft()
                tabu.append(act)
            else:
                tabu.append(act)

            # Nos movemos al sucesor
            actual = problem.result(actual, act)
            value = problem.obj_val(actual)
            self.niters += 1

            iter += 1

        end = time()
        self.tour = best_state
        self.value = best_value
        self.time =  end - start
