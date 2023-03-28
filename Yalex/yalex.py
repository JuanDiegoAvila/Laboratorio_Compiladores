class Yalex(object):
    def __init__(self, path):
        self.path = path
        self.tokens = {}
        self.getTokens()
        self.parseTokens()

    def getTokens(self):
        with open(self.path, 'r') as file:
            for line in file:
                # si la linea empieza con let, es un token

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

                    # agregar el token y su valor a la lista de tokens
                    self.tokens[token] = value

        print(self.tokens)
    
    def parseTokens(self):
        # Si el token tiene la forma ['0' - '9'] entonces poner de la forma '0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9'
        
        for token in self.tokens:
            actual = self.tokens[token]
            if actual.startswith("[") and actual.endswith("]"):
                actual = actual.replace("[", "").replace("]", "")

            self.tokens[token] = actual

            if actual == "'0'-'9'":
                actual = "0|1|2|3|4|5|6|7|8|9"

            if actual == "'a'-'Z''A'-'Z'":
                actual = "a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z"

            if actual == "'a'-'Z'":
                actual = "a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z"

            if actual == "'A'-'Z'":
                actual = "A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z"

            actual = actual.replace("''", "|")
            actual = actual.replace("'", "")

            self.tokens[token] = actual


        print(self.tokens)


    

