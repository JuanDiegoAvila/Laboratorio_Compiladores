
def is_operand(self, char):
    return True if char.isalpha() else char.isnumeric()


class AFD_D(object):
    def __init__(self, expresion):
        self.expresion = expresion+'#.'
        self.expresion = ([*self.expresion])
        self.followposT = {}
        self.ramas = []
        self.construccion_directa()

        
    def construccion_directa(self):

        # se construye el arbol sintactico
        arbol = ConstruccionArbol()
        ramasRaiz = arbol.Arbol(self.expresion)
        ramas = arbol.ramas
        ramas.append(ramasRaiz)
        
        for rama in ramas:
            if rama.nullable == None:
                self.nullable(rama)
            if rama.first_pos == None:
                self.firstpos(rama)
            if rama.last_pos == None:
                self.lastpos(rama)

    def nullable(self, nodo):
        if nodo.valor == 'ε':
            nodo.nullable = True
        elif is_operand(nodo.nullable):
            nodo.nullable = False
        elif nodo.valor == '*':
            nodo.nullable = True
        elif nodo.valor == '.':
            nodo.nullable = nodo.left.nullable and nodo.right.nullable
        elif nodo.valor == '|':
            nodo.nullable = nodo.left.nullable or nodo.right.nullable
    
    def firstpos(self, nodo):
        if nodo.valor == 'ε':
            nodo.fistpos = []
        if is_operand(nodo.valor):
            nodo.first_pos = [nodo.valor]
        elif nodo.valor == '*':
            nodo.first_pos = nodo.left.first_pos
        elif nodo.valor == '.':
            if nodo.left.nullable:
                nodo.first_pos = nodo.left.first_pos + nodo.right.first_pos
            else:
                nodo.first_pos = nodo.left.first_pos
        elif nodo.valor == '|':
            nodo.first_pos = nodo.left.first_pos + nodo.right.first_pos

    def lastpos(self, nodo):
        if nodo.valor == 'ε':
            nodo.last_pos = []
        if is_operand(nodo.valor):
            nodo.last_pos = [nodo.valor]
        elif nodo.valor == '*':
            nodo.last_pos = nodo.left.last_pos
        elif nodo.valor == '.':
            if nodo.right.nullable:
                nodo.last_pos = nodo.left.last_pos + nodo.right.last_pos
            else:
                nodo.last_pos = nodo.right.last_pos
        elif nodo.valor == '|':
            nodo.last_pos = nodo.left.last_pos + nodo.right.last_pos


class ConstruccionArbol(object):
    def __init__(self):

        self.followposT = {}
        self.ramas = []
        self.contador = 0

    def simple(self, nombre):
        self.contador+=1
        self.followposT[self.contador]=[]
        return Nodo(valor=nombre,pos=self.contador)
    
    def concat(self, valor, nodo1, nodo2):
        self.ramas.append(nodo1)
        self.ramas.append(nodo2)
        return Nodo(valor=valor, left=nodo2, right=nodo1)
    
    def orS(self, valor, nodo1, nodo2):
        self.ramas.append(nodo1)
        self.ramas.append(nodo2)
        return Nodo(valor=valor, left=nodo2, right=nodo1)
    
    def kleene(self, valor, nodo1):
        self.ramas.append(nodo1)
        return Nodo(valor=valor, left=nodo1)

    # implementacion parecida a thompson pero con Nodos del arbol sintactico
    def Arbol(self, stack):
        binarios = '|.'
        unarios = '*+'
        operadores = '|.*+'

        primero = stack.pop()

        if primero in binarios:
            nodo1 = stack.pop()

            if nodo1 in operadores:
                stack.append(nodo1)
                nodo1 = self.Arbol(stack)
            
            nodo2 = stack.pop()

            if nodo2 in operadores:
                stack.append(nodo2)
                nodo2 = self.Arbol(stack)

            '''
                Se revirete el orden llamando primero a nodo2 para que el contador
                de posiciones sea correcto.
            '''
            if isinstance(nodo2, str):
                nodo2 = self.simple(nodo2)
            
            if isinstance(nodo1, str):
                nodo1 = self.simple(nodo1)
            
            
            if primero == "|":
                
                return self.orS(primero, nodo1, nodo2)
            
            elif primero == ".":
                return self.concat(primero, nodo1, nodo2)
        
        elif primero in unarios:
            nodo1 = stack.pop()

            if nodo1 in operadores:
                stack.append(nodo1)
                nodo1 = self.Arbol(stack)

            if isinstance(nodo1, str):
                nodo1 = self.simple(nodo1)

            if primero == "*":
                return self.kleene(primero, nodo1)
        
        else:
            return self.simple(primero)

class Nodo(object):
    def __init__(self, valor = None, first_pos = None, last_pos = None, follow_pos = None, nullable = None, left = None, right = None, pos = None):
        self.valor = valor
        self.first_pos = first_pos
        self.last_pos = last_pos
        self.follow_pos = follow_pos
        self.nullable = nullable
        self.left = left
        self.right = right
        self.pos = pos

    def getValor(self):
        return self.valor
    
    def getFirstPost(self):
        return self.first_post
    
    def getLastPost(self):
        return self.last_post
    
    def getFollowPos(self):
        return self.follow_pos

    def __str__(self):
        return str(self.valor)
    
    def __repr__(self):
        return ('valor -> [ %s ] left -> [ %s ] right -> [ %s ] posicion -> [ %s ]\n' % (self.valor, self.left, self.right, self.pos))
    