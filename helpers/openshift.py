from os import environ, mkdir, path

ssh_path = '/root/.ssh/'
if not path.exists(ssh_path):
    mkdir(ssh_path)
k = environ['GIT_LAB_KEY']
with open(ssh_path + 'git_lab', 'w') as f:
    f.write(k)
