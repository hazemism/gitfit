import os

def write_file (path,data):
    with open (path,'wb') as wf:
        wf.write(data)


def init (repo) :
    os.mkdir(repo)
    os.mkdir(os.path.join(repo,'.git'))
    os.mkdir(os.path.join(repo,'.git','objects'))
    os.mkdir(os.path.join(repo,'.git','refs'))
    os.mkdir(os.path.join(repo,'.git','refs/heads'))

    write_file(os.path.join(repo,'.git','HEAD'),b'ref: refs/heads/master')

    print ("initialized empty repo {}".format(repo))
    

    



