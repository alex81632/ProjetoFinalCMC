class SparseLevenshteinAutomaton:
    def __init__(self, words):
        self.words = words
        self.sparse_list = []     

    def start(self):
        return (range(self.max_edits+1), range(self.max_edits+1))

    def step(self, indices, values, c):
        if indices and indices[0] == 0 and values[0] < self.max_edits:
            new_indices = [0]
            new_values = [values[0] + 1]
        else:
            new_indices = []
            new_values = []

        for j,i in enumerate(indices):
            if i == len(self.string): break
            cost = 0 if self.string[i] == c else 1
            val = values[j] + cost
            if new_indices and new_indices[-1] == i:
                val = min(val, new_values[-1] + 1)
            if j+1 < len(indices) and indices[j+1] == i+1:
                val = min(val, values[j+1] + 1)
            if val <= self.max_edits:
                new_indices.append(i+1)
                new_values.append(val)

        return (new_indices, new_values)

    def is_match(self, indices):
        return bool(indices) and indices[-1] == len(self.string)

    def can_match(self, indices):
        return bool(indices)

    def transitions(self, indices):
        return set(self.string[i] for i in indices if i < len(self.string))
    
    def quary(self, string, n=1):
        self.string = string
        self.max_edits = n
        for query in self.words:
            s_sparse = self.start()
            for c in query:
                if (self.can_match(s_sparse[0])):  
                    s_sparse = self.step(s_sparse[0], s_sparse[1], c)
                else:
                    break
            if self.is_match(s_sparse[0]):
                self.sparse_list.append(query)
        return self.sparse_list