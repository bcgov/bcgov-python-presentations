'''cleanup intermediary files '''
import os

def run(c): # run something at terminal and wait to finish
    print(c)
    a = os.system(c)

run('rm *.png')  # remove figures
run('rm test* truth*')  # wipe test and truth data
run('rm -rf test truth')  # wipe test and truth data segment files
