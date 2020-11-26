import gkdtex.builtins
from gkdtex.interpreter import Interpreter

interpreter = Interpreter()

interpreter.initialize()
interpreter.run_file("a.tex")
interpreter.dispose()