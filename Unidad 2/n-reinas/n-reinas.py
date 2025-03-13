import random
from collections import deque

class TabuSearchNQueens:
    def __init__(self, n=8, max_iterations=1000, tabu_tenure=10):
        self.n = n  # Número de reinas y tamaño del tablero (n x n)
        self.max_iterations = max_iterations  # Número máximo de iteraciones permitidas
        self.tabu_tenure = tabu_tenure  # Tiempo de permanencia en la lista tabú
        self.tabu_list = deque(maxlen=tabu_tenure)  # Lista tabú con memoria limitada
    
    def generate_initial_solution(self, entrada):
        """
        Genera una solución inicial aleatoria colocando las reinas en distintas filas.
        """
        if entrada == 1:
            return [int(input(f"Ingresa la columna de la reina en la fila {row + 1}: ")) for row in range(self.n)]
        else:
            return [random.randint(0, self.n - 1) for _ in range(self.n)]
    
    def calculate_conflicts(self, board):
        """
        Calcula el número de conflictos en un estado del tablero.
        """
        conflicts = 0
        for queen_col in range(self.n):
            for other_queen_col in range(queen_col + 1, self.n):
                if board[queen_col] == board[other_queen_col] or abs(board[queen_col] - board[other_queen_col]) == abs(queen_col - other_queen_col):
                    conflicts += 1
        return conflicts
    
    def get_neighbors(self, board):
        """
        Genera todos los vecinos del estado actual, moviendo cada reina a una nueva fila.
        """
        neighbors = []
        for queen_col in range(self.n):
            for new_row in range(self.n):
                if board[queen_col] != new_row:  # Evita movimientos redundantes
                    new_board = list(board)
                    new_board[queen_col] = new_row
                    neighbors.append((new_board, self.calculate_conflicts(new_board)))
        for neighbor in neighbors:
            print("Vecino generado:" + str(neighbor[0]) + " - Conflictos: " + str(neighbor[1]))
        return sorted(neighbors, key=lambda x: x[1])  # Ordena por menor cantidad de conflictos
    
    def print_board(self, board):
        """
        Imprime el tablero de ajedrez con el estado actual.
        """
        for row in range(self.n):
            line = ["."] * self.n
            line[board[row]] = "Q"
            print(" ".join(line))
        print("\n")
    
    def solve(self, entrada = 2):
        """
        Resuelve el problema de las N-Reinas utilizando búsqueda tabú.
        """
        current_board = self.generate_initial_solution(entrada)
        current_conflicts = self.calculate_conflicts(current_board)
        print("Tablero inicial:")
        self.print_board(current_board)
        
        for iteration in range(self.max_iterations):
            if current_conflicts == 0:
                print(f"Solución encontrada en {iteration} iteraciones:")
                self.print_board(current_board)
                return current_board  # Se encontró una solución óptima
            
            neighbors = self.get_neighbors(current_board)
            
            for neighbor_board, neighbor_conflicts in neighbors:
                if neighbor_board not in self.tabu_list:
                    self.tabu_list.append(neighbor_board)  # Agregar estado a la lista tabú
                    current_board = neighbor_board
                    current_conflicts = neighbor_conflicts
                    print(f"Iteración {iteration + 1} - Conflictos: {neighbor_conflicts}")
                    self.print_board(current_board)
                    break  # Avanza a la mejor solución no tabú encontrada
        
        print("No se encontró solución en las iteraciones máximas")
        return None  # No se encontró solución en las iteraciones máximas


## funcion main
print("Ingresa el tamaño del tablero (n x n):")
n = int(input())
print("Ingresa el número máximo de iteraciones:")
max_iterations = int(input())
print("Ingresa el tiempo de permanencia en la lista tabú:")
tabu_tenure = int(input())
print("\n")
print("Seleccione tipo de entrada de datos: \n 1. Manual \n 2. Aleatorio")
opcion = int(input())
tabu_search = TabuSearchNQueens(n, max_iterations, tabu_tenure)
solution = tabu_search.solve(opcion)
