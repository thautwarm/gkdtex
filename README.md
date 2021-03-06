# GKD TeX 

TeX that σ`∀´)!

`python setup.py install` and you can have the `gkdtex` command.

The syntax is compatible to TeX. Before executing a TeX engine, a part of TeX commands understandable to `gkdtex` are preprocessed, generating TeX code. 

The usage is:

`gkdtex main.tex [--config_dir <str>] [--out_file <str>=main.out.tex]`.

In GKD-TeX, there are 3 kinds of commands.

The first is a Python function provided by a Python file(usually in your `$config_dir/.gkdrc.py` or other gkd packages), you can check examples at Python module `gkdtex.builtins.*`.

The other 2, CBV(Call By Value) Commands and 2. CBN(Call By Name) Commands, are similar, can be defined via `\gkd@def` or `\gkd@def@lazy`.

Commands without any arguments shall be a constant string.

## Gkd Packages

Some Gkd packages providing productive tools can be installed via `pip`.

- [gkdbnf](https://github.com/thautwarm/gkdbnf): painless BNF writing; no dependencies.
- [gkdhighlight](https://github.com/thautwarm/gkdhighlight): syntax highlighting for vast programming languages; extensible; no dependencies other than `xcolor` and `amsmath`.
- [gkdtikz.tree](https://github.com/thautwarm/gkdtikz): simple TikZ trees with Yaml syntax.

P.S: For a package `$a.$b.$c`, use `pip install $a`.

## Python Commands

A minimal gkd package can be written in `$config_dir/mininalplugin.py`:

```python
from gkdtex.interpreter import Interpreter
from gkdtex.developer_utilities import *

def arginfo(*args: Group, tex_print, **kwargs):
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
        self.globals['arginfo'] = arginfo
``` 


```tex
\gkd@usepackage{mininalplugin}
\arginfo{1}{2}{3}{^a 1} % '3 positional arguments, keyword arguments: { a,self }'
```

## `\gkd@verb`(requires `fancyvrb`)

```tex
\gkd@verb{ {1, 2, 3}  a} % \verb& {1, 2, 3}  a&
```

## `\gkd@usepackage`

A GKD package is made from a Python module.
`\gkd@usepackage{module_name}` will do `import("module_name")`.

The module search path is Python `sys.path`, with `$config_dir` appended.

In that module you should provide a namespace `GkdInterface`, `GkdInterface` should have 1 or 2 elements,
`GkdInterface.load` and `GkdInterface.dispose`(optional).

Check `runtest/plugin_A.py` for how to implement `load` or `dispose`.

## `\gkd@input`

`\gkd@input{some_file}` literally inputs source code in `some_file`.

Note that `some_file` is the relative path. The base is the directory of the proceeding document.  


## CBV Commands


`\gkd@def` defines your own Call By Value command. You can define a Call By Name command by using `\gkd@def@lazy`.

- Positional arguments

    ```tex
     \gkd@def{\a{}}{#\1 + #\1}
     \a{1} % '1 + 1'
    ```
 
- Keyword arguments

    ```tex
    \gkd@def{\a{^a}{^b}}{#\a^#\b}
    \a{^b x}{^a y} % 'y + x' 
    ```
  
- Optional arguments

    ```tex
    \gkd@def{\a{1}{^b k_a}}{ #\1 + #\b }
    \a % '1 + k_a'
    ```
## `\gkd@pyexec` and `\gkd@pyeval`

```tex

\gkd@pyeval{1 + 1} % 2
\gkd@def{\add{}{}}{#\1 + #\2}

\gkd@pyexec{
    x = r"\add{1}"
}

\gkd@pyeval{^expand after=True}{x + "{1}"} % 1 + 1
```

P.S: You can use Python variable `tex_print(string)` to put `string` in the generated tex file,
     and you can use `self` to access the interpreter in case you need to inspect information such as frames(`self.frames`), current filename(`self.filename`), current source code(`self.src`), etc.

