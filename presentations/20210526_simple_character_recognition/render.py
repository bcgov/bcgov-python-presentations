''' render some text in latex, converting the typeset result to "raw binary" format..
..which can be read without a driver'''

import os

def run(c): # run something at terminal and wait to finish
    print(c)
    a = os.system(c)

def render(my_text, name):
    run('mkdir -p ' + name)

    # use "Computer Modern" font by Donald Knuth # insert Knuth quotes..
    open(name + '.tex', 'wb').write(('\n'.join(['\\documentclass{letter}',
                                                '\\usepackage{lmodern}',
                                                '\\usepackage[T1]{fontenc}',
                                                '\\usepackage{xcolor}',
                                                '\\usepackage[tracking=true, letterspace = 100]{microtype}',
                                                '\\DisableLigatures{encoding = *, family = *}',
                                                '\\begin{document}',
                                                '\\color{blue}'] +
                                                ['\\textls{'] + my_text + ['}\n\\end{document}'])).encode())

    if not os.path.exists(name + '.bin'): # delete train.bin to start from new data
        run('pdflatex ' + name + '.tex') # render with LaTeX
        run('convert -background white -density 333 ' + name + '.pdf ' + name + '.bmp') # convert to bitmap
        run('gdal_translate -of ENVI -ot Float32 ' + name + '.bmp ' + name + '.bin') # convert to raw binary
        
        if os.path.exists(name + '.hdr'):
            # add band names
            d = open(name + '.hdr').read() + 'band names = {red,\ngreen,\nblue}'
            open(name + '.hdr','wb').write(d.encode())
