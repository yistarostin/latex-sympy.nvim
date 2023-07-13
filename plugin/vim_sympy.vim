if !has('python3')
    echomsg ':python3 is not available, vim-find-test will not be loaded.'
    finish
endif

python3 import vim_find_test.sympyRunner
python3 sr = vim_find_test.sympyRunner.SympyRunner()

command! FindTest python3 sr.compile()
