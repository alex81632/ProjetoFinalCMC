# Binary Search Tree

class BS:

    class Estado:
        def __init__(self) -> None:
            self.word = None
            self.filho_dir = None
            self.filho_esq = None

    def __init__(self, words: list) -> None:
        self.words = words
        self.num_words = len(words)
        self.word = None
        self.raiz = self.Estado()
        self.matches = []

        self.criar()

    def criar(self):
        '''
        Cria uma BST a partir de uma lista de palavras
        '''
        self.raiz = self.criar_aux(0, self.num_words-1)

        self.words = None

    
    def criar_aux(self, ini: int, fim: int) -> Estado:
        '''
        Cria uma BST a partir de uma lista de palavras
        '''
        if ini > fim:
            return None

        meio = (ini + fim) // 2
        no = self.Estado()
        no.word = self.words[meio]
        no.filho_esq = self.criar_aux(ini, meio-1)
        no.filho_dir = self.criar_aux(meio+1, fim)

        return no
    
    def checar_combinacoes(self, word: str) -> list:
        '''
        Acha todas as palavras que começam com o prefixo dado
        '''
        self.matches = []
        self.word = word
        self.checar_combinacoes_aux(self.raiz)
        return self.matches
    
    def checar_combinacoes_aux(self, no: Estado) -> None:
        '''
        Acha todas as palavras que começam com o prefixo dado
        '''
        if no == None:
            return
        
        if no.word.startswith(self.word):
            self.matches.append(no.word)
            self.checar_combinacoes_aux(no.filho_esq)
            self.checar_combinacoes_aux(no.filho_dir)
        elif no.word > self.word:
            self.checar_combinacoes_aux(no.filho_esq)
        else:
            self.checar_combinacoes_aux(no.filho_dir)