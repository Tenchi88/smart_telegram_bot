from os import environ

k = environ['GIT_LAB_KEY']
with open('.ssh/git_lab', 'w') as f:
    f.write(k)
