'''cleanup intermediary files '''
import os

def run(c): # run something at terminal and wait to finish
    print(c)
    a = os.system(c)

run('rm *.png')
run('rm test* truth*')
run('rm -rf test truth')

