
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

        self.expresion = self.concat_expression(expresion)
        self.output = self.convert()
        self.final = ''.join(self.output)
        self.final = self.final.replace('?', 'ε|')

    def concat_expression(self, expresion):
        concat_expresion = ""
        
        for i in range(len(expresion)):
            char = expresion[i]
            concat_expresion += char

            if i+1 < len(expresion):
                nchar = expresion[i+1]

                if self.is_operand(char) and self.is_operator(nchar):
                    concat_expresion += ''
                elif self.is_unary(char) and self.is_operand(nchar):
                    concat_expresion += '.'
                elif self.is_binary(char) and self.is_operand(nchar):
                    concat_expresion += ''
                elif self.is_operand(char) and self.is_operand(nchar):
                    concat_expresion += '.'
                elif self.is_operator(char) and nchar == "(":
                    concat_expresion += '.'
                elif self.is_operator(nchar) and (nchar == ")" or self.is_operand(nchar)):
                    concat_expresion += ''
                elif char in [")", "("] and self.is_operator(nchar):
                    concat_expresion += ''

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
