from thompson import *

class Minimizacion(object):
    def __init__(self, nodos, alfabeto):
        self.nodos = nodos
        self.alfabeto = alfabeto
        self.tabla = self.crear_tabla()
        self.minimizado = self.minimizar()

    def crear_tabla(self):
        tabla = {}
        for nodo in self.nodos:
            tabla[nodo.conteo] = {}
            for letra in self.alfabeto:
                if not nodo.get_transition_valor(letra):
                    tabla[nodo.conteo][letra] = None
                else:
                    tabla[nodo.conteo][letra] = nodo.get_transition_valor(letra).conteo
        return tabla
    
    def getNodo(self, conteo):
        for nodo in self.nodos:
            if nodo.conteo == conteo:
                return nodo
            
    def getNuevosNodos(self, nodos,  conteo):
        for nodo in nodos:
            if nodo.conteo == conteo:
                return nodo
    
    def particionar(self, particion, particiones_completas):
        temp = {}
        for transicion in self.tabla:
            if transicion in particion:
                temp[transicion] = {}
                for letra in self.alfabeto:
                    if self.tabla[transicion][letra] in particion:
                        temp[transicion][letra] = particion
                    elif self.tabla[transicion][letra] == None:
                        temp[transicion][letra] = 'ERROR'
                    else:
                        temp[transicion][letra] = [self.tabla[transicion][letra]] if type(self.tabla[transicion][letra]) != list else self.tabla[transicion][letra]
        

        tabla = {}
        for elemento in temp:
            transiciones = []
            for letra in temp[elemento]:
                transiciones.append(temp[elemento][letra])
            tabla[elemento] = transiciones

        particion_nueva = []

        for elemento in tabla:
            p = [elemento]

            for transicion in tabla:
                if transicion != elemento:
                    if tabla[elemento] == tabla[transicion]:
                        p.append(transicion)
            
            # revisar si p esta en particion_nueva, sin importar el orden de los elementos

            esta = False
            for part in particion_nueva:
                if elemento in part:
                    esta = True
                    break

            if not esta:
                particion_nueva.append(p)
        
        return ([*particion_nueva]) if particion_nueva == particion else particion_nueva


    
    def minimizar(self):
        nodos_aceptacion = []
        nodos_no_aceptacion = []

        for nodo in self.nodos:
            if nodo.final:
                nodos_aceptacion.append(nodo.conteo)
            else:
                nodos_no_aceptacion.append(nodo.conteo)
        
        particion_inicial = [nodos_aceptacion, nodos_no_aceptacion]

        particiones = particion_inicial


        while True:
            particion_nueva = []

            for particion in particiones:
                
                if len(particion) != 1:
                    nuevas = self.particionar(particion, particiones)
                    for nueva in nuevas:
                        if nueva not in particion_nueva:
                            particion_nueva.append(nueva)
                else:
                    particion_nueva.append(particion)
                    
            if particion_nueva == particiones:
                break
            particiones = particion_nueva

        # crear nuevos nodos
        nuevos_nodos = []
        conteo = 0
        for particion in particiones:

            nuevos_nodos.append(Nodo(particion[0], inicial = self.getNodo(particion[0]).inicial, final = self.getNodo(particion[0]).final))
            conteo += 1

        # crear tabla de transiciones de los nuevos nodos utilizando la informacion de particiones y self.tabla
        for particion in particiones:
            for nodo in nuevos_nodos:
                if nodo.conteo == particion[0]:
                    for letra in self.alfabeto:
                        if self.tabla[particion[0]][letra] != None:
                            
                            valor_particion = ''
                            for particion2 in particiones:
                                if self.tabla[particion[0]][letra] in particion2:
                                    valor_particion = particion2[0]
                                    break

                            nodo.addTransition(self.getNuevosNodos(nuevos_nodos, valor_particion), letra)
                    break
        
        return nuevos_nodos





