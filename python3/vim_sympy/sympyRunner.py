import sympy
from sympy.parsing.latex import parse_latex
import time
import pytest
import os
try:
    import pynvim as neovim
except ImportError:
    import neovim
import vim



#VIMRC = 'test/data/test.vimrc'
SLEEP = 0.1


@pytest.fixture(scope='session')
def plugin_dir(tmpdir_factory):
    return tmpdir_factory.mktemp('test_plugin')


@pytest.fixture(scope='module', autouse=True)
def register_plugin(plugin_dir):
    os.environ['NVIM_RPLUGIN_MANIFEST'] = str(plugin_dir.join('rplugin.vim'))
    #child_argv = ['nvim', '-u', VIMRC, '--embed', '--headless']
    child_argv = ['nvim', '--embed', '--headless']
    vim = neovim.attach('child', argv=child_argv)
    vim.command('UpdateRemotePlugins')
    vim.quit()
    yield


def wait_for(func, cond=None, sleep=.001, tries=1000):
    for _ in range(tries):
        res = func()
        if cond is None:
            if res:
                return
        else:
            if cond(res):
                return res
        time.sleep(sleep)
    raise TimeoutError()
# @neovim.plugin
class SympyRunner:
    def __init__(self):
        self._vim = vim
    
    def _get_selection(self, buf):
        (lnum1, col1) = buf.mark('<')
        (lnum2, col2) = buf.mark('>')
        lines = self._vim.eval('getline({}, {})'.format(lnum1, lnum2))
        lines[0] = lines[0][col1:]
        lines[-1] = lines[-1][:col2]
        return lines


    def compile(self) -> None:
        buf = self._vim.current.buffer
        latex_equation = self._get_selection(buf)
        equation = parse_latex(latex_equation)
        print(f"{latex_equation}:\t\t{equation}\n")

    def is_filetype_supported(self) -> bool:
        return self._vim.eval("&filetype") in ['tex', 'latex']
