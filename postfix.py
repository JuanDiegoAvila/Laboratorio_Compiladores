
class Postfix():
    def __init__(self, expresion):
        self.expresion = self.concat_expression(expresion)
        print(self.expresion)
        self.stack = []
        self.output = []
        self.operators = {
            '(': 1,
            ')': 1,
            '*': 2,
            '+': 2,
            '.': 3,
            '|': 4,
            '#': 5,
        }
        self.convert()
        print(self.output)

    def concat_expression(self, expresion):
        concat_expresion = ''
        for i in range(len(expresion)):
            if i+1 < len(expresion):
                if self.is_operand(expresion[i]) and self.is_operand(expresion[i+1]):
                    concat_expresion += expresion[i] + '.'
                elif self.is_operand(expresion[i]) and expresion[i+1] == '(':
                    concat_expresion += expresion[i] + '.'
                elif expresion[i] == ')' and self.is_operand(expresion[i+1]):
                    concat_expresion += expresion[i] + '.'
                elif expresion[i] == ')' and expresion[i+1] == '(':
                    concat_expresion += expresion[i] + '.'
                else:
                    concat_expresion += expresion[i]
            else:
                concat_expresion += expresion[i]
                concat_expresion += '.'
                concat_expresion += '#'

        return concat_expresion

    def is_operator(self, char):
        return char in self.operators.keys()

    def is_operand(self, char):
        return char.isalpha()
    
    def get_precedence(self, operator):
        return self.operators[operator]
    
    def convert(self):
        for i in self.expresion:
            if self.is_operand(i):
                self.output.append(i)
            elif i == '(':
                self.stack.append(i)
            elif i == ')':
                while self.stack[-1] != '(':
                    self.output.append(self.stack.pop())
                self.stack.pop()
            else:
                while self.stack and self.get_precedence(i) <= self.get_precedence(self.stack[-1]):
                    self.output.append(self.stack.pop())
                self.stack.append(i)
