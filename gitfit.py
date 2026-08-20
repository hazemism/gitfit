import os,hashlib,zlib,enum

class object (enum.ob):
    commit = 1
    tree = 2
    blob = 3

#low level functions
def write_file (path,data):
    with open (path,'wb') as wf:
        wf.write(data)
    
def read_file (path):
     with open (path,'rb') as rf:
      return rf.read()         

def init (repo) :
    os.mkdir(repo)
    os.mkdir(os.path.join(repo,'.git'))
    for file in ['objects','refs','refs/heads']:
           os.mkdir(os.path.join(repo,'.git',file))

    write_file(os.path.join(repo,'.git','HEAD'),b'ref: refs/heads/master')

    print ("initialized empty repo {}".format(repo))

#Object storage layer
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

def find_object(sha1_prefix):
    if len(sha1_prefix) < 2:
        raise ValueError("error")
    obj_dir = os.path.join('.git', 'objects', sha1_prefix[:2])
    rest = sha1_prefix[2:]
    filename = os.listdir(obj_dir)
    objects = []
    for file in filename:
        if file.startswith(rest):
            objects.append(file)
    if not object:
        raise ValueError ("object not fount")
    if len(object)>=2:
        raise ValueError ('multiple objects ({}) with {}'.format(len(object),sha1_prefix))
    return os.path.join(obj_dir,object[0])

def read_object(sha1):
    path = find_object(sha1)
    if not path:
        raise ValueError('error')
    full_data = zlib.decompress(read_file(path))
    null = full_data.index(b'\x00') 
    header = full_data[:null] 
    type_obj,size_obj = header.decode().split()
    data = full_data[null+1:]
    assert size_obj == len(data),'execute size {}, got {}'.format(size_obj,len(data))
    return type_obj,data