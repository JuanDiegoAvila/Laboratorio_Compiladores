class Arbol(object):
    def __init__(self, expresion):
        self.expresion = expresion
        self.stack = self.expresion_stack()

    def expresion_stack(self):
        stack = ([*self.expresion])
        stack.reverse()
        return stack


class Rama(object):
    def __init__(self, r, izq = None, der = None, valor = False):
        self.r = r
        self.izq = izq
        self.der = der
        self.valor = valor