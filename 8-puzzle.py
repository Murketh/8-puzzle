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
