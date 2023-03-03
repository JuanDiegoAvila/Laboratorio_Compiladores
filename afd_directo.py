from prettytable import PrettyTable

def is_operand(char):
    return True if char.isalpha() else char.isnumeric()


class AFD_D(object):
    def __init__(self, expresion):
        self.expresion = expresion+'#.'
        self.expresion = ([*self.expresion])
        self.alfabeto = self.getAlfabeto()
        self.followposT = {}
        self.ramas = []
        self.construccion_directa()

        
    def getAlfabeto(self):
        alfabeto = []
        for char in self.expresion:
            if is_operand(char) and char not in alfabeto:
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

        print(self.followposT)
        self.tabla_transiciones(ramas)

    def nullable(self, nodo):
        if nodo.valor == 'ε':
            nodo.nullable = True
        elif is_operand(nodo.valor):
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
        if is_operand(nodo.valor) or nodo.valor=='#':
            nodo.first_pos = [nodo.pos]
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
        if is_operand(nodo.valor) or nodo.valor=='#':
            nodo.last_pos = [nodo.pos]
        elif nodo.valor == '*':
            nodo.last_pos = nodo.left.last_pos
        elif nodo.valor == '.':
            if nodo.right.nullable:
                nodo.last_pos = nodo.left.last_pos + nodo.right.last_pos
            else:
                nodo.last_pos = nodo.right.last_pos
        elif nodo.valor == '|':
            nodo.last_pos = nodo.left.last_pos + nodo.right.last_pos

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


                    if not existe:
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

        self.print_transiciones(transiciones, estados)

        return None
    
    def print_transiciones(self, transiciones, estados):
        x = PrettyTable()
        x.field_names = ["Posiciones", "Estado"]
        for i in range(len(self.alfabeto)):
            x.field_names.append("Transiciones con " +self.alfabeto[i])
    
        for transicion in transiciones:
            posicion = estados[transicion-1]['posiciones']
            estado = estados[transicion-1]['estado']

            temp = []

            for letra in transiciones[transicion]:
                if letra not in temp:
                    temp.append(letra)

            estados_temp = []
            for element in temp:
                estados_temp.append(self.getEstado(estados, transiciones[transicion][element]))

            
            lista = [posicion, estado]
            lista.extend(estados_temp)
            x.add_row(lista)
        
        print(x.rows)

        print(x)

        
        

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
        x = PrettyTable()
        x.field_names = ["Valor", "FirstPos", "LastPos", "FollowPos", "Nullable"]
        x.add_row([self.valor, self.first_pos, self.last_pos, self.follow_pos, self.nullable])
        return x.get_string()+'\n\n'
    