import re
def check_expresion(expresion):
    postfix = Postfix(expresion)
    postfix.error_check(expresion)

    return postfix.concat_expression(expresion)

def deconstruct_expresion(expresion):
        temp_expresion = ([*expresion])
        stack = []
        es_comilla = False
        temp = []
    
        for i in range(len(temp_expresion)):
            if temp_expresion[i] == "'":
                es_comilla = not es_comilla
                temp.append(temp_expresion[i])

                if not es_comilla:
                    stack.append("".join(temp))
                    temp = []

            elif es_comilla:
                temp.append(temp_expresion[i])
            else:
                stack.append(temp_expresion[i])
        return stack

def postive_format(expresion):

    expresion = deconstruct_expresion(expresion)
    nueva_expresion = []
    conteo_par_izq = 0
    conteo_par_der = 0

    for char in range(len(expresion)):

        if expresion[char] == '+':
            prev_char = expresion[char-1]
            if prev_char == ')':

                conteo_par_der += 1

                i = char-2
                temp = []
                while i >= 0:
                    if expresion[i] == ')':
                        conteo_par_der += 1
                    if expresion[i] == '(':
                        conteo_par_izq += 1

                        if conteo_par_izq == conteo_par_der:
                            
                            # temp.append(expresion[i])
                            temp = reversed(temp)
                            temp = list(temp)
                            temp.insert(0, '(')
                            temp.append(')')
                            temp.append('*')

                            break
                        else:
                            temp.append(expresion[i])

                    else:
                        temp.append(expresion[i])
                    i -= 1
                
                nueva_expresion.extend(temp)
            else:
                # expresion[char] = prev_char + '*'
                temp = [prev_char, '*']
                nueva_expresion.extend(temp)

        else:
            nueva_expresion.append(expresion[char])
    return ''.join(nueva_expresion)


class Postfix():
    def __init__(self, expresion, AFD = False):
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
        self.AFD = AFD
        self.expresion = expresion
    
    def toPostfix(self):
        self.error_check(self.expresion)
        
        self.expresion = deconstruct_expresion(self.expresion)

        if self.AFD:
            self.expresion = postive_format(self.expresion)

        self.expresion = self.concat_expression(self.expresion)
        self.output = self.convert()
        self.final = ''.join(self.output)
        self.final = self.final.replace('?', 'ε|')

    def error_check(self, expresion):
        
        parentesis_izq = 0
        parentesis_der = 0
        herror = False
        error = ''
        
        inicio = "\n==============================================================================================\n"
        final = "=============================================================================================="

        if self.is_operator(expresion[0]) and expresion[0] not in '()':
            error += "\tError: La expresión regular ingresada es incorrecta. \n\tNo puede iniciar con un operador.\n"
            herror = True

        if len(expresion) == 0:
            error += "\tError: La expresión regular ingresada es incorrecta. \n\tNo se ingresó ninguna expresión.\n"
            herror = True
        
        if self.is_binary(expresion[-1]): 
            error += "\tError: La expresión regular ingresada es incorrecta. \n\tNo puede terminar con un operador binario.\n\n"
            herror = True
        
        
        expresion = ([*expresion])

        for char in range(len(expresion)):


            # if expresion[char] == ' ':
            #     error += "\tError: La expresión regular ingresada es incorrecta. \n\tNo puede haber espacios en blanco.\n\n"
            #     herror = True
            if expresion[char] == '(':
                parentesis_izq += 1
            elif expresion[char] == ')':
                parentesis_der += 1
            
            elif not self.is_operand(expresion[char]) and not self.is_operator(expresion[char]) and not '#':
                error += "\tError: La expresión regular ingresada es incorrecta. \n\tEl símbolo '" + expresion[char] + "' no es válido.\n\n"
                herror = True
            
            if char + 1 < len(expresion):
                if expresion[char] == '|':
                    if self.is_operator(expresion[char+1]) and expresion[char+1] != '(':
                        error += "\tError: La expresión regular ingresada es incorrecta. \n\tNo puede haber un operador seguido de |.\n\n"
                        herror = True
                elif expresion[char] == '+' and ( not self.is_operand(expresion[char-1]) and expresion[char-1] != ')'):
                    error += "\tError: La expresión regular ingresada es incorrecta. \n\tEl operador + no se está aplicando a ningín símbolo.\n\n"
                    herror = True
                elif expresion[char] == '*' and ( not self.is_operand(expresion[char-1]) and expresion[char-1] != ')'):
                    error += "\tError: La expresión regular ingresada es incorrecta. \n\tEl operador * no se está aplicando a ningín símbolo.\n\n"
                    herror = True
                elif expresion[char] == '?' and ( not self.is_operand(expresion[char-1]) and expresion[char-1] != ')'):
                    error += "\tError: La expresión regular ingresada es incorrecta. \n\tEl operador ? no se está aplicando a ningín símbolo.\n\n"
                    herror = True
                elif expresion[char] == '|' and ( not self.is_operand(expresion[char-1]) and expresion[char-1] != ')'):
                    error += "\tError: La expresión regular ingresada es incorrecta. \n\tEl operador | no se está aplicando a ningín símbolo.\n\n"
                    herror = True
                elif expresion[char] == '|' and ( not self.is_operand(expresion[char+1]) and expresion[char+1] != '('):
                    error += "\tError: La expresión regular ingresada es incorrecta. \n\tEl operador | no se está aplicando a ningín símbolo.\n\n"
                    herror = True
                    
        if parentesis_izq != parentesis_der:
            error += "\tError: La expresión regular ingresada es incorrecta. \n\tNo existe la misma cantidad de '(' que de ')'.\n\n"
            herror = True
            
        if herror:
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

        concat_expresion = deconstruct_expresion(concat_expresion)
        

        return concat_expresion

    def is_unary(self, char):
        return char in '*+?'
    
    def is_binary(self, char):
        return char in '|.'
    
    def is_operator(self, char):
        return char in '*+?.|'

    def is_operand(self, char, dentro_de_comillas=False):
        return not self.is_operator(char) and char != '(' and char != ')'
        # if char == 'ε':
        #     return True
        # else:
        #     match = re.match("'\w+'", char)
        #     if match:
        #         return True
        #     if dentro_de_comillas:
        #         return True
        #     return True if char.isalpha() else char.isnumeric()

    def get_precedence(self, operator):
        return self.operators[operator]
    

    def convert(self):
        stack = []
        output = []
        last = ''
        # self.expresion = deconstruct_expresion(self.expresion)
        dentro_de_comillas = False

        for i in range(len(self.expresion)):
            # if self.expresion[i] == "'":
            #     dentro_de_comillas = not dentro_de_comillas

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

        while stack:
            output.append(stack.pop())

        return output
