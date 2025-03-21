import random
import math

class SimulatedAnnealingNQueens:
    def __init__(self, n=8, initial_temp=1000, cooling_rate=0.99, min_temp=0.01):
        self.n = n  # Número de reinas y tamaño del tablero (n x n)
        self.initial_temp = initial_temp  # Temperatura inicial
        self.cooling_rate = cooling_rate  # Tasa de enfriamiento
        self.min_temp = min_temp  # Temperatura mínima para detener la búsqueda
    
    def generate_initial_solution(self, initial_board=None):
        """
        Genera una solución inicial aleatoria o utiliza la proporcionada por el usuario.
        """
        if initial_board:
            return initial_board
        return [random.randint(0, self.n - 1) for _ in range(self.n)]
    
    def calculate_conflicts(self, board):
        """
        Calcula el número de conflictos en un estado del tablero.
        """
        conflicts = 0
        for queen_col in range(self.n):
            for other_queen_col in range(queen_col + 1, self.n):
                # Verifica si hay conflictos en la misma fila o diagonal
                if board[queen_col] == board[other_queen_col] or abs(board[queen_col] - board[other_queen_col]) == abs(queen_col - other_queen_col):
                    conflicts += 1
        return conflicts

    def get_random_neighbor(self, board):
        """
        Genera un vecino aleatorio modificando la posición de una reina aleatoria.
        """
        neighbor = list(board)
        queen_col = random.randint(0, self.n - 1)  # Selecciona una columna aleatoria para mover la reina
        new_row = random.randint(0, self.n - 1)  # Nueva posición para la reina
        while neighbor[queen_col] == new_row:
            new_row = random.randint(0, self.n - 1)
        
        neighbor[queen_col] = new_row  # Actualiza la posición de la reina
        return neighbor

    def print_board(self, board):
        """
        Imprime el tablero de ajedrez con el estado actual.
        """
        for row in range(self.n):
            line = ["."] * self.n
            line[board[row]] = "Q"
            print(" ".join(line))
        print("\n")

    def accept_probability(self, old_cost, new_cost, temperature):
        """
        Calcula la probabilidad de aceptar una solución peor.
        """
        if new_cost < old_cost:
            return 1.0  # Acepta siempre si la nueva solución es mejor
        return math.exp((old_cost - new_cost) / temperature)  # Calcula probabilidad de aceptar solución peor
    
    def solve(self, initial_board=None):
        """
        Resuelve el problema de las N-Reinas utilizando recocido simulado.
        """
        current_board = self.generate_initial_solution(initial_board)  # Usa el tablero inicial ingresado o aleatorio
        current_conflicts = self.calculate_conflicts(current_board)  # Calcula conflictos iniciales
        temperature = self.initial_temp  # Inicializa la temperatura
        iteration = 0  # Contador de iteraciones

        print("Tablero inicial:")
        self.print_board(current_board)

        # Iteración principal hasta que la temperatura llegue al mínimo o no haya conflictos
        while temperature > self.min_temp and current_conflicts > 0:
            iteration += 1  # Incrementar iteración
            neighbor_board = self.get_random_neighbor(current_board)  # Genera vecino aleatorio
            neighbor_conflicts = self.calculate_conflicts(neighbor_board)  # Calcula conflictos del vecino
            acceptance_prob = self.accept_probability(current_conflicts, neighbor_conflicts, temperature)  # Probabilidad de aceptación

            # Decidir si aceptar el nuevo tablero
            if random.random() < acceptance_prob:
                current_board = neighbor_board  # Acepta nuevo estado
                current_conflicts = neighbor_conflicts  # Actualiza el número de conflictos
                accepted = True
            else:
                accepted = False

            # Imprimir datos relevantes de la iteración
            print(f"Iteración: {iteration}")
            print(f"Temperatura: {temperature:.2f}")
            print(f"Conflictos actuales: {current_conflicts}")
            print(f"Conflictos del vecino: {neighbor_conflicts}")
            print(f"Probabilidad de aceptación: {acceptance_prob:.4f}")
            print(f"Movimiento aceptado: {'Sí' if accepted else 'No'}")
            self.print_board(current_board)

            # Reducir la temperatura
            temperature *= self.cooling_rate

        # Si no hay conflictos, se encontró una solución válida
        if current_conflicts == 0:
            print("Solución encontrada:")
            self.print_board(current_board)
            return current_board
        else:
            # Si no se encontró solución después de enfriamiento
            print("No se encontró solución óptima.")
            return None

# Permite al usuario definir el tamaño del tablero
n = int(input("Introduce el número de reinas (N): "))

# Menú para elegir si ingresar manualmente o generar aleatoriamente
print("Elige una opción:")
print("1. Ingresar posiciones manualmente")
print("2. Generar posiciones aleatorias")
choice = input("Opción (1/2): ")

initial_board = []

if choice == "1":
    print(f"Introduce las posiciones de las reinas fila por fila (valores entre 0 y {n - 1}):")
    for i in range(n):
        while True:
            try:
                pos = int(input(f"Fila para la columna {i}: "))
                if 0 <= pos < n:
                    initial_board.append(pos)
                    break
                else:
                    print(f"Por favor, introduce un valor entre 0 y {n - 1}.")
            except ValueError:
                print("Entrada no válida. Introduce un número entero.")
else:
    initial_board = [random.randint(0, n - 1) for _ in range(n)]
    print("Posiciones generadas aleatoriamente:", initial_board)

# Ejecución del algoritmo
sa_n_queens = SimulatedAnnealingNQueens(n=n, initial_temp=2000, cooling_rate=0.99, min_temp=0.001)
solution = sa_n_queens.solve(initial_board)
