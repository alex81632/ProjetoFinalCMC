# FST ( Minimal Deterministic Finite State Transducer )

class TRIE:

    class Estado:
        def __init__(self) -> None:
            self.transicoes = []
            self.name = 1
            self.final = False

    class Transicao:
        def __init__(self) -> None:
            self.estado1 = None
            self.estado2 = None
            self.valor = None
            self.indice = None
    
    def __init__(self, words: list) -> None:
        self.raiz = self.Estado()
        self.num_nos = 1
        self.words = words
        self.criar()
        self.matches = []
        self.ultimo = None
    
    def imprimir(self) -> None:
        '''
        Imprime a TRIE em um arquivo trie.dot
        '''
        arquivo = open("trie.dot", 'w')
        arquivo.write('digraph TRIE {\n')
        arquivo.write('    rankdir=LR;\n')
        arquivo.write('    node [shape=circle];\n')
        arquivo.write('    node [style=filled];\n')
        arquivo.write('    node [fillcolor="#EEEEEE"];\n')
        arquivo.write('    node [color="#EEEEEE"];\n')
        arquivo.write('    edge [color="#31CEF0"];\n')
        arquivo.write('    edge [style="bold"];\n')
        arquivo.write('    edge [arrowsize=1.5];\n')
        
        for transicao in self.raiz.transicoes:
            arquivo.write(f'    {transicao.estado1.name} -> {transicao.estado2.name} [label="{transicao.valor}"];\n')
            self.imprimir_filhos(transicao.estado2, arquivo)
        
        arquivo.write('}')

        print("Número de nós:", self.num_nos)

    def imprimir_filhos(self, estado: Estado, arquivo) -> None:
        '''
        Imprimir as transiçõs em DFS
        '''
        for transicao in estado.transicoes:
            arquivo.write(f'    {transicao.estado1.name} -> {transicao.estado2.name} [label="{transicao.valor}"];\n')
            self.imprimir_filhos(transicao.estado2, arquivo)

    def achar_transicao(self, estado: Estado, valor: str) -> Estado:
        '''
        Para um estado, se ele tiver uma transição com o valor dado, retorna o estado de destino. Se não, retorna None.
        '''
        for transicao in estado.transicoes:
            if transicao.valor == valor:
                return transicao.estado2
            
    def checar_combinacoes(self, word: str) -> list:
        '''
        Acha o último estado que pode ser achado a partir do prefixo dado e chama a função de combinações
        '''
        no_atual = self.raiz
        for i in range(len(word)):
            no_atual = self.achar_transicao(no_atual, word[i])
            if no_atual == None:
                return []
            
        self.matches = []

        self.combinacoes(no_atual, word)

        return self.matches
    
    def combinacoes(self, estado: Estado, word: str) -> None:
        '''
        Retorna uma lista de palavras que podem ser formadas a partir do prefixo dado
        '''
        if len(estado.transicoes) == 0:
            self.matches.append(word)
            return
        
        if estado.final:
            self.matches.append(word)

        for transicao in estado.transicoes:
            self.combinacoes(transicao.estado2, word + transicao.valor)

    def criar(self) -> None:
        '''
        Cria uma TRIE a partir de uma lista de palavras e imprime o grafo em um arquivo .dot
        '''
        no_atual = self.raiz
        for word in self.words:
            for i in range(len(word)):
                if(self.achar_transicao(no_atual, word[i]) == None):
                    nova_transicao = self.Transicao()
                    nova_transicao.estado1 = no_atual
                    nova_transicao.estado2 = self.Estado()
                    self.num_nos += 1
                    nova_transicao.estado2.name = self.num_nos
                    nova_transicao.valor = word[i]
                    no_atual.transicoes.append(nova_transicao)
                no_atual = self.achar_transicao(no_atual, word[i])
            no_atual.final = True
            no_atual = self.raiz

class FST:

    class Estado:
        def __init__(self) -> None:
            self.transicoes = []
            self.transicoes_inversas = []
            self.name = 1
            self.final = False
            self.impresso = False
            self.anti_impresso = False
            self.congelado = False
        
        def __repr__(self) -> str:
            return str(self.name)

    class Transicao:
        def __init__(self) -> None:
            self.estado1 = None
            self.estado2 = None
            self.valor = None

        def __repr__(self) -> str:
            return str(self.valor)
    
    def __init__(self, words: list) -> None:
        self.raiz = self.Estado()
        self.anti_raiz = None
        self.num_nos = 1
        self.words = words
        self.matches = []
        self.ultimo = None

        self.criar()
    
    def imprimir_inverso(self) -> None:
        '''
        Imprime a FST em um arquivo fst_inverso.dot
        '''
        arquivo = open("fst_inverso.dot", 'w')
        arquivo.write('digraph FST {\n')
        arquivo.write('    rankdir=LR;\n')
        arquivo.write('    node [shape=circle];\n')
        arquivo.write('    node [style=filled];\n')
        arquivo.write('    node [fillcolor="#EEEEEE"];\n')
        arquivo.write('    node [color="#EEEEEE"];\n')
        arquivo.write('    edge [color="#31CEF0"];\n')
        arquivo.write('    edge [style="bold"];\n')
        arquivo.write('    edge [arrowsize=1.5];\n')

        if self.anti_raiz.final:
            arquivo.write(f'    {self.anti_raiz.name} [shape=doublecircle];\n')
        
        for transicao in self.anti_raiz.transicoes_inversas:
            arquivo.write(f'    {transicao.estado1.name} -> {transicao.estado2.name} [label="{transicao.valor}"];\n')
            if not transicao.estado2.anti_impresso:
                self.imprimir_filhos_inverso(transicao.estado2, arquivo)
        
        arquivo.write('}')

    def imprimir_filhos_inverso(self, estado: Estado, arquivo) -> None:
        '''
        Imprimir as transiçõs em DFS
        '''

        if estado.final:
            arquivo.write(f'    {estado.name} [shape=doublecircle];\n')

        estado.anti_impresso = True
        for transicao in estado.transicoes_inversas:
            arquivo.write(f'    {transicao.estado1.name} -> {transicao.estado2.name} [label="{transicao.valor}"];\n')
            if not transicao.estado2.anti_impresso:
                self.imprimir_filhos_inverso(transicao.estado2, arquivo)

    def imprimir(self) -> None:
        '''
        Imprime a FST em um arquivo fst.dot
        '''
        self.num_nos = 1

        arquivo = open("fst.dot", 'w')
        arquivo.write('digraph FST {\n')
        arquivo.write('    rankdir=LR;\n')
        arquivo.write('    node [shape=circle];\n')
        arquivo.write('    node [style=filled];\n')
        arquivo.write('    node [fillcolor="#EEEEEE"];\n')
        arquivo.write('    node [color="#EEEEEE"];\n')
        arquivo.write('    edge [color="#31CEF0"];\n')
        arquivo.write('    edge [style="bold"];\n')
        arquivo.write('    edge [arrowsize=1.5];\n')

        if self.raiz.final:
            arquivo.write(f'    {self.raiz.name} [shape=doublecircle];\n')
        
        for transicao in self.raiz.transicoes:
            arquivo.write(f'    {transicao.estado1.name} -> {transicao.estado2.name} [label="{transicao.valor}"];\n')
            if not transicao.estado2.impresso:
                self.imprimir_filhos(transicao.estado2, arquivo)
        
        arquivo.write('}')

        print("Número de nós:", self.num_nos)

    def imprimir_filhos(self, estado: Estado, arquivo) -> None:
        '''
        Imprimir as transiçõs em DFS
        '''
        self.num_nos += 1
        if estado.final:
            arquivo.write(f'    {estado.name} [shape=doublecircle];\n')

        estado.impresso = True
        for transicao in estado.transicoes:
            arquivo.write(f'    {transicao.estado1.name} -> {transicao.estado2.name} [label="{transicao.valor}"];\n')
            if not transicao.estado2.impresso:
                self.imprimir_filhos(transicao.estado2, arquivo)
            
    def checar_combinacoes(self, word: str) -> list:
        '''
        Acha o último estado que pode ser achado a partir do prefixo dado e chama a função de combinações
        '''
        no_atual = self.raiz
        for i in range(len(word)):
            no_atual = self.achar_transicao(no_atual, word[i])
            if no_atual == None:
                return []
            
        self.matches = []

        self.combinacoes(no_atual, word)

        return self.matches
    
    def combinacoes(self, estado: Estado, word: str) -> None:
        '''
        Retorna uma lista de palavras que podem ser formadas a partir do prefixo dado
        '''
        if len(estado.transicoes) == 0:
            self.matches.append(word)
            return
        
        if estado.final:
            self.matches.append(word)

        for transicao in estado.transicoes:
            self.combinacoes(transicao.estado2, word + transicao.valor)

    def achar_transicao(self, estado: Estado, valor: str) -> Estado:
        '''
        Para um estado, se ele tiver uma transição com o valor dado, retorna o estado de destino. Se não, retorna None.
        '''
        for transicao in estado.transicoes:
            if transicao.valor == valor:
                return transicao.estado2

    def achar_transicao_inversa(self, estado: Estado, valor: str) -> Estado:
        '''
        Para um estado, retorna o estado pai que tem uma transição com o valor dado
        '''
        for transicao_inversa in estado.transicoes_inversas:
            if transicao_inversa.valor == valor:
                return transicao_inversa.estado2

    def junta_transicoes(self, estado: Estado) -> None:
        '''
        Junta as transições da anti_raiz que tem mesmo sufixo
        '''
        transicao_nova = estado.transicoes_inversas[-1]
        valor = transicao_nova.valor
        no_adicionado = transicao_nova.estado2

        no_similar = self.achar_transicao_inversa(estado, valor)

        if no_similar == no_adicionado or no_similar == None or no_adicionado == None or no_similar.final != no_adicionado.final or no_adicionado == self.ultimo or no_similar.congelado == False or len(no_similar.transicoes) > 1 or len(no_adicionado.transicoes) > 1:
            return

        estado.transicoes_inversas.pop()
        
        for transicao_inv in no_adicionado.transicoes_inversas:
            for transicao in transicao_inv.estado2.transicoes:
                if transicao.estado2 == no_adicionado:
                    transicao.estado2 = no_similar

                    # Transição Inversa
                    nova_transicao_inversa = self.Transicao()
                    nova_transicao_inversa.estado1 = no_similar
                    nova_transicao_inversa.estado2 = transicao_inv.estado2
                    nova_transicao_inversa.valor = transicao_inv.valor
                    no_similar.transicoes_inversas.append(nova_transicao_inversa)

        self.junta_transicoes(no_similar)

    def adicionar(self, estado: Estado) -> None:
        '''
        Percorre o caminho recem congelado e muda o último estado para a anti_raiz
        '''
        no_atual = estado
        no_atual.congelado = True

        while len(no_atual.transicoes):
            no_atual = no_atual.transicoes[-1].estado2

        if no_atual == self.anti_raiz:
            return
        
        valor = no_atual.transicoes_inversas[-1].valor
        no_atual = no_atual.transicoes_inversas[-1].estado2

        no_atual.transicoes.pop()

        # Nova Transição
        nova_transicao = self.Transicao()
        nova_transicao.estado1 = no_atual
        nova_transicao.estado2 = self.anti_raiz
        nova_transicao.valor = valor
        no_atual.transicoes.append(nova_transicao)

        # Nova Transição Inversa
        nova_transicao_inversa = self.Transicao()
        nova_transicao_inversa.estado1 = self.anti_raiz
        nova_transicao_inversa.estado2 = no_atual
        nova_transicao_inversa.valor = valor
        self.anti_raiz.transicoes_inversas.append(nova_transicao_inversa)

        self.junta_transicoes(self.anti_raiz)

        return

    def criar(self) -> None:
        '''
        Cria uma FST a partir de uma lista de palavras e imprime o grafo em um arquivo .dot
        '''
        no_atual = self.raiz
        for j in range(len(self.words)):
            word = self.words[j]
            
            for i in range(len(word)):
                no = self.achar_transicao(no_atual, word[i])

                if(no == None):

                    # Novo Estado
                    self.num_nos += 1
                    novo_no = self.Estado()
                    novo_no.name = self.num_nos
                    valor = word[i]

                    if no_atual == self.anti_raiz:
                        self.anti_raiz = None


                    if len(no_atual.transicoes):
                        self.adicionar(no_atual.transicoes[-1].estado2)
                        self.ultimo = no_atual

                    # Transição
                    nova_transicao = self.Transicao()
                    nova_transicao.estado1 = no_atual
                    nova_transicao.estado2 = novo_no
                    nova_transicao.valor = valor
                    no_atual.transicoes.append(nova_transicao)

                    # Transição Inversa
                    transicao_inversa = self.Transicao()
                    transicao_inversa.estado1 = novo_no
                    transicao_inversa.estado2 = no_atual
                    transicao_inversa.valor = valor
                    novo_no.transicoes_inversas.append(transicao_inversa)

                    no_atual = novo_no
                    
                else:
                    no_atual = no
            no_atual.final = True

            if self.anti_raiz == None:
                self.anti_raiz = no_atual

            no_atual = self.raiz
        
        self.adicionar(self.ultimo)