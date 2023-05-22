import json

class Comunicador(object):
    def __init__(self):
        self.tokens = []
        self.actual = ''

        self.enviado = False
        self.termino = False
        self.inicio = False

        self.mensaje = ''

        self.path_archivo = './comunicacion.json'

    def recibir(self):
        with open(self.path_archivo, 'r') as f:
            data = json.load(f)
            self.mensaje = data['mensaje']

    def cambiar(self):
        with open(self.path_archivo, 'w') as f:
            data = {}
            data['mensaje'] = ''
            data['otro'] = True
            data['termino'] = False
            json.dump(data, f)

    def enviar(self, mensaje):
        with open(self.path_archivo, 'w') as f:
            data = {}
            data['mensaje'] = mensaje
            data['otro'] = False
            data['termino'] = False
            json.dump(data, f)

    def otro(self):
        with open(self.path_archivo, 'r') as f:
            data = json.load(f)
            return data.get('otro', False)

    def terminar(self):
        with open(self.path_archivo, 'w') as f:
            data = {}
            data['termino'] = True
            json.dump(data, f)

    def getTerminar(self):
        with open(self.path_archivo, 'r') as f:
            data = json.load(f)
            return data.get('termino', False)

    def iniciar(self):
        with open(self.path_archivo, 'w') as f:
            data = {}
            data['inicio'] = True
            data['termino'] = False
            data['mensaje'] = ''

            json.dump(data, f)

    def getInicio(self):
        with open(self.path_archivo, 'r') as f:
            data = json.load(f)
            return data.get('inicio', False)
