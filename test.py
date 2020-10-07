import turingmachine as tm
import sys
import time

# def delLines():
#     sys.stdout.write("\033[K")
#     sys.stdout.write("\033[F")
#     sys.stdout.write("\033[K")

# tape = tm.Tape()

# sys.stdout.write(str(tape))

# tape.shift(-1)
# tape.write("M")
# tape.shift(-1)
# tape.shift(-1)

# time.sleep(1)

# sys.stdout.write("\033[K")
# sys.stdout.write("\033[F")
# sys.stdout.write("\033[K")
# # sys.stdout.write("STUFF")

# time.sleep(1)


# sys.stdout.write(str(tape))
# time.sleep(1)

# # tape.shift(1)
# tape.shift(1)

# print(tape.read())

# sys.stdout.write("ABCD")
# sys.stdout.write("\b\b")
# sys.stdout.write("ABCD\n")


# stuff = (("acd", 23), 2, 3)
# print(stuff)


turingMachine = tm.TuringMachine()

turingMachine.useAlphabet(['1', '0', 'X'])


