import subprocess

print( subprocess.call(['mocp', '-i', ['|'], ['grep', 'State']], shell=False) )
