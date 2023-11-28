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
