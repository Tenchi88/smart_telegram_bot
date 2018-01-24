from os import environ
import os

os.mkdir('~/.ssh', 400)
k = environ['GIT_LAB_KEY']
with open('~/.ssh/git_lab', 'w') as f:
    f.write(k)
