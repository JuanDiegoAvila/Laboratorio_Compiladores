class Subconjuntos(object):
    def __init__(self, thompson):
        self.thompson = thompson
        self.nodos = thompson.visitados