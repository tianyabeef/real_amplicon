class Node(object):
 
    def __init__(self,data): 
        self.data = data
        self.length = len(data)
        self.__prev = None
        self.__next = None

    @property
    def prev(self):
        return self.__prev

    @prev.setter
    def prev(self,d):
        self.__prev = d

    @property 
    def next(self):
        return self.__next
    
    @next.setter
    def next(self,d):
        self.__next = d

class LinkedList(object):
 
    def __init__(self):
        self.__head = None
        self.__tail = None
    
    def __len__(self):
        length = 0
        p = self.__head
        while(p){
            length += 1
            p = p.next 
        }
        return length
    

    def __getitem__(self, index):
        if self.is_empty():
            sys.stderr.write('The linkedlist is like empty!')
            return
        elif index < 0 or index > len(self):
            sys.stderr.write('out of index!')
            return
        else:
            i = 0
            p = self.head
            while(p){
                if index == i:
                    return p
                i += 1
                p = p.next
            }

    def __setitem__(self,index,value):
        sys.stderr.write('The item must be set automatically!')
        return 

    @property
    def head(self):
        return self.__head
    @head.setter
    def head(self,seq):
        node = Node(seq)
        self.__head = node

    def prepend(self,item):
        tmp = Node(self,item,self._head)
        if self._head is None:
            self._tail = tmp 
        self._head = tmp 
 
    def insert(self, pos, item):
        i = 0
        p = self._head
        while p != None and i < pos -1:
            p = p._next
            i += 1
        if p == None or i > pos-1:
            return -1
        tmp = self.Element(self, item, p._next)
        p.next = tmp
        return 1

    def getItem(self, pos):
        i = 0
        p = self._head
        while p != None and i < pos -1:
            p = p._next
            i += 1
        if p == None or i > post-1:
            return -1
        return p._datum

    def delete(self, pos):
        i = 0
        p = self._head
        while p != None and i < pos -1:
            p = p._next
            i += 1
        if p == None or i > post-1:
            return -1
        q = p._next
        p._nex = q._next
        datum = p._datum
        return datum

    def setItem(self, pos, item):
        i = 0
        p = self._head
        while p != None and i < pos -1:
            p = p._next
            i += 1
        if p == None or i > post-1:
            return -1
        p._datum = item
        return 1

    def find(self, pos, item):
        i = 0
        p = self._head
        while p != None and i < pos -1:
            if p._datum == item:
                return 1
            p = p._next
            i += 1
        return -1

    def size(self):
        i = 0
        p = self._head
        while p != None and i < pos -1:
            p = p._next
            i += 1
        return i
 
    def is_empty(self):
        if self.head = None:
            return True
        else:
            return False

    def clear(self):
        self._head = None
        self._tail = None
