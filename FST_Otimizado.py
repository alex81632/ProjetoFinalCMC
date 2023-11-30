# FST ( Minimal Deterministic Finite State Transducer )

class FST_Otimizado:

    class Estado:
        def __init__(self) -> None:
            self.transicoes = {}
            self.transicoes_inversas = {}
            self.final = False
            self.congelado = False
    
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

        for valor, estado_inter in estado.transicoes.items():
            self.combinacoes(estado_inter, word + valor)

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
        estado1.transicoes[valor] = estado2

        # Transição Inversa
        estado2.transicoes_inversas[valor] = estado1

    def junta_transicoes(self, estado: Estado) -> None:
        '''
        Junta as transições da anti_raiz que tem mesmo sufixo
        '''        
        valor, no_adicionado = estado.transicoes_inversas.popitem()
        estado.transicoes_inversas[valor] = no_adicionado

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
        
        estado.transicoes_inversas.popitem()

        valor, aux = no_adicionado.transicoes_inversas.popitem()
        no_adicionado.transicoes_inversas[valor] = aux
        
        valor, aux2 = aux.transicoes.popitem()
        aux.transicoes[valor] = no_similar

        # Transição Inversa
        no_similar.transicoes_inversas[valor] = aux

        self.junta_transicoes(no_similar)

    def adicionar(self, estado: Estado) -> None:
        '''
        Percorre o caminho recem congelado e muda o último estado para a anti_raiz
        '''
        no_atual = estado
        no_atual.congelado = True

        while len(no_atual.transicoes):
            valor, aux = no_atual.transicoes.popitem()
            no_atual.transicoes[valor] = aux
            no_atual = aux
            no_atual.congelado = True

        if no_atual == self.anti_raiz:
            return
        
        valor, aux = no_atual.transicoes_inversas.popitem()
        no_atual.transicoes_inversas[valor] = aux
        no_atual = aux

        no_atual.transicoes.popitem()

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
                    valor, aux = no_atual.transicoes.popitem()
                    no_atual.transicoes[valor] = aux
                    self.adicionar(aux)
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

        valor, aux = self.ultimo.transicoes.popitem()
        self.ultimo.transicoes[valor] = aux          

        self.adicionar(aux)
        self.adicionar(self.raiz)

    
    def otimizar_memoria(self) -> None:
        '''
        Otimiza a memória da FST
        '''
        self.anti_raiz = None
        self.ultimo = None
        self.words = None

        self.criar = None
        self.add = None
        self.adicionar = None
        self.junta_transicoes = None
        self.transicao

        self.otimizar(self.raiz)

    def otimizar(self, estado: Estado) -> None:
        '''
        Função recursiva que passa pelos nos liberando memoria
        '''
        estado.transicoes_inversas = None
        
        for valor, estado_inter in estado.transicoes.items():
            self.otimizar(estado_inter)