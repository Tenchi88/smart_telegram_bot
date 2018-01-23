from os import environ

k = environ['GIT_LAB_KEY']
with open('.rsa/git_lab', 'w') as f:
    f.write(k)
