import re
import graphviz as gv

class YAPAR(object):

    def  __init__(self, path):
        self.path = path
        self.tokens = []
        self.ignored = []
        self.gramatica = {}
        
        self.getTokens()
        self.getGrammar()
        
        self.simbolosG = self.getSimbolosGramaticales()
        self.arbol = self.getArbol()

    def getTokens(self):
        with open(self.path, 'r') as f:
            for line in f:

                if line.startswith('%token'):
                    ln = line.split(' ')
                    tokens = ln[1:]
                    for token in tokens:
                        self.tokens.append(token.strip('\n'))

                if line.startswith('IGNORE'):
                    ln = line.split(' ')
                    tokens = ln[1:]
                    for token in tokens:
                        self.ignored.append(token.strip('\n'))

    def getGrammar(self):
        gramatica = {}

        with open(self.path, 'r') as f:
            data = f.read()

            data = data.split('%%')[1]
            data = data.replace('\n', ' ')
            data = data.replace('\t', ' ')

            # replace more than two spaces with only one
            data = re.sub(' +', ' ', data)

        expresiones = []

        for line in data.split(';'):
            expresiones.append(line.strip())

        # eliminar elementos vacios
        expresiones = list(filter(None, expresiones))
        
        for expresion in expresiones:
            ex = expresion.split(':')
            terminos = ex[1].split('|')
            
            gramatica[ex[0].strip()] = []

            for termino in terminos:
                gramatica[ex[0].strip()].append(termino.split(' '))

        # eliminar elementos vacios de la gramatica
        for key in gramatica:
            gramatica[key] = list(filter(None, gramatica[key]))
            for i in range(len(gramatica[key])):
                gramatica[key][i] = list(filter(None, gramatica[key][i]))

        # se crea la gramatica aumentada agregando S' -> S en terminos de la gramatica 
        primer_key = list(gramatica.keys())[0]+ "'"
        self.gramatica[primer_key] = [[list(gramatica.keys())[0]]]

        for key in gramatica:
            self.gramatica[key] = gramatica[key]

    def cerradura(self, I):
        J = I.copy()

        while True:
            punto = None
            # Buscar el elemento que tiene el punto antes en J
            for elemento in J:
                lista = elemento.split(' ')
                for expresion in lista:
                    if expresion == '•':

                        # si el punto esta al final de la expresion no se hace nada
                        if lista.index(expresion) == len(lista)-1:
                            break

                        index = lista.index(expresion)
                        punto = lista[index+1]


            # punto = punto.replace('•', '')
            
            # Buscar las producciones del elemento con punto
            producciones = []

            for key in self.gramatica.copy():
                if key == punto:
                    producciones = self.gramatica[key].copy()

            # Se ponen las producciones en el formato de B -> •y
            for i in range(len(producciones)):
                # si es lista hacer la produccion un string 
                if type(producciones[i]) == list:
                    string = ' '.join(producciones[i])
                else:
                    string = producciones[i]

                producciones[i] = punto + ' -> ' + '• ' + string
     
            # Agregar las producciones a J si no estan
            agregados = 0
            for produccion in producciones:
                if produccion not in J:
                    agregados += 1
                    J.append(produccion)

            if agregados == 0:
                break
        
        for elemento in J.copy():
            if elemento in I:
                J.remove(elemento)

        return J

    def getSimbolosGramaticales(self):
        simbolos = []
        for key in self.gramatica:
            simbolos.append(key)
            for produccion in self.gramatica[key]:
                for simbolo in produccion:
                    if simbolo not in simbolos:
                        simbolos.append(simbolo)
        return simbolos
    
    def ir_a(self, I, X):

        # se busca las producciones que tengan a X como el elemento que sigue al punto
        # y se desplaza el punto una posición a la derecha
        # se hace la cerradura de las producciones encontradas para encontrar el resto de elementos del conjunto
        J = []
        for elemento in I.copy():
            partes = elemento.split(" -> ")

            derecha_expresion = partes[1].split(' ')

            for elemento in derecha_expresion:
                if elemento == '•':
                    # si el punto esta al final de la expresion no se hace nada
                    if derecha_expresion.index(elemento) == len(derecha_expresion)-1:
                        return [], []
                    
                    index = derecha_expresion.index(elemento)
                    punto = derecha_expresion[index+1]


            # Buscar las producciones del elemento que tengan tambien a X como el elemento que sigue al punto
            
            producciones = []
            for key in self.gramatica.copy():
                for produccion in self.gramatica[key]:
                    nuevo = key + ' -> ' + ' '.join(produccion)
                    nuevo = nuevo.split(' ')

                    if len (produccion) > 1:
                        if produccion[0] == punto and produccion[0] == X:
                            producciones.append(nuevo)
                    else:
                        if produccion[0] == punto and produccion[0] == X:
                            producciones.append(nuevo)

            for produccion in producciones:
                
                # se busca los elementos luego del -> en la produccion
                derecha = produccion[2:]

                # se coloca el punto luego del elemento X en la produccion
                for elemento in derecha:
                    if elemento == X:
                        index = derecha.index(elemento)
                        
                        # se agrega un nuevo elemento en el index + 1
                        derecha.insert(index+1, '•')

                produccion = produccion[0] + ' -> ' + ' '.join(derecha)

                if produccion not in J:
                    J.append(produccion)

        if len(J) > 0:
            return J, self.cerradura(J)
        else:
            return [], []

    def getNodo(self, nodos, corazon):
        for nodo in nodos.copy():
            if type(corazon) != list:
                corazon = [corazon]
            if nodo.corazon == corazon:
                return nodo
        return None


    def getArbol(self):

        G = gv.Digraph(format='png', graph_attr={'rankdir':'LR', 'shape':'square'})
        nodos = []

        # Se pone al primer elemento de la gramatica como el corazon y se le agrega un punto
        corazon = list(self.gramatica.keys())[0] + ' -> • ' + ' '.join(self.gramatica[list(self.gramatica.keys())[0]][0])
        C = [self.cerradura([corazon])]

        str_1 = corazon + '\n================================\n' + '\n'.join(C[0])
        G.node(str_1, shape='box')
         
        # primero = N([corazon], C)
        # nodos.append(primero)

        while True:
            agregados = 0
            for i in C.copy():
                for simbolo in self.simbolosG:
                    CORAZON, RESTO = self.ir_a(i, simbolo)

                    if len(CORAZON) > 0 or len(RESTO) > 0:
                        print(CORAZON)
                        print(RESTO)
                        str_temp = '\n'.join(CORAZON) + '\n================================\n' + '\n'.join(RESTO)
                        G.node(str_temp, shape='box')

                        # nuevo = N(CORAZON, RESTO)
                        
                        # nodos.append(nuevo)
                    
                        # # se crea la transicion del nodo actual al nuevo nodo
                        # nodo = self.getNodo(nodos, corazon)
                        # if nodo != None:
                        #     nodo.createTransicion(simbolo, nuevo)

                        # corazon = CORAZON

                        if CORAZON+RESTO not in C:
                            C.append(CORAZON+RESTO)
                            print(C)
                            input()
                            agregados += 1
                        
            if agregados == 0:
                break
        
        print(C)


        G.render("test-output/prueba.gv", view=True)

class N(object):
    def __init__(self, corazon, resto, transicion = None):
        self.corazon = corazon
        self.resto = resto
        self.nombre = self.getNombre()
        self.transicion = {}

    def createTransicion(self, simbolo, nodo):
        self.transicion[simbolo] = nodo
    
    def getNombre(self):
        str = ''
        for elemento in self.corazon:
            str += elemento + '\n'

        str += '\n=====================\n'
        
        for elemento in self.resto:
            str += elemento + '\n'
        return str
    

    def __str__(self):
        return self.nombre
    
    def __repr__(self):
        return self.nombre



yap = YAPAR('./slr-1.txt')