from collections import deque

class Simulacion(object):
    def __init__(self, nodos, alfabeto = None, expresion = None, tipo = None):
        self.expresion = expresion
        self.nodos = nodos
        self.alfabeto = alfabeto

        self.contador = 0
        self.visitados = self.crearVisitados(nodos)
        if tipo:
            self.aceptado, self.movimientos = self.simulacionAFN() if tipo == "AFN" else self.simulacionAFD()

        self.aceptado = False
        self.movimientos = ""
        self.linea = 1
        self.entrada = ''
        self.puntero = 0

    def crearVisitados(self, nodos):
        visitados = {}
        for nodo in nodos:
            visitados[nodo] = False
        return visitados

    def sigCar(self, expresion):
        car = expresion[self.contador]
        self.contador += 1
        return car

    def e_closure(self, nodos):

        nodos = [nodos] if type(nodos) != list else nodos

        for nodo in nodos:
            queue = deque([nodo])
            while queue:
                nodo = queue.popleft()
                for s_nodo, valor in nodo.transicion.items():
                    if s_nodo not in nodos and valor == ['ε']:
                        nodos.append(s_nodo)
                        queue.append(s_nodo)
                        self.visitados[s_nodo] = True
        return nodos
    
    def move(self, nodos, simbolo):
        
        nodos = [nodos] if type(nodos) != list else nodos
        n_nodos = []

        for nodo in nodos:
            for s_nodo, valor in nodo.transicion.items():
                simbolo = [simbolo] if type(simbolo) != list else simbolo
                if valor == simbolo:
                    self.visitados[s_nodo] = True
                    n_nodos.append(s_nodo)

        return n_nodos  

    def simulacionAFN(self):
        expresion = [caracter for caracter in self.expresion]
        expresion.append('#') # Se agrega el simbolo de fin de cadena

        S = self.e_closure(self.nodos[0])
        c = self.sigCar(expresion)

        while (c != '#'):
            move = self.move(S, c)
            S = self.e_closure(move)
            c = self.sigCar(expresion)

        movimientos = ""
        for visitado in self.visitados:
            if self.visitados[visitado]:
                for key, value in visitado.transicion.items():
                        movimientos+= "\n\t\t "+str(visitado.conteo)+" -> "+str(value)+" -> "+str(key.conteo)+"\n"

        for s in S:
            if s.final:
                return True, movimientos
        return False, movimientos
    
    def move_mega_automata(self, nodos, simbolo):
        nodos = [nodos] if type(nodos) != list else nodos
        n_nodos = []
        if simbolo == '\n':
            simbolo = '\\n'
        elif simbolo == '\t':
            simbolo = '\\t'

        for nodo in nodos:
            for s_nodo, valor in nodo.transicion.items():
                simbolo = [simbolo] if type(simbolo) != list else simbolo
                if valor == simbolo:
                    self.visitados[s_nodo] = True
                    n_nodos.append(s_nodo)
        return n_nodos

    def setEntrada(self, entrada, token_keys, rules):
        self.entrada = entrada
        self.entrada += ' @'
        self.token_keys = token_keys
        self.rules = rules
        self.puntero = 0

    def sigCarP(self):
        car = self.entrada[self.puntero]
        self.puntero += 1

        # if car == '\n':
        #     self.linea += 1
        return car
    
    def getPuntero(self):
        return self.puntero

    def setPuntero(self, puntero):
        self.puntero = puntero
    
    def verificar(self, aceptado, texto_reconocido):
        output = []
        # print('==================ACEPTADO==================')
        # print('aceptado: ', aceptado)
        # print('texto_reconocido: ', texto_reconocido)
        # print('====================================')
        for token in aceptado:
            existe = False

            for key, value in self.rules.items():
                if texto_reconocido == key:
                    if value != '':
                        output.append(value)
                        existe = True

                    break
                if token == key and not existe:
                    if value != '':
                        output.append(value)
                        existe = True

                    break
                    
        
            if not existe and token not in self.token_keys:
                posicion = 0
                for i in range(self.linea):
                    posicion += len(texto_reconocido)
                # +' en la posicion ' + str(posicion)+'
                string = 'Error lexico en la linea '+ str(self.linea +1)+' : ' + repr(texto_reconocido) + ' no es un token valido'
                output.append(string)

        return output
        
    
    # simulacion afn del yalex con punteros para que siga recibiendo caracteres hasta que reconozca algo
    def simulacionAFN_YALEX_PUNTERO(self):
    
        S = self.e_closure(self.nodos[0])
        c = self.sigCarP()

        
        reconocidos = []
        temp = ''
        temp2 = ''

        texto_reconocido = []
        while (c != '@'):

            move = self.move_mega_automata(S, c)

            if move == []:

                if self.puntero > 1:
                    self.puntero -= 1

                nodos_reconocidos = []
                for s in S:
                    if s.final_yalex:
                        nodos_reconocidos.append(s.valor_diccionario)

                if len(nodos_reconocidos) > 0 and nodos_reconocidos[0] != []:
                    temp = nodos_reconocidos
                else:
                    temp = [temp]

                S = self.e_closure(self.nodos[0])

                aceptado = temp
                textoreconocido = temp2 if temp2 != '' else c

                temp = ''
                temp2 = ''

                move = self.move_mega_automata(S, c)

                return self.verificar(aceptado, textoreconocido), False

            temp += c
            temp2 += c

            S = self.e_closure(move)
            c = self.sigCarP()
        

        if c == '@':
            return None, True

    def simulacionAFN_YALEX(self, expresion):
        self.contador = 0
        expresion = [caracter for caracter in expresion]
        expresion.append('@') # Se agrega el simbolo de fin de cadena

        S = self.e_closure(self.nodos[0])
        c = self.sigCar(expresion)

        reconocidos = []
        temp = ''
        temp2 = ''
        reconocidos = []

        texto_reconocido = []
        while (c != '@'):

            move = self.move_mega_automata(S, c)

            if move == []:
                
                nodos_reconocidos = []
                for s in S:
                    # se encuentra el nodo con mayor prioridad
                    if s.final_yalex:
                        nodos_reconocidos.append(s.valor_diccionario)

                if len(nodos_reconocidos) > 0 and nodos_reconocidos[0] != []:
                    temp = nodos_reconocidos
                else:
                    temp = [temp]

                S = self.e_closure(self.nodos[0])
                texto_reconocido.append(temp2)
                reconocidos.append(temp)
                temp = ''
                temp2 = ''

                move = self.move_mega_automata(S, c)
            
            temp += c
            temp2 += c
            
            S = self.e_closure(move)
            c = self.sigCar(expresion)

        if len(reconocidos) > 0:
            return True, reconocidos, texto_reconocido
        else:
            return False, [], False


    def simulacionAFD(self):

        expresion = [caracter for caracter in self.expresion]

        transiciones = []
        for simbolo in expresion:
            if simbolo not in self.alfabeto:
                print("\n\tLa expresion no pertenece al alfabeto")
                return False
            
            transiciones.append(simbolo)
        
        actual = self.nodos[0]
        movimientos = ""

        for simbolo in transiciones:
            if actual.get_transition_valor(simbolo):
                movimientos+= "\n\t\t "+str(actual.conteo)+" -> "+str(simbolo)+" -> "+str(actual.get_transition_valor(simbolo).conteo)+"\n"
                actual = actual.get_transition_valor(simbolo)
            else:
                return False
            
            
        return actual.final, movimientos

    
    
        
