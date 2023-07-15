from typing import List
import vim
from latex2sympy2 import latex2latex



class SympyRunner:
    def __init__(self):
        self._vim = vim
    
    def _get_selection(self, buf) -> List[str]:
        (lnum1, col1) = buf.mark('<')
        (lnum2, col2) = buf.mark('>')
        lines = self._vim.eval('getline({}, {})'.format(lnum1, lnum2))
        lines[0] = lines[0][col1:]
        lines[-1] = lines[-1][:col2]
        return lines


    def compile(self) -> None:
        try:
            buf = self._vim.current.buffer
            latex_equation = "\n".join(self._get_selection(buf))

            equation = latex2latex(latex_equation)
            vim.command(f':normal A \n{equation}') 
        except:
            print("Can't evaluate current selection")

    def is_filetype_supported(self) -> bool:
        return self._vim.eval("&filetype") in ['tex', 'latex']
