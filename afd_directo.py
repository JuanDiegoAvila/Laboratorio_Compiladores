
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

        print(ramas)

    

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
    