import re
import graphviz as gv

class N(object):
    def __init__(self, corazon, resto, transicion = None):
        self.estado = ''
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

class Yapar(object):

    def  __init__(self, path):
        self.path = path
        self.tokens = []
        self.ignored = []
        self.gramatica = {}
        
        self.getTokens()
        self.getGrammar()
        self.gramaticaList = self.getGramaticaList()
        
        self.simbolosG = self.getSimbolosGramaticales()
        self.arbol = self.getArbol()

        self.getTabla()
        
    def checkErrors(self, yalex_rules):

        values = []
        for key in yalex_rules:
            temp = yalex_rules[key]
            temp = temp.replace(' ', '')
            values.append(temp)

        # verificar que los tokens sean los mismos que en la gramatica
        for key in self.tokens:
            if key not in values and key != 'ε' and key not in self.ignored:
                print('Error: El token ' + key + ' no esta en la gramatica')
                exit(0)

        # verificar que no hay mas tokens en la gramatica que en el yalex, exceptuando los tokens ignorados
        contador = 0
        len_values = len(values)
        for key in self.tokens:
            if key not in self.ignored:
                contador += 1
        if contador != len_values:
            print('Error: La cantidad de tokens no coincide con la gramatica')
            exit(0)


        # verificar que los tokens esten escritos en mayusculas
        for key in self.tokens:
            if key != key.upper() and key != 'ε':
                print('Error: El token ' + key + ' no es valido')
                exit(0)
        
    def getTokens(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            data = f.read()

        if '%%' not in data:
            print('Error: No se encontro el separador %%')
            exit()
            
        with open(self.path, 'r', encoding='utf-8') as f:
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
        
        if self.tokens == []:
            print('Error: No se encontraron tokens')
            exit()

        self.tokens.append('ε')

    def getGrammar(self):
        gramatica = {}

        with open(self.path, 'r', encoding='utf-8') as f:
            data = f.read()

            data = data.split('%%')[1]
            data = data.replace('\n', ' ')
            data = data.replace('\t', ' ')

            # replace more than two spaces with only one
            data = re.sub(' +', ' ', data)

        # revisar errores de sintaxis en data
        dos_puntos = data.count(':')
        punto_coma = data.count(';')

        if dos_puntos > punto_coma:
            print('Error: No hay la misma cantidad de ; que de :')
            exit()

        if dos_puntos < punto_coma:
            print('Error: No hay la misma cantidad de : que de ;')
            exit()

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

            if key in self.tokens:
                # no puede haber un terminal en la cabeza de una produccion
                print('Error: No puede haber un terminal en la cabeza de una produccion')
                exit()

    def getSimbolosGramaticales(self):
        simbolos = []
        for key in self.gramatica:
            if key not in simbolos:
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
                    
                    # si el corazoon tiene la forma X -> ε • ignorarlo

                    if len(CERRADURA) == 0 and len(CORAZON) == 0:
                        continue
                    
                    # print(CORAZON)
                    # prueba = CORAZON[0].split('->')
                    # if prueba[1] == ' ε •':
                    #     continue

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

        contador = 0
        for n in nodos.copy():
            n.estado = 'I' + str(contador) 
            contador += 1

            n.nombre = n.estado + '\n' + n.nombre

        for n in nodos.copy():
            # si el nombre del nodo tiene la forma X -> ε • ignorarlo
            match = re.search(r'ε •', n.nombre)
            if match:
                continue

            G.node(n.nombre, shape='box')
            for key, value in n.transicion.items():
                
                if value == 'ε':
                    continue
            
                G.edge(n.nombre, key.nombre, label=value)
            
            # if n.estado == 'I1':
            # si el corazon del elemento tiene S' -> S •
           
            if list(self.gramatica.keys())[0] + ' -> ' + ' '.join(self.gramatica[list(self.gramatica.keys())[0]][0]) + ' •' in n.corazon:
            
                # agregar un nodo que tenga el texto de aceptacion y crear una transicion a el con $
                nodo_aceptacion = N('Aceptacion', ['Aceptacion'])
                nodo_aceptacion.nombre = 'Aceptacion'

                n.createTransicion(nodo_aceptacion, '$')

                nodos.append(nodo_aceptacion)
                G.node(nodo_aceptacion.nombre, shape='plaintext')
                G.edge(n.nombre, nodo_aceptacion.nombre, label='$')

        self.nodos = nodos

        # G.render("test-output/prueba.gv", view=True)

    def primero(self, simbolo):
        primeros = []

        # si es un terminal
        if simbolo in self.tokens:
            return [simbolo]

        else:
            # si se tiene la produccion X -> ε
            if simbolo in self.gramatica.keys() and self.gramatica[simbolo] == [['ε']]:
                primeros.append('ε')

            # si se tiene la produccion X -> Y1Y2...Yn
            else:
                
                for produccion in self.gramatica[simbolo]:
                    
                    if produccion[0] != simbolo:
                        n_primero = self.primero(produccion[0])
                        contador = 0
                        
                        while('ε' in n_primero and contador < len(produccion)-1):
                            contador += 1
                            n_primero.remove('ε')
                            n_primero += self.primero(produccion[contador])

                        
                        # aplanar la lista
                        if type(n_primero) == list:
                            for e in n_primero:
                                if e not in primeros:
                                    primeros.append(e)
                        else:
                            if n_primero not in primeros:
                                primeros.append(n_primero)
        return primeros
    
    def siguiente(self, simbolo):
        siguientes = []
        
        if simbolo == self.gramatica[list(self.gramatica.keys())[0]][0][0]:
            siguientes.append('$')
        
        for key in self.gramatica:
            for produccion in self.gramatica[key]:
                for elemento in produccion:
                    if elemento == simbolo:
                        index = produccion.index(elemento)
                        if index == len(produccion)-1:
                            if key == simbolo:
                                continue
                            else:
                                n_siguientes = self.siguiente(key)
                                for e in n_siguientes:
                                    if e != 'ε' and e not in siguientes:
                                        siguientes.append(e)
                        else:
                            
                            recorridos = 0
                            epsilons = 0
                        
                            for i in range(index+1, len(produccion)):
                                recorridos += 1
                                n_primeros = self.primero(produccion[i])
                                
                                if 'ε' in n_primeros:
                                    epsilons +=1 

                                for e in n_primeros:
                                    if e != 'ε' and e not in siguientes:
                                        siguientes.append(e)
                                    
                                if 'ε' not in n_primeros:
                                    break
                            
                            if recorridos == epsilons:
                                n_siguientes = self.siguiente(key)
                                for e in n_siguientes:
                                    if e != 'ε' and e not in siguientes:
                                        siguientes.append(e)

        return siguientes

    def getPS(self):
        primeros = {}
        siguientes = {}

        for key in self.gramatica:
            primeros[key] = self.primero(key)

            if "'" in key:
                siguientes[key] = self.siguiente(key.replace("'", ""))
            else:
                siguientes[key] = self.siguiente(key)

        print("primeros: ", primeros)
        print("siguientes: ", siguientes)
        return None
    
    def getGramaticaList(self):
        conteo = 0
        gramatica_list = {}
        for key, value in self.gramatica.items():
            # if conteo == 0:
            #     for values in value: 
            #         produccion = key + ' -> ' + ' '.join(values)
            #         gramatica_list[conteo] = produccion
            #         conteo += 1
            # else:
                for values in value:
                    produccion = key + ' -> ' + ' '.join(values)

                    gramatica_list[conteo] = produccion
                    conteo += 1
        
        return gramatica_list

    
    def getTabla(self):
        C = {}
        for nodo in self.nodos:
            if nodo.estado != '':
                C[nodo.estado] = nodo

        # 2.- 
        # a) Si [A -> α • aβ] está en Ii y GOTO(Ii, a) = Ij entonces M[i, a] = “desplazar j”
        # b) Si [A -> α •] está en Ii entonces M[i, a] = “reducir A -> α" para toda a en SIGUIENTE(A)
        # c) Si [S' -> S •] está en Ii entonces M[i, $] = “aceptar”
        # 3.-
        # Las transiciones de GOTO para el estado i se construyen para todos los no terminales A usando la regla
        # si GOTO(Ii, A) = Ij entonces M[i, A] = j
        # 4.- Si no se cumple con las reglas 2 y 3 se deja como error
        # 5.- El estado inicial es I0, que contiene el item S' -> • S

        # ACCEPT
        tabla_accion = {}
        for nodo in self.nodos.copy():
            estado = nodo.estado.replace('I', '')

            if estado not in tabla_accion and nodo.estado != '':
                tabla_accion[estado] = {}
            
            # si tiene la transicion $ entonces es aceptacion
            for key, value in nodo.transicion.items():
                if '$' == value:
                    
                    tabla_accion[estado]['$'] = 'aceptar'


        # DESPLAZAR
        for nodo in self.nodos.copy():
            # Si [A -> α • aβ] está en Ii y GOTO(Ii, a) = Ij entonces M[i, a] = “desplazar j”
            for key, value in nodo.transicion.items():
                if value in self.tokens and value != 'ε':
                    estado = nodo.estado.replace('I', '')
                    if estado not in tabla_accion:
                        tabla_accion[estado] = {}

                    tabla_accion[estado][value] = 's'+ key.estado.replace('I', '')
        
        

        # REDUCIR
        for nodo in self.nodos.copy():
            # Si [A -> α •] está en Ii entonces M[i, a] = “reducir A -> α" para toda a en SIGUIENTE(A)
            if nodo.estado != '':
                corazon = nodo.corazon
                if type(corazon) != list:
                    corazon = [corazon]

                for produccion in corazon:
                    partes = produccion.split(' -> ')
                    izquierda = partes[0]
                    derecha = partes[1].split(' ')

                    if '•' in derecha[len(derecha)-1]:
                        siguiente = self.siguiente(izquierda)
                        for simbolo in siguiente:
                            if simbolo != 'ε':
                                pass

                            for key, value in self.gramaticaList.items():
                                
                                prod_temp = derecha.copy()
                                prod_temp.remove('•')

                                if izquierda + ' -> ' + ' '.join(prod_temp) == value:
                                    if simbolo not in tabla_accion[nodo.estado.replace('I', '')]:
                                        tabla_accion[nodo.estado.replace('I', '')][simbolo] = 'r' + str(key)
                                    else:
                                        # si hay un match con r en el espacio es error de reduccion/reduccion
                                        if simbolo in tabla_accion[nodo.estado.replace('I', '')] and [nodo.estado.replace('I', '')][simbolo][0] == 'r':
                                            print('Error: Conflicto en la tabla de analisis. Error reduccion/reduccion')

                                        elif simbolo in tabla_accion[nodo.estado.replace('I', '')] and  tabla_accion[nodo.estado.replace('I', '')][simbolo][0] == 's':
                                            print('Error: Conflicto en la tabla de analisis. Error reduccion/desplazamiento')
                                        exit(0)
                                    break

        # self.imprimirTabla(tabla_accion)
        # GOTO
        tabla_goto = {}
        for nodo in self.nodos.copy():
            for key, value in nodo.transicion.items():
                if value not in self.tokens and value != 'ε' and value != '$':
                    estado = nodo.estado.replace('I', '')
                    if estado not in tabla_goto:
                        tabla_goto[estado] = {}

                    tabla_goto[estado][value] = key.estado.replace('I', '')

        # self.imprimirTabla(tabla_goto)

        self.tabla_analisis = {}
        self.tabla_analisis['accion'] = tabla_accion
        self.tabla_analisis['ir_A'] = tabla_goto
                                    
    def imprimirTabla(self, tabla):
        
        for key, value in tabla.items():
            print(key, value)

        return None