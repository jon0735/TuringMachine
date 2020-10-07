

class State:
    def __init__(self, transitionsTuples=None, isHaltingState=False):
        #  TransitionTuples: list of ( (toState(int), fromSymbols(list of chars), newSymbols(list of chars)), shifting(list of 1/0/-1) )
        self.isHalting = isHaltingState
        self.transitionFunction = dict() # Map for transition information. 
        if transitionsTuples is not None:
            for tup in transitionsTuples:
                addTransition(tup[1], (tup[0], tup[2])) 


    def addTransition(self, symbols, toState, toSymbols, shifting):
        transInfo = self.transitionFunction
        for s in symbols[:-1]:  # go down all symbols except the last
            if s not in transInfo:
                transInfo[s] = dict()
            transInfo = transInfo[s]
        lastS = symbols[-1]
        if lastS == transInfo:
            print("Warning: Replacing transiton tuple")
        transInfo[lastS] = (toState, toSymbols, shifting)
            

    def getTransitionInformation(self, tapeSymbols):
        transInfo = self.transitionFunction
        for s in tapeSymbols:
            if s not in transInfo:
                # No transition for this configuration. Machine should halt
                return None
            transInfo = transInfo[s]
        return transInfo  # should be (state, writesymbols, shifting)


class Tape:
    def __init__(self, initSize=10):
        self.head = 0
        # sizes = initSize // 3
        # Initialising left (negative) side of tape to be less than right (positive). Is this justified?
        self.leftSize = initSize // 3
        self.rightSize = initSize - self.leftSize
        self.leftTape = [' '] * self.leftSize
        self.rightTape = [' '] * self.rightSize

    def __getitem__(self, key):  # override indexing in a get situation (var = tape[x])
        if key < 0:
            return self.leftTape[abs(key)-1]
        else:
            return self.rightTape[key]

    def __setitem__(self, key, val):  # override indexing in a set situation (tape[x] = var)
        if key < 0:
            self.leftTape[abs(key)-1] = val
        else:
            self.rightTape[abs(key)] = val

    def __str__(self):  #  String of tape shows a visual representation of the tape with header
        leftIndexString = str(-self.leftSize) + ' ' 
        rightIndexString = ' ' + str(self.rightSize - 1)
        tapeString = leftIndexString + str(self.leftTape[::-1] + self.rightTape) + rightIndexString
        headPrint = (" " * ((self.leftSize + self.head)*5 + 2 + len(leftIndexString)))
        return tapeString + "\n" + headPrint + "^"

    def read(self):
        return self[self.head]

    def write(self, char):
        if len(char) != 1:
            raise Exception("Can only write char (or strings of length 1). Given: " + char)
        self[self.head] = char

    def shift(self, direction):  # assumes sequential tapes
        if direction == 0:
            return
        elif direction == 1:
            self.head += 1
            if self.head >= self.rightSize:
                self.rightTape = self.rightTape + ([' '] * self.rightSize)
                self.rightSize = self.rightSize * 2
        elif direction == -1:
            self.head -= 1
            if abs(self.head) > self.leftSize:
                self.leftTape = self.leftTape + ([' '] * self.leftSize)
                self.leftSize = self.leftSize * 2
        else:
            raise Exception("Can only shift 1, -1 or 0, not " + str(direction))
    

class TuringMachine:
    def __init__(self, numOfTapes=1):
        self.numOfTapes = numOfTapes
        self.states = []
        self.alphabet = set()  # Should be a set?
        self.tapes = [Tape() for _ in range(numOfTapes)]  # tape 0 is input tape, and last is output tape
        self.currentState = 0

    def useAlphabet(self, alph):
        if len(self.alphabet) != 0:
            print("Warning: Overwriting existing alphabet. If states have been created this will probably break things")
        self.alphabet = set(alph)


    def setNumOfStates(self, numStates, haltingStates=None):
        if haltingStates is None:
            haltingStates = []
        self.states = [State(isHaltingState=(i in haltingStates)) for i in range(numStates)]


    def addTransisiton(self, fromState, toState, fromSymbols, toSymbols, shifting):
        for s in fromSymbols + toSymbols:
            if s not in self.alphabet and s != " ":
                print("Transitions contains symbol " + s + " not in alphabet")
                return

        state = self.states[fromState]
        state.addTransition(fromSymbols, toState, toSymbols, shifting)


    def addTransisitons(self, transitionList):
        for trans in transitionList:
            self.addTransisiton(trans[0], trans[1], trans[2], trans[3], trans[4])
            

    def setInput(self, input):
        for i, c in enumerate(input):
            self.tapes[0][i] = c

    def step(self, printTape=False):
        tapeSymbols = [tape.read() for tape in self.tapes]
        state = self.states[self.currentState]

        transitionInformation = state.getTransitionInformation(tapeSymbols)
        if transitionInformation is None: # No transistion information from this configurations -> machine halts
            return False

        toState, writeSymbols, shifting = transitionInformation
        for i in range(len(self.tapes)):
            self.tapes[i].write(writeSymbols[i])

        for i in range(len(self.tapes)):
            self.tapes[i].shift(shifting[i])

        # TODO: call function for getting the transition information based on the state and current tape symbols
        # TODO: Use transition information to update tapes
        # for symbol in tapeSymbols:
        #     state = state[symbol]


## TODO NEXT: Lav simpel turing machine of test

## TODO (future work): Handle input only tape