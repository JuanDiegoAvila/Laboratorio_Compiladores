
import pickle
from comunicador import Comunicador

None

class AL(object):
    def __init__(self):
        self.output = []
        self.actual = 0
        self.next = False
        

    def getNext(self):
    
        self.analizador_lexico()
        self.next = True
        self.actual += 1

        while(self.output == []):
            self.analizador_lexico()
            self.actual += 1

        temp = self.output[0].replace(' ', '')
        print(temp)
        return temp
        


    def analizador_lexico(self):

        # Cargar el archivo con el arreglo nodos
        nodos = None
        with open('./Yalex/pickle/nodos.pickle', 'rb') as f:
            nodos = pickle.load(f)

        YALEX = None
        with open('./Yalex/pickle/YALEX.pickle', 'rb') as f:
            YALEX = pickle.load(f)

        simulacion = None
        with open('./Yalex/pickle/simulacion.pickle', 'rb') as f:
            simulacion = pickle.load(f)


        rules = YALEX.rules
        tokens = YALEX.tokens

        token_keys = tokens.keys()


        # Hacer la simulacion de el automata con cada cadena de entrada

        with open('./Yapar/entrada1.txt', 'r') as file:
            output = []
            count_lineas = 0
            expresion = ''
            
            for line in file:
                count_lineas += 1
                line = line + ' '
            
                # se simula la expresion completa
                result, aceptado, texto_reconocido = simulacion.simulacionAFN_YALEX(line)
                
                indice = 0
                # for a in aceptado:
                if self.actual >= len(aceptado):
                    self.output = ['$']
                    return

                a = aceptado[self.actual]

                for token in a:
                    existe = False

                    for key, value in rules.items():
                        if texto_reconocido[indice] == key:
                            if value != '':
                                output.append(value)
                                existe = True

                            break

                        if token == key and not existe:
                            if value != '':
                                output.append(value)
                                existe = True

                            break
                            
                
                    if not existe and token not in token_keys and token != '':
                        posicion = 0
                        for i in range(indice):
                            posicion += len(texto_reconocido[i])

                        string = 'Error lexico en la linea '+ str(count_lineas) +' en la posicion ' + str(posicion)+': ' + repr(token) + ' no es un token valido'
                        output.append(string)
                        print(string)
                        
                indice += 1
            
            self.output = output

            # escribir archivo con todos los elementos de output
            with open('./Yalex/Output.txt', 'w', encoding='utf-8') as file:
                for i in output:
                    file.write(i + "\n")

    

None
