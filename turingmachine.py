import sys
import time

class State:
    def __init__(self, transitionsTuples=None, isHaltingState=False, isAcceptingState=False):
        #  TransitionTuples: list of ( (toState(int), fromSymbols(list of chars), newSymbols(list of chars)), shifting(list of 1/0/-1) )
        self.isHalting = isHaltingState
        self.isAccepting = isAcceptingState
        self.transitionFunction = dict() # Map for transition information. 
        if transitionsTuples is not None:
            raise Exception("Creating state with transitions not yet implemented")
            # for tup in transitionsTuples:
            #     self.addTransition(tup[1], (tup[0], tup[2])) 


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

    def toString(self):
        leftString = ""
        emptyPart = True
        for c in reversed(self.leftTape):
            if c == ' ' and emptyPart:
                continue
            else:
                if emptyPart:
                    emptyPart = False
                leftString += c
        emptyPart = True  
        rightString = ""     
        for c in reversed(self.rightTape):
            if c == ' ' and emptyPart:
                continue
            else:
                if emptyPart:
                    emptyPart = False
                rightString += c
        return leftString + rightString[::-1]

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
        self.hasHalted = False

    def useAlphabet(self, alph):
        if len(self.alphabet) != 0:
            print("Warning: Overwriting existing alphabet. If states have been created this will probably break things")
        self.alphabet = set(alph)

    def setNumOfStates(self, numStates, haltingStates=None, acceptingStates=None):
        if haltingStates is None: # Should be something otherwise the machine will run forever
            # TODO: Print warning
            haltingStates = []
        if acceptingStates is None: # Should be something otherwise the Language of the machine is empty 
            # TODO: Print warning
            acceptingStates = []
        self.states = [State(isHaltingState=(i in haltingStates), isAcceptingState=(i in acceptingStates)) for i in range(numStates)]

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

    def step(self, printTapes=False, printDelay=.5):
        if self.hasHalted:
            print("Machine has already halted")
            return

        tapeSymbols = [tape.read() for tape in self.tapes]
        state = self.states[self.currentState]

        transitionInformation = state.getTransitionInformation(tapeSymbols)
        if transitionInformation is None: # No transistion information from this configurations -> machine halts
            self.hasHalted = True
            if printTapes:
                self.eraseAndPrintTapes()
                # time.sleep(printDelay)
            return

        toState, writeSymbols, shifting = transitionInformation
        for i in range(len(self.tapes)):
            self.tapes[i].write(writeSymbols[i])

        if printTapes:
            self.eraseAndPrintTapes()
            time.sleep(printDelay)

        for i in range(len(self.tapes)):
            self.tapes[i].shift(shifting[i])

        if printTapes:
            self.eraseAndPrintTapes()
            time.sleep(printDelay)

        self.currentState = toState
        if self.states[self.currentState].isHalting:
            self.hasHalted = True

    def run(self, printTapes=False, printDelay=.5):
        if printTapes:
            sys.stdout.write("\n")
            self.printTapes()
        while not self.hasHalted:
            self.step(printTapes=printTapes, printDelay=printDelay)
        return self.states[self.currentState].isAccepting, self.tapes[-1].toString()

    def runOnInput(self, input, printTapes=False, printDelay=.5):
        self.setInput(input)
        return self.run(printTapes=printTapes, printDelay=printDelay)

    # Assumes a machine has already been printed
    def eraseAndPrintTapes(self):
        for _ in range(len(self.tapes)):
            sys.stdout.write("\033[1A")
            sys.stdout.write("\033[2K")
            sys.stdout.write("\033[1A")
            sys.stdout.write("\033[2K")
            sys.stdout.flush()
        self.printTapes()

    def printTapes(self):
        for tape in self.tapes:
            sys.stdout.write(str(tape))
            sys.stdout.write("\n")
        sys.stdout.flush()

## TODO (future work): Handle input only tape