from prettytable import PrettyTable
from thompson import *

def is_operand(char):
    return True if char.isalpha() else char.isnumeric()

def order_nodos(first_node):
        visitados = {first_node}
        queue = deque([first_node])
        nodos_ordenados = []

        while queue:
            nodo = queue.popleft()
            nodos_ordenados.append(nodo)

            for s_nodo, valor in nodo.transicion.items():
                if s_nodo not in visitados:
                    visitados.add(s_nodo)
                    queue.append(s_nodo)

        return nodos_ordenados


class AFD_D(object):
    def __init__(self, expresion):
        self.expresion = expresion+'#.'
        self.expresion = ([*self.expresion])
        self.alfabeto = self.getAlfabeto()
        self.followposT = {}
        self.ramas = []
        self.transiciones, self.estados = self.construccion_directa()
        self.iniciales_finales(self.estados)
        self.nodos = self.crear_nodos(self.transiciones, self.estados)

    
    def iniciales_finales(self, estados):
        finales = []
        for follow in self.followposT:
            if len(self.followposT) in self.followposT[follow]:
                finales.append(follow)

        estados_f = []
        for estado in estados:
            if len(self.followposT) in estado["posiciones"]:
                estados_f.append(estado["estado"])

        for estado in estados:
            estado["inicial"] = False
            estado["aceptacion"] = False
            if estado["estado"] in estados_f:
                estado["aceptacion"] = True
            else:
                estado["aceptacion"] = False
            # numero = estado["estado"].split('S')
            # numero = int(numero[1]) + 1

            

            # if numero in finales:
            #     estado["aceptacion"] = True

        estados[0]["inicial"] = True
                

    def crear_nodos(self, transiciones, estados):
        nodos = []
        for estado in estados:
            nodo = Nodo(estado["estado"])
            nodo.inicial = estado["inicial"]
            nodo.final = estado["aceptacion"]
            nodos.append(nodo)
        
        for nodo in nodos:
            transicion = int(nodo.conteo.split('S')[1]) +1
            for index, value in transiciones[transicion].items():
                if value != []:
                    for estado in estados:
                        if estado["posiciones"] == value:
                            for n in nodos:
                                if n.conteo == estado["estado"]:
                                    nodo.addTransition(n, index)
        
        nodos = order_nodos(nodos[0])
        return nodos
        
    def getAlfabeto(self):
        alfabeto = []
        for char in self.expresion:
            if is_operand(char) and char not in alfabeto and char!='ε':
                alfabeto.append(char)
        return alfabeto

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

        self.followpos(ramas[len(ramas)-1])
        self.followposT = {k: v for k, v in sorted(self.followposT.items(), key=lambda item: item[0])}

        return self.tabla_transiciones(ramas)

    def nullable(self, Rama):
        if Rama.valor == 'ε':
            Rama.nullable = True
        elif is_operand(Rama.valor):
            Rama.nullable = False
        elif Rama.valor == '*':
            Rama.nullable = True
        elif Rama.valor == '.':
            Rama.nullable = Rama.left.nullable and Rama.right.nullable
        elif Rama.valor == '|':
            Rama.nullable = Rama.left.nullable or Rama.right.nullable
    
    def firstpos(self, Rama):
        if Rama.valor == 'ε':
            Rama.fistpos = []
        if is_operand(Rama.valor) or Rama.valor=='#':
            Rama.first_pos = [Rama.pos]
        elif Rama.valor == '*':
            Rama.first_pos = Rama.left.first_pos
        elif Rama.valor == '.':
            if Rama.left.nullable:
                Rama.first_pos = Rama.left.first_pos + Rama.right.first_pos
            else:
                Rama.first_pos = Rama.left.first_pos
        elif Rama.valor == '|':
            Rama.first_pos = Rama.left.first_pos + Rama.right.first_pos

    def lastpos(self, Rama):
        if Rama.valor == 'ε':
            Rama.last_pos = []
        if is_operand(Rama.valor) or Rama.valor=='#':
            Rama.last_pos = [Rama.pos]
        elif Rama.valor == '*':
            Rama.last_pos = Rama.left.last_pos
        elif Rama.valor == '.':
            if Rama.right.nullable:
                Rama.last_pos = Rama.left.last_pos + Rama.right.last_pos
            else:
                Rama.last_pos = Rama.right.last_pos
        elif Rama.valor == '|':
            Rama.last_pos = Rama.left.last_pos + Rama.right.last_pos

    def followpos(self, raiz):
        if raiz.right:
            self.followpos(raiz.right)

        if raiz.left:
            self.followpos(raiz.left)
        
        if raiz.valor == '.':
            for i in raiz.left.last_pos:
                if i not in self.followposT:
                    self.followposT[i] = []
                
                for right in raiz.right.first_pos:
                    if right not in self.followposT[i]:
                        self.followposT[i].append(right)

                        self.followposT[i].sort()
        
        elif raiz.valor == '*':
            for i in raiz.last_pos:
                if i not in self.followposT:
                    self.followposT[i] = []

                for left in raiz.left.first_pos:
                    if left not in self.followposT[i]:
                        self.followposT[i].append(left)
                        self.followposT[i].sort()

        elif raiz.valor == "#":
            self.followposT[raiz.pos] = []
    
    def final(self, diccionario):
        temp = []
        for i in diccionario:
            if i['final']:
                temp.append(True)
            else:
                temp.append(False)
        return False if False in temp else True
        


    def tabla_transiciones(self, ramas):
        primera_posicion = ramas[len(ramas)-1].first_pos
        transiciones = {}
        estados = [
            {
                'estado': 'S0',
                'posiciones': primera_posicion,
                'final': False
            }
        ]

        mas_conjuntos = False
        contador = 0

        while not self.final(estados):
            temp_estado = estados[contador]
            estados[contador]['final'] = True

            for letra in self.alfabeto:
                if letra != '#':
                    temp = []
                    for element in temp_estado['posiciones']:
                        for rama in ramas:
                            if letra == rama.valor and element == rama.pos:
                                temp.extend(self.followposT[element])
                                temp.sort()
                    
                    existe = False
                    for estado in estados:
                        if estado['posiciones'] == temp:
                            existe = True


                    if not existe and temp != []:
                        estados.append({
                            'estado': 'S'+str(len(estados)),
                            'posiciones': temp,
                            'final': False
                        })

                    if contador+1 not in transiciones:
                        transiciones[contador+1] = {}

                    if letra not in transiciones[contador+1]:
                        transiciones[contador+1][letra] = {}

                    transiciones[contador+1][letra] = temp
                    
            contador+=1
        return transiciones, estados
    
    # def print_transiciones(self, transiciones, estados):
    #     x = PrettyTable()
    #     x.field_names = ["Posiciones", "Estado"]
    #     for i in range(len(self.alfabeto)):
    #         if self.alfabeto[i] != '#':
    #             mensaje = "Transiciones con " + self.alfabeto[i]
    #             x.field_names.append(mensaje)
    
    #     for transicion in transiciones:
    #         posicion = estados[transicion-1]['posiciones']
    #         estado = estados[transicion-1]['estado']

    #         temp = []

    #         for letra in transiciones[transicion]:
    #             if letra not in temp:
    #                 temp.append(letra)

    #         estados_temp = []
    #         for element in temp:
    #             estados_temp.append(self.getEstado(estados, transiciones[transicion][element]))

            
    #         lista = [posicion, estado]
    #         lista.extend(estados_temp)
    #         x.add_row(lista)
        
    #     print(x.rows)

    #     print(x)

        
        

    def getEstado(self, estados, conjunto):
        for estado in estados:
            if estado['posiciones'] == conjunto:
                return estado['estado']


class ConstruccionArbol(object):
    def __init__(self):

        self.followposT = {}
        self.ramas = []
        self.contador = 0

    def simple(self, nombre):
        self.contador+=1
        self.followposT[self.contador]=[]
        return Rama(valor=nombre,pos=self.contador)
    
    def concat(self, valor, Rama1, Rama2):
        self.ramas.append(Rama1)
        self.ramas.append(Rama2)
        return Rama(valor=valor, left=Rama2, right=Rama1)
    
    def orS(self, valor, Rama1, Rama2):
        self.ramas.append(Rama1)
        self.ramas.append(Rama2)
        return Rama(valor=valor, left=Rama2, right=Rama1)
    
    def kleene(self, valor, Rama1):
        self.ramas.append(Rama1)
        return Rama(valor=valor, left=Rama1)

    # implementacion parecida a thompson pero con Ramas del arbol sintactico
    def Arbol(self, stack):
        binarios = '|.'
        unarios = '*+'
        operadores = '|.*+'

        primero = stack.pop()

        if primero in binarios:
            Rama1 = stack.pop()

            if Rama1 in operadores:
                stack.append(Rama1)
                Rama1 = self.Arbol(stack)
            
            Rama2 = stack.pop()

            if Rama2 in operadores:
                stack.append(Rama2)
                Rama2 = self.Arbol(stack)

            '''
                Se revirete el orden llamando primero a Rama2 para que el contador
                de posiciones sea correcto.
            '''
            if isinstance(Rama2, str):
                Rama2 = self.simple(Rama2)
            
            if isinstance(Rama1, str):
                Rama1 = self.simple(Rama1)
            
            
            if primero == "|":
                
                return self.orS(primero, Rama1, Rama2)
            
            elif primero == ".":
                return self.concat(primero, Rama1, Rama2)
        
        elif primero in unarios:
            Rama1 = stack.pop()

            if Rama1 in operadores:
                stack.append(Rama1)
                Rama1 = self.Arbol(stack)

            if isinstance(Rama1, str):
                Rama1 = self.simple(Rama1)

            if primero == "*":
                return self.kleene(primero, Rama1)
        
        else:
            return self.simple(primero)


class Rama(object):
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
        x = PrettyTable()
        x.field_names = ["Valor", "FirstPos", "LastPos", "FollowPos", "Nullable"]
        x.add_row([self.valor, self.first_pos, self.last_pos, self.follow_pos, self.nullable])
        return x.get_string()+'\n\n'
    