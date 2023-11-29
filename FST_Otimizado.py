# FST ( Minimal Deterministic Finite State Transducer )

class FST_Otimizado:

    class Estado:
        def __init__(self) -> None:
            self.transicoes = {}
            self.transicoes_inversas = {}
            self.ultima_transicao = None
            self.ultima_transicao_inversa = None
            self.final = False
            self.congelado = False

    class Transicao:
        def __init__(self) -> None:
            self.estado = None
            self.valor = None
        
        def __eq__(self, other) -> bool:
            return self.valor == other.valor
        
        def __hash__(self) -> int:
            return hash((self.estado, self.valor))
    
    def __init__(self, words: list) -> None:
        self.raiz = self.Estado()
        self.anti_raiz = None
        self.words = words
        self.matches = []
        self.ultimo = None

        self.criar()
    
            
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
            self.combinacoes(transicao.estado, word + transicao.valor)

    def achar_transicao(self, estado: Estado, valor: str) -> Estado:
        '''
        Para um estado, se ele tiver uma transição com o valor dado, retorna o estado de destino. Se não, retorna None.
        '''
        return estado.transicoes.get(valor, None)

    def achar_transicao_inversa(self, estado: Estado, valor: str) -> Estado:
        '''
        Para um estado, retorna o estado pai que tem uma transição com o valor dado
        '''
        return estado.transicoes_inversas.get(valor, None)

    def transicao(self, estado1: Estado, estado2: Estado, valor: str) -> None:
        '''
        Cria uma transição entre dois estados
        '''
        # Transição
        nova_transicao = self.Transicao()
        nova_transicao.estado = estado2
        nova_transicao.valor = valor
        estado1.transicoes.append(nova_transicao)

        # Transição Inversa
        transicao_inversa = self.Transicao()
        transicao_inversa.estado = estado1
        transicao_inversa.valor = valor
        estado2.transicoes_inversas.append(transicao_inversa)

    def junta_transicoes(self, estado: Estado) -> None:
        '''
        Junta as transições da anti_raiz que tem mesmo sufixo
        '''
        transicao_nova = estado.transicoes_inversas[-1]
        valor = transicao_nova.valor
        no_adicionado = transicao_nova.estado

        if no_adicionado.congelado == False:
            return

        no_similar = self.achar_transicao_inversa(estado, valor)

        if no_similar == None:
            return

        if no_similar == no_adicionado:
            return
        
        if no_similar.final != no_adicionado.final:
            return
        
        if len(no_similar.transicoes) > 1:
            return
        
        if len(no_adicionado.transicoes) > 1:
            return
        
        estado.transicoes_inversas.pop()

        transicao_inv = no_adicionado.transicoes_inversas[-1]

        transicao_inv.estado.transicoes[-1].estado = no_similar

        # Transição Inversa
        nova_transicao_inversa = self.Transicao()
        nova_transicao_inversa.estado = transicao_inv.estado
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
            no_atual = no_atual.transicoes[-1].estado
            no_atual.congelado = True

        if no_atual == self.anti_raiz:
            return
        
        valor = no_atual.transicoes_inversas[-1].valor
        no_atual = no_atual.transicoes_inversas[-1].estado

        no_atual.transicoes.pop()

        self.transicao(no_atual, self.anti_raiz, valor)

        self.junta_transicoes(self.anti_raiz)

        return
    
    def add(self, word: str) -> None:
        '''
        Adiciona uma palavra à FST
        '''
        no_atual = self.raiz
        for i in range(len(word)):
            no = self.achar_transicao(no_atual, word[i])

            if(no == None):
                # Novo Estado
                novo_no = self.Estado()

                if no_atual == self.anti_raiz:
                    self.anti_raiz = None

                if len(no_atual.transicoes):
                    self.adicionar(no_atual.transicoes[-1].estado)
                    self.ultimo = no_atual

                self.transicao(no_atual, novo_no, word[i])

                no_atual = novo_no
                
            else:
                no_atual = no
        no_atual.final = True

        if self.anti_raiz == None:
            self.anti_raiz = no_atual

    def criar(self) -> None:
        '''
        Cria uma FST a partir de uma lista de palavras e imprime o grafo em um arquivo .dot
        '''
        for j in range(len(self.words)):
            self.add(self.words[j])            

        self.adicionar(self.ultimo.transicoes[-1].estado)
        self.adicionar(self.raiz)

        self.words = []