# GKD TeX 

TeX that σ`∀´)!

`python setup.py install` and you can have the `gkdtex` command.

The syntax is compatible to TeX, and we execute a part of commands and generating TeX code.

In GKD-TeX, there are 3 kinds of executable commands.
The first of which is provided by Python script(in your `$PWD/.gkdrc.py`), you can check
examples at Python module `gkdtex.builtins.*`.

The other 2 executable commands are 1. CBV(Call By Value) Commands; 2. CBN(Call By Name) Commands.  

A CBN Command does not expand its arguments.

Commands without any arguments shall be a constant string.

```
gkdtex main.tex [--config_path <str>] [--out_file <str>=main.out.tex]
```

## CBV Commands

`\define` : Define your own Call By Value command. 

- Positional arguments

    ```tex
     \define{\a{}}{#\1 + #\1}
     \a{1} % '1 + 1'
    ```
 
- Keyword arguments

    ```tex
    \define{\a{^a}{^b}}{#\a^#\b}
    \a{^b x}{^a y} % 'y + x' 
    ```
  
- Optional arguments

    ```tex
    \define{\a{1}{^b k_a}}{ #\1 + #\b }
    \a % '1 + k_a'
    ```
## `\pyexec` and `pyeval`

```tex

\pyeval{ }{1 + 1} % 2
\define{\add{}{}}{#\1 + #\2}

\pyexec{expandbefore=False}{
    x = r"\add{1}"
}

\pyeval{expandbefore=False, expandafter=True}{x + "{1}"} % 1 + 1
```

## `\verb`(requires `fancyvrb`)

```tex
\verb{ {1, 2, 3}  a} % \verb& {1, 2, 3}  a&
```