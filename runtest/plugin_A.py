from gkdtex.interpreter import Interpreter

def narg(*, self: Interpreter, tex_print):
    tex_print(str(len(self.frames[0][2])))

def arginfo(*args, tex_print, **kwargs):
    tex_print(
        "{} positional arguments, keyword arguments: {{ {} }}".format(
            len(args),
            ','.join(kwargs.keys())
        )
    )

class GkdInterface:
    @staticmethod
    def load(self: Interpreter, text_print):
        if 'narg' in self.globals:
            raise NameError("'narg' has already been defined.")
        self.globals['narg'] = narg
        self.globals['arginfo'] = arginfo