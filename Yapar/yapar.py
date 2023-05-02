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

    def getSimbolosGramaticales(self):
        simbolos = []
        for key in self.gramatica:
            simbolos.append(key)
            for produccion in self.gramatica[key]:
                for simbolo in produccion:
                    if simbolo not in simbolos:
                        simbolos.append(simbolo)
        return simbolos
    
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

        return J

    def ir_a(self, I, X):
        J = []
        
        existe = False
        for elemento in I.copy():
            partes = elemento.split(" -> ")

            derecha_expresion = partes[1].split(' ')
            for elemento in derecha_expresion:
                if elemento == '•':
                    # si el punto esta al final de la expresion no se hace nada
                    if derecha_expresion.index(elemento) == len(derecha_expresion)-1:
                        pass
                    
                    else:
                        index = derecha_expresion.index(elemento)
                        punto = derecha_expresion[index+1]

                        if punto == X:
                            existe = True

                            # Se agrega el elemento a J con el punto desplazado una posición a la derecha
                            derecha_expresion[index] = punto
                            derecha_expresion[index+1] = '•'

                            string = ' '.join(derecha_expresion)
                            J.append(partes[0] + ' -> ' + string)
                            break

        if not existe:
            return [], []
        
        return J, self.cerradura(J)

    def getNodo(self, nodos, contenido):
        for nodo in nodos.copy():
            if set(nodo.contenido) == set(contenido):
                return nodo
        return None

    def getArbol(self):

        G = gv.Digraph(format='png', graph_attr={'rankdir':'LR', 'shape':'square'})
        

        # Se pone al primer elemento de la gramatica como el corazon y se le agrega un punto
        corazon = list(self.gramatica.keys())[0] + ' -> • ' + ' '.join(self.gramatica[list(self.gramatica.keys())[0]][0])
        C = [self.cerradura([corazon])]
       
        nodos = []
        nodoI = N(corazon, C[0])
        nodos.append(nodoI)

        while True:
            agregados = 0
            copia_C = C.copy()

            for i in copia_C:
                nodo_i = self.getNodo(nodos, i)

                for simbolo in self.simbolosG:
                    CORAZON, CERRADURA = self.ir_a(i, simbolo)

                    if len(CERRADURA) == 0 and len(CORAZON) == 0:
                        continue

                    if CERRADURA not in C:
                        
                        nodo_nuevo = N(CORAZON, CERRADURA)
                        nodos.append(nodo_nuevo)

                        # crear transicion 
                        nodo_i.createTransicion(nodo_nuevo, simbolo)

                        C.append(CERRADURA)
                        agregados += 1

                    else:
                        nodo_n = self.getNodo(nodos, CERRADURA)
                        nodo_i.createTransicion(nodo_n, simbolo)

                    temp_cerradura = ''
                    for e in CERRADURA:
                        if e not in CORAZON:
                            temp_cerradura += e + '\n'
 
            if agregados == 0:
                break

        for n in nodos.copy():
            G.node(n.nombre, shape='box')
            for key, value in n.transicion.items():
                G.edge(n.nombre, key.nombre, label=value)

        G.render("test-output/prueba.gv", view=True)

class N(object):
    def __init__(self, corazon, resto, transicion = None):
        self.corazon = corazon
        self.resto = resto
        self.nombre = self.getNombre()
        self.contenido = self.getContenido()
        self.transicion = {}

    def createTransicion(self, simbolo, nodo):
        self.transicion[simbolo] = nodo
    
    def getNombre(self):
        str = ''
        
        if type(self.corazon) == list:
            for elemento in self.corazon:
                str += elemento + '\n'
        
        else:
            str += self.corazon

        str += '\n=====================\n'
        
        for elemento in self.resto:
            if elemento in self.corazon:
                continue
            str += elemento + '\n'
            # str += elemento + '\n'
        return str
    
    def getContenido(self):
        contenido = []
        if type(self.corazon) == list:
            for elemento in self.corazon:
                contenido.append(elemento)
        
        else:
            contenido.append(self.corazon)
        
        for elemento in self.resto:
            contenido.append(elemento)

        return contenido
    


yap = YAPAR('./slr-1.txt')