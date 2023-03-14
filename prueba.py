from postfix import *
from thompson import *
from grafo import *
from afd_directo import *
from afd_subconjuntos import *
from simulacion import *
from minimizacion import *


expresion = input("\n Ingrese la expresion regular que sera convertida a AFN -> ")

# Se hace la conversion de la expresion regular a postfix.
expresion = postive_format(expresion)
print ("Converted to: " + expresion)