import os
import hashlib 
import zlib

def write_file (path,data):
    with open (path,'wb') as wf:
        wf.write(data)


def init (repo) :
    os.mkdir(repo)
    os.mkdir(os.path.join(repo,'.git'))
    for file in ['objects','refs','refs/heads']:
           os.mkdir(os.path.join(repo,'.git',file))

    write_file(os.path.join(repo,'.git','HEAD'),b'ref: refs/heads/master')

    print ("initialized empty repo {}".format(repo))


def hash_object (data, type, write=True):
     size = len(data)
     header = '{} {}'.format(type,size).encode()
     full_data = header + b'\x00' + data
     sha1 = hashlib.sha1(full_data).hexdigest()

     if write :
        path = os.path.join('.git', 'objects',sha1[:2],sha1[2:])
        if not os.path.exists(path):
             os.makedirs(os.path.dirname(path),exist_ok=True)
             write_file = (path, zlib.compress(full_data))

     return sha1