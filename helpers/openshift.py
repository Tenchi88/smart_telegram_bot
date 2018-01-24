from os import environ
import os

os.mkdir('/root/.ssh', 400)
k = environ['GIT_LAB_KEY']
with open('/root/.ssh/git_lab', 'w') as f:
    f.write(k)
