class Node:
    prev = None
    next = None

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return str(self.data)

class ListaDobleEnlazada():

    def __init__(self):
        pass
    
    def index(self, node):
        if self.head == None: return
        try:
            if node < 0: return "Indice no valido"
            current = self.head
            for i in range(0, node):
                if current.next == None: break
                current = current.next
            return current
        except:
            return "Indice no valido"
    
    def pushFront(self, data):
        newNode = Node(data)

        if (self.head!=None):
            newNode.next = self.head
        if self.head != None: self.head.prev = newNode
        self.head = newNode
        if self.tail == None: self.tail = newNode
    
    def pushBack(self, data):
        newNode = Node(data)

        if (self.head==None):
            self.head = newNode
            self.tail = newNode
        else:
            self.tail.next = newNode
            newNode.prev = self.tail
            self.tail = newNode
    
    def popFront(self):
        if (self.head!=None):
            cabeza = self.head.data
            self.head = self.head.next
            self.head.prev = None
        if self.head==None: self.tail = None
        return cabeza
    
    def popBack(self):
        if (self.tail!=None):
            cola = self.tail.data
            self.tail = self.tail.prev
            self.tail.next = None
        if self.tail == None: self.head = None
        return cola
    
    def find(self, data):
        if (self.head == None): return
        current = self.head
        index = 0
        while current != None:
            if current.data == data:
                return index
            current = current.next
            index+=1
        return
    
    def erase(self, data):
        if self.head == None: return
        if self.head.data == data:
            self.head = self.head.next
            self.head.prev = None
            return
        current = self.head
        while current.next != None:
            if current.next.data == data:
                if self.tail == current.next: self.tail = current
                current.next.prev = current
                current.next = current.next.next
                return
            current = current.next
    
    def addBefore(self, node, data):
        newNode = Node(data)
        newNode.next = node
        newNode.prev = node.prev
        if node.prev != None: node.prev.next = newNode
        node.prev = newNode
        if node == self.head: self.head=newNode
        return
        
    def addAfter(self, node, data):
        newNode = Node(data)
        newNode.next = node.next
        newNode.prev = node
        if node.next!= None: node.next.prev = newNode
        node.next = newNode
        if node == self.tail: self.tail=newNode
        return
    
    def __str__(self):
        current = self.head
        texto = ""

        while(current!=None):
            texto += str(current) + " -> "
            current = current.next
        texto += "None"
        return texto