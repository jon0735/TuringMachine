

class State:
    def __init__(self, transitionsTuples, isHaltingState=False):
        self.isHalting = isHaltingState

        pass


class Tape:
    def __init__(self, initSize=10):
        self.head = 0
        # sizes = initSize // 3
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

    def shift(self, direction):
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
        self.alphabet = []  # Should be a set?
        self.tapes = []  # tape 0 is input tape, and last is output tape
        self.currentState = 0

    def use_alphabet(self, alph):
        if not self.alphabet:
            print("Warning: Overwriting existing alphabet. If states have been created this will probably break things")
        self.alphabet = set(alph)

    def add_state(self, state):
        if not self.alphabet:
            print("Error: Define alphabet before adding states")
            return
        pass


    def step(self):
        tapeSymbols = [tape.read() for tape in self.tapes]
        state = self.states[self.currentState]
        for symbol in tapeSymbols:
            state = state[symbol]
        

        # TODO
        pass

