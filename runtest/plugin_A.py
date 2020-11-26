from gkdtex.interpreter import Interpreter

def narg(self: Interpreter, __, tex_print):
    tex_print(str(len(self.frames[0][2])))

class GkdInterface:
    @staticmethod
    def load(self: Interpreter, text_print):
        if 'narg' in self.globals:
            raise NameError("'narg' has already been defined.")
        self.globals['narg'] = narg
