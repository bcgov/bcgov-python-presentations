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
                                                '\\usepackage[tracking=true, letterspace = 100]{microtype}',  # bigger spacing
                                                '\\DisableLigatures{encoding = *, family = *}',
                                                '\\pagenumbering{gobble}',  # no page numbering
                                                '\\begin{document}',
                                                '\\color{blue}'] +  # blue text
                                                ['\\textls{'] + my_text + ['}\n\\end{document}'])).encode())

    if not os.path.exists(name + '.bin'): # delete train.bin to start from new data
        run('pdflatex ' + name + '.tex') # render with LaTeX
        run('convert -background white -density 333 ' + name + '.pdf ' + name + '.bmp') # convert to bitmap
        run('gdal_translate -of ENVI -ot Float32 ' + name + '.bmp ' + name + '.bin') # convert to raw binary
        
        if os.path.exists(name + '.hdr'):
            d = open(name + '.hdr').read() + 'band names = {red,\ngreen,\nblue}'  # add band names
            open(name + '.hdr','wb').write(d.encode())

truth = [] # truth characters

if __name__ == "__main__":

    def chars(i, j):  # add chars between ascii codes i, j to truth data
        global truth
        my_chars = [chr(x) for x in range(i, j)]
        truth += my_chars
        print("my_chars", my_chars)
        return ' '.join(my_chars)

    if not os.path.exists('truth.bin'):
        render([chars(48, 58) + '\n', chars(65, 91) + '\n', chars(97, 123)],  # render 0-9, a-z, A-Z in LaTeX
               'truth')  # designate as truth

        print('+w truth_chars.txt')
        open('truth_chars.txt', 'wb').write((''.join(truth)).encode())  # record the character representations used

    if not os.path.exists('test.bin'):
        print("render test data..")
        render(["hello world"], 'test')
        '''
        render(["Through three cheese trees\\ \\\\",
                "three free fleas flew\\ \\\\",
                "While these fleas flew\\ \\\\",
                "freezy breeze blew\\ \\\\", 
                "Freezy breeze made\\ \\\\", 
                "these three trees freeze\\ \\\\",
                "Freezy trees made\\ \\\\",
                "these trees cheese freeze\\ \\\\",
                "Thats what made these\\ \\\\",
                "three free fleas sneeze\\ \\\\"],
                'test')'''
