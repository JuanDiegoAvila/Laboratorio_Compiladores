import re
class Yalex(object):
    def __init__(self, path):
        self.path = path
        self.header = None
        self.trailer = None
        self.tokens = {}
        self.rules = {}
        self.getRules()
        self.getHeaderTrailer()
        self.check_error()
        self.getTokens()
        self.parseTokens()

    def check_error(self):
        # Definimos una lista de palabras clave 
        keywords = ["let", "in", "if", "then", "else", "match", "with", "fun", "function", "try", "raise", "exception", "open", "module", "type", "mutable", "rec", "and", "rule"]

        with open(self.path, "r") as f:
            lines = f.readlines()

        in_rule = False
        for linea in lines:
            words = linea.split()

            # Eliminar lineas vacias
            stripped_line = linea.strip()

            # Verificamos si la cadena resultante es una cadena vacía
            if not stripped_line:
                continue

            # Si hay dos keywords en la cadena hay error
            if words[0] in keywords and words[1] in keywords:
                raise Exception("Error: El nombre no puede ser una palabra reservada")

            # Si la linea empieza con (* y termina con *) entonces es un comentario
            pattern = r"^\(\*.*\*\)$"
            match = re.match(pattern, linea)

            if match:
                continue

            # La linea debe iniciar con un keyword
            if words[0] not in keywords and not in_rule:
                raise Exception("Error: La linea debe iniciar con un keyword")
            
            if words[0] == "rule":
                in_rule = True
                
            # La linea debe tener un '='
            if words[0] == 'let' and "=" != words[2]:
                raise Exception("Error: La linea debe tener un '='")

            # No puede haber el simbolo " si la linea empieza con let
            if '"' in linea and linea.startswith('let'):
                raise Exception("Error: No puede haber el simbolo \"")
            
            temp_string = "###"
            pattern = r"'(?:[^'\\]|\\.)*'"  # Expresión regular para encontrar subcadenas entre comillas simples
            linea = re.sub(pattern, temp_string, linea)

            # Los simbolos {}, [] y () deben estar balanceados
            if linea.count("{") != linea.count("}"):
                raise Exception("Error: Los simbolos {} deben estar balanceados")
                
            if linea.count("[") != linea.count("]"):
                raise Exception("Error: Los simbolos [] deben estar balanceados")

           
            if linea.count("(") != linea.count(")"):
                raise Exception("Error: Los simbolos () deben estar balanceados")

    def getRules(self):
        is_rule = False
        # leer el archivo con encoding utf-8
        with open(self.path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith("rule"):
                    is_rule = True
                    continue

                # Si es salto de linea terminar
                if line == "\n" and is_rule:
                    break

                if is_rule:
                    # El formato es | nombre { valor }

                    # Eliminar doble espacio o mas
                    line = re.sub(r'\s+', ' ', line)
                    line = line.replace(" | ", "")

                    is_value = False
                    temp_value = ""
                    temp_key = ""
                    for element in line:
                        if element == "{":
                            is_value = True
                            continue

                        if element == "}":
                            is_value = False
                            continue

                        if is_value:
                            temp_value += element
                        else:
                            temp_key += element

                    temp_key = temp_key.replace(" ", "")
                    temp_key = temp_key.replace("'", "")
                    temp_value = temp_value.replace(" print(\"", "").replace("\\n\")", "").replace("\")","")
                    # agregar el token y su valor a la lista de tokens
                    self.rules[temp_key] = temp_value


    def getTokens(self):
        with open(self.path, 'r') as file:
            for line in file:
                # si la linea empieza con let, es un token\

                if line.startswith("let"):
                    # tomar la linea sin la palabra inicial let
                    line = line.replace("let ", "", 1)

                    token = line.split("=")[0]
                    value = line.split("=")[1]

                    # eliminar espacios y el salto de linea en el valor
                    value = value.replace("\n", "")
                    
                    # si empieza con espacio eliminarlo
                    if value.startswith(" "):
                        value = value[1:]
                    token = token.replace(" ", "")
                    
                    # agregar el token y su valor a la lista de tokens
                    self.tokens[token] = value

    def parseTokens(self):
        # Si el token tiene la forma ['0' - '9'] entonces poner de la forma '0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9'
        
        for token in self.tokens:
            actual = self.tokens[token]
            if actual.startswith("[") and actual.endswith("]"):
                actual = actual.replace("[", "").replace("]", "")

            self.tokens[token] = actual
            
            if re.match(r"'(\d+)'-'(\d+)'", actual):
                inicio, fin = map(int, re.findall(r'\d+', actual))
                numeros = list(range(inicio, fin+1))
                numeros_str = [str(num) for num in numeros]
                actual = "|".join(numeros_str)

            if re.match(r"'(\w+)'-'(\w+)''(\w+)'-'(\w+)'", actual):
                inicio1, fin1, inicio2, fin2 = re.findall(r'\w+', actual)
                letras1 = list(range(ord(inicio1), ord(fin1)+1))
                letras2 = list(range(ord(inicio2), ord(fin2)+1))
                letras = letras1 + letras2
                letras_str = [chr(num) for num in letras]
                actual = "|".join(letras_str)
            
            elif re.match(r"'(\w+)'-'(\w+)'", actual):
                inicio, fin = re.findall(r'\w+', actual)
                letras = list(range(ord(inicio), ord(fin)+1))
                letras_str = [chr(num) for num in letras]
                actual = "|".join(letras_str)


            actual = actual.replace("''", "'|'")
            # actual = actual.replace("'", "")

            self.tokens[token] = actual

        # si algun nombre de un token esta en el valor, sustituirlo por el valor real del token
        for token in self.tokens:
            # recorrer de forma inversa el resto de tokens
            for key2 in reversed(list(self.tokens.keys())):
                if token != key2:
                    self.tokens[token] = self.tokens[token].replace(key2, '('+self.tokens[key2]+')')

            # for token2 in self.tokens:
            #     if token != token2:
            #         self.tokens[token] = self.tokens[token].replace(token2, '('+self.tokens[token2]+')')

    def getHeaderTrailer(self):
        header = False
        with open(self.path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith("(*") and not header:
                    header = True
                    self.header = line.replace("(* ", "").replace(" *)", "")
                    continue

                if line.startswith("(*") and header:
                    self.trailer = line.replace("(* ", "").replace(" *)", "")

        

        






    

