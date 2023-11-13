# FST ( Minimal Deterministic Finite State Transducer )

class FST:

    class State:
        def __init__(self) -> None:
            pass

    class Dictionary:
        def __init__(self) -> None:
            pass

    def __init__(self, first, last) -> None:
        self.first_char = first
        self.last_char = last
        self.MAX_WORD_LEN = 100

    def new_state(self) -> State:
        '''
        Create a new state and return it        
        '''
        state = self.State()
        return state

    def is_final(self, state: State, lett: chr) -> bool:
        '''
        boolean returns true if the state is final and false otherwise;
        '''
        pass

    def set_final(self, state: State, final: bool) -> None:
        '''
        sets the finality of the state to the boolean parameter;
        '''
        pass

    def transition(self, state: State, lett: chr) -> State:
        '''
        returns the state to which the transducer transits from the parameter state with the parameter char;
        '''
        pass

    def set_transition(self, state: State, lett: chr, next_state: State) -> None:
        '''
        Sets the transition from first parameter state by the parameter char to the second parameter state;
        '''
        pass

    def state_output(self, state: State) -> set:
        '''
        returns the output set of strings on final states;
        '''
        pass

    def set_state_output(self, state: State, out: set) -> None:
        '''
        sets the output set of strings on final states;
        '''
        pass

    def output(self, state: State, lett: chr) -> str:
        '''
        returns the output string for the transition from the parameter state by the parameter char;
        '''
        pass

    def set_output(self, state: State, lett: chr, out: str) -> None:
        '''
        sets the output string for the transition from the parameter state by the parameter char;
        '''
        pass

    def print_transducer(self, state: State, file) -> None:
        '''
        prints the transducer starting from the parameter state to file.
        '''
        pass

    # Utils

    def copy_state(self, state: State) -> State:
        '''
        returns a copy of the parameter state;
        '''
        pass

    def clear_state(self, state: State) -> None:
        '''
        clears the parameter state;
        '''
        pass

    def compare_states(self, state1: State, state2: State) -> int:
        '''
        compares two states;
        '''
        pass

    # dictionary

    def new_dictionary(self) -> Dictionary:
        '''
        creates a new dictionary and returns it;
        '''
        pass

    def member(self, dictionary: Dictionary, state:State) -> State:
        '''
        returns state in the dictionary equivalent to the parameter state or NULL if not present;
        '''
        pass

    def insert(self, dictionary: Dictionary, state: State) -> None:
        '''
        inserts the parameter state into the dictionary;
        '''
        pass

    def create_minimal_transducer(self, words: list, file_out) -> None:
        '''
        creates a minimal deterministic transducer from the parameter list of words;
        '''

        # Create a new dictionary
        MinimalTrasducerStatesDictionary = self.new_dictionary()

        def findMinimazed (state: self.State) -> self.State:
            '''
            returns an equivalent state from the dictionary. 
            If not present inserts a copy of the parameter 
            to the dictionary and returns it.
            '''
            r = self.member(MinimalTrasducerStatesDictionary, state)

            if r == None:
                r = self.copy_state(state)
                self.insert(MinimalTrasducerStatesDictionary, r)

            return r

        TempStates = []
        
        for i in range(self.MAX_WORD_LEN):
            TempStates.append(self.new_state())
        self.clear_state(TempStates[0])

        PrevWord = ""
        for CurrWord in range(len(words)):
            i = 1
            while i < len(CurrWord) and i < len(PrevWord) and CurrWord[i] == PrevWord[i]:
                i += 1
            PrefixLenPlus1 = i
            # we minimize the states from the sufix of the previous word
            for i in range(len(PrevWord), PrefixLenPlus1, -1):
                self.set_transition(TempStates[i-1], PrevWord[i], findMinimazed(TempStates[i]))
            for i in range(PrefixLenPlus1, len(CurrWord)):
                self.clear_state(TempStates[i])
                self.set_transition(TempStates[i-1], CurrWord[i], TempStates[i])

            if CurrWord != PrevWord:
                self.set_final(TempStates[len(CurrWord)], True)
                self.set_output(TempStates[len(CurrWord)], '')

            for j in range(1, PrefixLenPlus1-1):
                CommonPrefix = PrevWord[:j]
                WordSufix = PrevWord[j:]
                self.set_output(TempStates[j-1], CurrWord[j], CommonPrefix)

                for c in range(self.first_char, self.last_char+1):
                    if c != CurrWord[j]:
                        self.set_output(TempStates[j-1], c, CommonPrefix + c + WordSufix)






