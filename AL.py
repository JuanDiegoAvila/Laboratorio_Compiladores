
import pickle
from comunicador import Comunicador

None

class AL(object):
    def __init__(self):
        self.output = []
        self.actual = 0
        self.next = False

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

        

    def getNext(self):
        self.next = True
        self.analizador_lexico()

        if 'Error' in self.output[0]:
            print(self.output[0])
            exit()

        temp = self.output[0].replace(' ', '')
        
        return temp
        


    def analizador_lexico(self):

        # Hacer la simulacion de el automata con cada cadena de entrada

        with open('./Yapar/entrada1.txt') as file:
            
            for line in file:
                line = line
                puntero = self.simulacion.getPuntero()
                # puntero = puntero -1 if puntero > 0 else puntero
                
                
                self.suma_puntero += puntero

                # agarrar la linea a partir del puntero 
                linea = line[self.suma_puntero:]

                self.simulacion.setEntrada(linea,  self.tokens.keys(),  self.rules)

                token, termino =  self.simulacion.simulacionAFN_YALEX_PUNTERO()
                
                if token != None:
                    self.output = token
                
                if termino:
                    self.output = ['$']
    

None
