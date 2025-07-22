import Paises
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

    def __str__(self):
        return str(self.data)

class ListaDoblementeEnlazada:
    def __init__(self):
        self.head = None
        self.tail = None
    
    def index(self, node):
        if self.head is None:
            return None
        if node < 0:
            return "Índice no válido"
        current = self.head
        for i in range(node):
            if current.next is None:
                break
            current = current.next
        return current
    
    def pushFront(self, data):
        newNode = Node(data)
        if self.head is not None:
            newNode.next = self.head
            self.head.prev = newNode
        self.head = newNode
        if self.tail is None:
            self.tail = newNode
    
    def pushBack(self, data):
        newNode = Node(data)
        if self.head is None:
            self.head = newNode
            self.tail = newNode
        else:
            self.tail.next = newNode
            newNode.prev = self.tail
            self.tail = newNode
    
    def popFront(self):
        if self.head is None:
            return None
        cabeza = self.head.data
        self.head = self.head.next
        if self.head is not None:
            self.head.prev = None
        else:
            self.tail = None
        return cabeza
    
    def popBack(self):
        if self.tail is None:
            return None
        cola = self.tail.data
        self.tail = self.tail.prev
        if self.tail is not None:
            self.tail.next = None
        else:
            self.head = None
        return cola
    
    def find(self, data):
        if self.head is None:
            return None
        current = self.head
        index = 0
        while current is not None:
            if current.data == data:
                return current
            current = current.next
            index += 1
        return None
    
    def find_por_nombre(self, nombre_pais):
        current = self.head
        while current is not None:
            if isinstance(current.data, Paises.Paises):
                if current.data.get_nombre() == nombre_pais:
                    return current
            current = current.next
        return None

    
    def erase(self, data):
        if self.head is None:
            return
        if self.head.data == data:
            self.head = self.head.next
            if self.head is not None:
                self.head.prev = None
            else:
                self.tail = None
            return
        current = self.head
        while current.next is not None:
            if current.next.data == data:
                if self.tail == current.next:
                    self.tail = current
                to_delete = current.next
                current.next = to_delete.next
                if current.next is not None:
                    current.next.prev = current
                return
            current = current.next
    
    def addBefore(self, node, data):
        if node is None:
            return
        newNode = Node(data)
        newNode.next = node
        newNode.prev = node.prev
        if node.prev is not None:
            node.prev.next = newNode
        node.prev = newNode
        if node == self.head:
            self.head = newNode
    
    def addAfter(self, node, data):
        if node is None:
            return
        newNode = Node(data)
        newNode.next = node.next
        newNode.prev = node
        if node.next is not None:
            node.next.prev = newNode
        node.next = newNode
        if node == self.tail:
            self.tail = newNode
    
    def __str__(self):
        current = self.head
        texto = ""
        while current is not None:
            texto += str(current) + " -> "
            current = current.next
        texto += "None"
        return texto

