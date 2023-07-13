if !has('python3')
    echomsg ':python3 is not available, vim-find-test will not be loaded.'
    finish
endif

python3 import vim_sympy.sympyRunner
python3 sr = vim_sympy.sympyRunner.SympyRunner()

command! LatexSympy python3 sr.compile()
