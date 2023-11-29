data = open('words.txt', 'r')
words = []
for line in data:
    line = line.strip()
    if len(line) == 1:
        continue
    
    words.append(line)

print("Numero de palavras: ", len(words))

from FST_Otimizado import FST_Otimizado as FST_Otimizado

import timeit

ini = timeit.default_timer()
fst = FST_Otimizado(words)
fim = timeit.default_timer()

print("Tempo de criação: ", fim - ini)