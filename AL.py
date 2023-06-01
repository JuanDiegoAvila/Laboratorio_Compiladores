
import pickle
from comunicador import Comunicador

None

class AL(object):
    def __init__(self):
        self.output = []
        self.error = False
        self.actual = 0
        self.next = False
        self.aceptar = False
        self.cantidad_lineas = self.cantidadLineas()
        self.linea_actual = 1

        # Cargar el archivo con el arreglo nodos
        self.nodos = None
        with open('./Yalex/pickle/nodos.pickle', 'rb') as f:
            self.nodos = pickle.load(f)

        self.YALEX = None
        with open('./Yalex/pickle/YALEX.pickle', 'rb') as f:
            self.YALEX = pickle.load(f)

        self.simulacion = None
        with open('./Yalex/pickle/simulacion.pickle', 'rb') as f:
            self.simulacion = pickle.load(f)

        self.rules = self.YALEX.rules
        self.tokens =  self.YALEX.tokens
        self.token_keys = self.tokens.keys()
        self.suma_puntero = 0

    def cantidadLineas(self):
        cantidad_lineas = 0
        with open('./Yapar/entrada1.txt') as file:
            for line in file:
                cantidad_lineas += 1
        return cantidad_lineas


    def getNext(self):
        self.next = True
        self.analizador_lexico()

        if 'Error' in self.output[0]:
            print(self.output[0])
            self.output = []
            self.error = True
            self.analizador_lexico()

        if self.output[0] == 'cambio de linea':
            self.output = []
            self.analizador_lexico()

        temp = self.output[0].replace(' ', '')
        print(temp)
        return temp
        

    def analizador_lexico(self):

        # Hacer la simulacion de el automata con cada cadena de entrada
        cantidad_lineas = 1
        termino = False


        with open('./Yapar/entrada1.txt') as file:
            
            for line in file:
            
                if self.simulacion.linea == cantidad_lineas:
                    line = line.replace('\n', ' \n')
                    puntero = self.simulacion.getPuntero()
                
                    self.suma_puntero += puntero

                    # agarrar la linea a partir del puntero 
                    linea = line[self.suma_puntero:]


                    if linea == ' \n':
                        self.linea_actual += 1
                        self.simulacion.linea += 1
                        self.output = ['cambio de linea']
                        self.suma_puntero = 0
                        self.simulacion.setPuntero(0)

                        if self.linea_actual > self.cantidad_lineas:
                            self.output = ['$']

                        return
                        

                    self.simulacion.setEntrada(linea, self.tokens.keys(), self.rules)

                    token, termino = self.simulacion.simulacionAFN_YALEX_PUNTERO()
                    
                    if token != None:
                        self.output = token
                
                cantidad_lineas += 1
    

None
