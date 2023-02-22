
class Postfix():
    def __init__(self, expresion):
        self.stack = []
        self.output = []
        self.operators = {
            '*': 4,
            '+': 4,
            '?': 4,
            '.': 3,
            '|': 2,
            '#': 1,
            '(': 1
        }

        self.binary_operators = '|.'
        self.unary_operators = '*+?'

        self.error_check(expresion)

        self.expresion = self.concat_expression(expresion)
        self.output = self.convert()
        self.final = ''.join(self.output)
        self.final = self.final.replace('?', 'ε|')

    def error_check(self, expresion):
        
        parentesis_izq = 0
        parentesis_der = 0
        
        inicio = "\n==============================================================================================\n"
        final = "=============================================================================================="

        if self.is_operator(expresion[0]) and expresion[0] not in '()':
            error = "\tError: La expresión regular ingresada es incorrecta. \n\tNo puede iniciar con un operador.\n"
            raise Exception(inicio + error + final)

        if len(expresion) == 0:
            error = "\tError: La expresión regular ingresada es incorrecta. \n\tNo se ingresó ninguna expresión.\n"
            raise Exception(inicio + error + final)

        for char in expresion:
            if char == ' ':
                error = "\tError: La expresión regular ingresada es incorrecta. \n\tNo puede haber espacios en blanco.\n"
                raise Exception(inicio + error + final)
            elif char == '(':
                parentesis_izq += 1
            elif char == ')':
                parentesis_der += 1
                if parentesis_izq == 0 or parentesis_der > parentesis_izq:
                    error = "\tError: La expresión regular ingresada es incorrecta. \n\tNo hay un '(' que iguale un parentesis ')'. \n"
                    raise Exception(inicio + error + final)
            elif char == '|':
                if self.is_operator(expresion[expresion.index(char)+1]):
                    error = "\tError: La expresión regular ingresada es incorrecta. \n\tNo puede haber un operador seguido de |.\n"
                    raise Exception(inicio + error + final)
            elif char == '+' and ( not self.is_operand(expresion[expresion.index(char)-1]) and expresion[expresion.index(char)-1] != ')'):
                error = "\tError: La expresión regular ingresada es incorrecta. \n\tEl operador + no se está aplicando a ningín símbolo.\n"
                raise Exception(inicio + error + final)
            elif char == '*' and ( not self.is_operand(expresion[expresion.index(char)-1]) and expresion[expresion.index(char)-1] != ')'):
                error = "\tError: La expresión regular ingresada es incorrecta. \n\tEl operador * no se está aplicando a ningín símbolo.\n"
                raise Exception(inicio + error + final)
            elif char == '?' and ( not self.is_operand(expresion[expresion.index(char)-1]) and expresion[expresion.index(char)-1] != ')'):
                print(char)
                print(expresion[expresion.index(char)-1])
                error = "\tError: La expresión regular ingresada es incorrecta. \n\tEl operador ? no se está aplicando a ningín símbolo.\n"
                raise Exception(inicio + error + final)
            elif char == '|' and ( not self.is_operand(expresion[expresion.index(char)-1]) and expresion[expresion.index(char)-1] != ')'):
                error = "\tError: La expresión regular ingresada es incorrecta. \n\tEl operador | no se está aplicando a ningín símbolo.\n"
                raise Exception(inicio + error + final)
            elif char == '|' and ( not self.is_operand(expresion[expresion.index(char)+1]) and expresion[expresion.index(char)+1] != '('):
                error = "\tError: La expresión regular ingresada es incorrecta. \n\tEl operador | no se está aplicando a ningín símbolo.\n"
                raise Exception(inicio + error + final)
            
        if self.is_binary(expresion[-1]): 
            error = "\tError: La expresión regular ingresada es incorrecta. \n\tNo puede terminar con un operador binario.\n"
            raise Exception(inicio + error + final)
        
        if parentesis_izq != parentesis_der:
            error = "\tError: La expresión regular ingresada es incorrecta. \n\tNo existe la misma cantidad de '(' que de ')'.\n"
            raise Exception(inicio + error + final)
    

    def concat_expression(self, expresion):
        concat_expresion = ""
        
        for i in range(len(expresion)):
            char = expresion[i]
            concat_expresion += char

            if i+1 < len(expresion):
                nchar = expresion[i+1]

                if char != "(" and nchar != ")" and not self.is_operator(nchar) and not self.is_binary(char):
                    concat_expresion += "."
    
        return concat_expresion

    def is_unary(self, char):
        return char in self.unary_operators
    
    def is_binary(self, char):
        return char in self.binary_operators
    
    def is_operator(self, char):
        return char in self.operators.keys()

    def is_operand(self, char):
        if char == 'ε':
            return True
        else:
            return True if char.isalpha() else char.isnumeric()

    def get_precedence(self, operator):
        return self.operators[operator]

    def convert(self):
        stack = []
        output = []
        self.expresion = ([*self.expresion])
        last = ''
        for i in range(len(self.expresion)):
            if self.is_operand(self.expresion[i]):
                output.append(self.expresion[i])
            elif self.expresion[i] == '(':
                stack.append(self.expresion[i])
            elif self.expresion[i] == ')':
                while stack[-1] != '(':
                    output.append(stack.pop())
                if stack.pop() != '(':
                    print('Error: Hace falta un paréntesis')
                    return
            elif self.is_operator(self.expresion[i]):
                while stack and self.get_precedence(self.expresion[i]) <= self.get_precedence(stack[-1]):
                    output.append(stack.pop())
                stack.append(self.expresion[i])
                
            else:
                print(self.expresion[i])
                print('Error: Caracter no válido')
                return
        while stack:
            output.append(stack.pop())

        return output
