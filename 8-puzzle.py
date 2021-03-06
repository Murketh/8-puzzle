import time


class Node:
    def __init__(self, data, fval, direction):
        # Inicializa el nodo con la data, el valor calculado de la función f(x)
        # y la dirección del movimiento
        self.data = data
        self.fval = fval
        self.direction = direction

    def generate_child(self):
        # Genera los nodos hijo de un nodo al mover el espacio en blanco
        # en cualquiera de las cuatro direcciones (arriba, abajo, izquierda, derecha)
        x, y = self.find(self.data, '_')
        # Lista que contiene los índices de las piezas
        # a las cuales puede moverse el espacio en blanco
        # (derecha, izquierda, abajo, arriba) respectivamente
        values_list = [[x, y-1], [x, y+1], [x-1, y], [x+1, y]]
        directions = ["Derecha", "Izquierda", "Abajo", "Arriba"]
        children = []
        for index, value in enumerate(values_list):
            child = self.move(self.data, x, y, value[0], value[1])
            move_direction = directions[index]
            if child is not None:
                child_node = Node(child, 0, move_direction)
                children.append(child_node)
        return children

    def move(self, puzzle, x1, y1, x2, y2):
        # Mueve el espacio en blanco en la dirección dada
        # Si el valor de la posición está fuera del rango de la lista, se retorna None
        if x2 >= 0 and x2 < len(self.data) and y2 >= 0 and y2 < len(self.data):
            temp_puzzle = []
            temp_puzzle = self.copy(puzzle)
            temp = temp_puzzle[x2][y2]
            temp_puzzle[x2][y2] = temp_puzzle[x1][y1]
            temp_puzzle[x1][y1] = temp
            return temp_puzzle
        else:
            return None

    def copy(self, node):
        # Función copy para crear una matriz similar del nodo dado
        temp = []
        for i in node:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp

    def find(self, puzzle, x):
        # Función find permite encontrar la posición del espacio en blanco
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data)):
                if puzzle[i][j] == x:
                    return i, j


class Puzzle:
    def __init__(self):
        # Inicializa el tamaño del puzzle y las listas open y closed
        self.size = 3
        self.open = []
        self.closed = []

    def accept(self):
        # Función accept transforma el string ingresado por el usuario
        # y lo convierte en una lista
        puzzle = []
        for i in range(0, self.size):
            temp = input().split(" ")
            puzzle.append(temp)
        return puzzle

    def misplaced_tiles(self, start, goal):
        # Función misplaced_tiles cuenta el número de piezas
        # mal ubicadas con respecto al estado objetivo
        count = 0
        for i in range(0, self.size):
            for j in range(0, self.size):
                if start[i][j] != goal[i][j] and start[i][j] != '_':
                    count -= 1
        return count

    def best_first_search(self, goal_state):
        # Función best_first_search implementa el algoritmo Best First
        # con la heurística de piezas mal ubicadas
        while True:
            current = self.open[0]
            print("===============================\n")
            for column in current.data:
                for row in column:
                    print(row, end=" ")
                print("")

            print("\nDirección:", current.direction)
            print("h:", current.fval)

            if (self.misplaced_tiles(current.data, goal_state) == 0):
                break

            for i in current.generate_child():
                i.fval = self.misplaced_tiles(i.data, goal_state)
                self.open.append(i)

            self.closed.append(current)
            del self.open[0]
            self.open.sort(key=lambda x: x.fval, reverse=True)

    def solve(self, start_state, goal_state):
        # Función solve resuelve el 8-puzzle
        # transformando el estado inicial en el estado objetivo
        start_time = time.time()
        start = Node(start_state, 0, "")
        start.fval = self.misplaced_tiles(start.data, goal_state)
        self.open.append(start)
        print("\n")
        self.best_first_search(goal_state)
        print("Tiempo: %s segundos\n" % (time.time() - start_time))


if __name__ == "__main__":
    puzzle = Puzzle()
    print("\nIngrese el estado inicial: \n")
    start = puzzle.accept()
    print("\nIngrese el estado objetivo: \n")
    goal = puzzle.accept()
    puzzle.solve(start, goal)
