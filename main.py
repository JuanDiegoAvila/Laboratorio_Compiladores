from Yalex.yalex import * 
from Yapar.yapar import *
from Automatas.postfix import *
from Automatas.thompson import * 
from comunicador import *
import pickle
import sys
import subprocess
import multiprocessing
sys.setrecursionlimit(5000)


comunicador = Comunicador()
with open('./pickle/comunicador.pickle', 'wb') as f:
        pickle.dump(comunicador, f)

# # crear el comunicador y guardarlo en un pickle para usarlo en los generadores

# def runYapar():
#     

# def runYalex():
#     

# if __name__ == "__main__":
    

#     # crear el proceso para yapar
#     p2 = multiprocessing.Process(target=runYapar)

#     # crear el proceso para yalex
#     p1 = multiprocessing.Process(target=runYalex)

#     # iniciar los procesos
#     p1.start()
#     p2.start()

#     # esperar a que terminen los procesos
#     p1.join()
#     p2.join()

subprocess.run(["python", "generadorAS.py"])
subprocess.run(["python", "generadorAL.py"])
subprocess.run(["python", "AS.py"])
subprocess.run(["python", "AL.py"])