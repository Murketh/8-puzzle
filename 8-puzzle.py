import time


class Node:
    def __init__(self, data, level, fval):
        # Inicializa el nodo con la data y el valor calculado de la función f(x)
        self.data = data
        self.level = level
        self.fval = fval

    def generate_child(self):
        # Genera los nodos hijo de un nodo al mover el espacio en blanco
        # en cualquiera de las cuatro direcciones (arriba, abajo, izquierda, derecha)
        x, y = self.find(self.data, '_')
        # Lista que contiene los índices de las piezas
        # a las cuales puede moverse el espacio en blanco
        values_list = [[x, y-1], [x, y+1], [x-1, y], [x+1, y]]
        children = []
        for i in values_list:
            child = self.move(self.data, x, y, i[0], i[1])
            if child is not None:
                child_node = Node(child, self.level+1, 0)
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

    def copy(self, root):
        # Función copy para crear una matriz similar del nodo dado
        temp = []
        for i in root:
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

    def f(self, start, goal):
        # Función f calcula el valor heurístico f(x) = h(x)
        return self.misplaced_tiles(start.data, goal) - start.level

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
        while True:
            current = self.open[0]
            print("===============================\n")
            for i in current.data:
                for j in i:
                    print(j, end=" ")
                print("")

            if (self.misplaced_tiles(current.data, goal_state) == 0):
                print("\nh:", 0)
                print("Open:", len(self.open))
                print("Closed:", len(self.closed), "\n")
                break

            for i in current.generate_child():
                i.fval = self.f(i, goal_state)
                self.open.append(i)

            print("\nh:", current.fval)
            self.closed.append(current)
            del self.open[0]
            self.open.sort(key=lambda x: x.fval, reverse=True)
            print("Open:", len(self.open))
            print("Closed:", len(self.closed), "\n")

    def solve(self, start_state, goal_state):
        # Función solve resuelve el 8-puzzle
        # transformando el estado inicial en el estado objetivo
        start_time = time.time()
        start = Node(start_state, 0, 0)
        start.fval = self.f(start, goal_state)
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
