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
        simbolos_aceptados = []

        for nodo in nodos:
            for s_nodo, valor in nodo.transicion.items():
                simbolo = [simbolo] if type(simbolo) != list else simbolo
                if valor == simbolo:
                    simbolos_aceptados.append(simbolo)
                    self.visitados[s_nodo] = True
                    n_nodos.append(s_nodo)

        return n_nodos, simbolos_aceptados
    
    def simulacionAFN_YALEX(self, expresion):
        self.contador = 0
        expresion = [caracter for caracter in expresion]
        expresion.append('#') # Se agrega el simbolo de fin de cadena

        S = self.e_closure(self.nodos[0])
        c = self.sigCar(expresion)

        simbolos_aceptados = []

        while (c != '#'):
            move, aceptados = self.move_mega_automata(S, c)
            S = self.e_closure(move)
            c = self.sigCar(expresion)
            simbolos_aceptados.append(aceptados)

        reconocidos = []
        for s in S:
            if s.final_yalex:
                reconocidos.append(s.valor_diccionario)
            

        if len(reconocidos) > 0:
            return True, reconocidos
        else:
            return False, False


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

    
    
        
