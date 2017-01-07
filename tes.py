#!/usr/bin/python3

import re
import os
import sys
import math
import cmath

varLetters = set(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
mathOperations = ["factorial", "copysign", "isfinite", "isclose", "degrees", "radians", "lgamma", "floor", "frexp", "isinf", "isnan", "ldexp", "trunc", "expm1", "log1p", "log10", "atan2", "hypot", "acosh", "asinh", "atanh", "gamma", "cmath", "phase", "polar", "ceil", "fabs", "fmod", "fsum", "modf", "log2", "sqrt", "acos", "asin", "atan", "cosh", "sinh", "tanh", "erfc", "fabs", "rect", "infj", "nanj", "gcd", "exp", "log", "pow", "cos", "sin", "tan", "erf", "tau", "inf", "nan", "pi", "e"]
rows, columns = os.popen('stty size', 'r').read().split()
rows = int(rows)
columns = int(columns)

def substitute(equation, variables):
    for variable in variables:
        equation = equation.replace(variable[0], str(variable[1]))
        # Restore math and cmath operations
        for operation in mathOperations:
            equation = equation.replace(operation.replace(variable[0], str(variable[1])), operation)
    try:
        eval(equation)
        return equation
    except ValueError:
        return equation.replace("math.", "cmath.")


def prettyPrint(info):
    # Total amount specified in the information text
    lines = 0
    for paragraph in info:
        for line in paragraph:
            if len(line) == 0:
                lines += 1
            else:
                lines += math.ceil(len(line) / int(columns))
    remainder = int(rows) - lines
    padding = remainder // (2 + (len(info) - 1) + 2) # 2 initial, 1 in between paragraphs, 2 afterwards
    for i in range(2*padding): print()
    for paragraph in info:
        for line in paragraph:
            spaces = (int(columns) - len(line))//2
            print(" "*spaces + line)
        for i in range(padding): print()
    for i in range(2*padding): print()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        info = [
        [
        "######################",
        "#     Calculator     #",
        "# by Anton Bäckström #",
        "######################"
        ],[
        "-------------------- Usage --------------------",
        "",
        "The program evaluates equations entered as terminal arguments.",
        "Different statements are separated by spaces, i.e. 'python3 " + sys.argv[0] + " A=1 B=2 A+B'",
        "If the an equation contains parantheses, the entire equation must be encapsulated in quotation-marks.",
        "This could for example look like this: 'python3 " + sys.argv[0] + " A=42 B=1336 \"A*(B+1)\"'"
        ],[
        "------------------ Variables ------------------",
        "",
        "Variables are one or more capital letters from A-Z.",
        "Assignment of variables is done using an equal sign like this: 'python3 " + sys.argv[0] + " FOO=1'.",
        "",
        "Variables must be assigned before they are referenced.",
        "Meaning, this would not work: 'python3 " + sys.argv[0] + " A=B B=1 2*A'",
        "While this would: 'python3 " + sys.argv[0] + " B=1 A=B 2*A'",
        "",
        "Variables will be substituted for their values and not their references.",
        "This means that 'python3 " + sys.argv[0] + " A=1 B=A A=2 B' would yield 1 and not 2",
        "as A contains the value 1 when B gets assigned its value.",
        "",
        "Variables are directly translated to their values, so AB would be the concatination of A and B rather than the multiplication.",
        "This means that 'python3 " + sys.argv[0] + " A=4 B=2 AB' would yield 42 instead of 8."
        ]]
        prettyPrint(info)
    else:
        variables = [] # List of tuples instead of dictionary so that you can i.e. use variables 'a' and 'aa' simultanously
        for arg in sys.argv[1:]:
            # Store original equation for printing
            original = arg
            # Allow the user to use i instead of j for imaginary/complex numbers
            while True:
                index = -1
                if re.search("[^a-z]i[^a-z]", arg) != None:
                    index = re.search("[^a-z]i[^a-z]", arg).start()
                elif re.search("^i[^a-z]", arg) != None:
                    index = re.search("^i[^a-z]", arg).start()
                    arg = "1j" + arg[1:]
                    continue
                elif re.search("[^a-z]i$", arg) != None:
                    index = re.search("[^a-z]i$", arg).start()
                else:
                    break
                if ord(arg[index]) >= 48 and ord(arg[index]) <= 57:
                    arg = arg[:index+1] + "j" + arg[index+2:]
                else:
                    arg = arg[:index+1] + "1j" + arg[index+2:]
            # Allows the user to use some basic percentage operations
            while arg.find("%") != -1:
                end = arg.find("%")
                start = end
                for i in range(end, 0, -1):
                    if arg[i] == "+" or arg[i] == "-" or arg[i] == "*" or arg[i] == "/":
                        start = i
                        break
                s = "(" + arg[start:end+1]
                s = s.replace("-", "1-")
                s = s.replace("+", "1+")
                s = s.replace("*", "")
                s = s.replace("/", "")
                arg = arg[:start] + "*" + s.replace("%", "/100)") + arg[end+1:]
            # Allow or remove special words/operations
            arg = arg.replace("math.","")
            arg = arg.replace("cmath.","")
            arg = arg.replace("^","**")
            for operation in mathOperations:
                arg = arg.replace(operation, "math." + operation)
            if arg.find("=") != -1: # Assignment of variables
                var = arg[:arg.find("=")]
                for c in var:
                    if not c in varLetters:
                        raise Exception("Illegal variable-name detected:" + var)
                value = eval(substitute(arg[arg.find("=")+1:], variables))
                variables += [(var, value)]
                variables.sort(key = lambda x: len(x[0]), reverse = True)
            else: # Print results
                value = eval(substitute(arg, variables))
                real = round(value.real,10)
                if real == int(real):
                    real = int(real)
                imag = round(value.imag,10)
                if imag == int(imag):
                    imag = int(imag)
                output = ""
                if real != 0:
                    output += str(real)
                if imag != 0:
                    if imag > 0 and output != "":
                        output += "+"
                    output += str(imag) + "i"
                if output == "":
                    output = "0"
                print(original + " = " + output)
