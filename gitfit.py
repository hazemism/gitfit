import os,hashlib,zlib,enum,struct,collections

class object (enum.Enum):
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

def init () :
    os.mkdir(os.path.join('.git'))
    for file in ['objects','refs','refs/heads']:
           os.mkdir(os.path.join('.git',file))
    write_file(os.path.join('.git','HEAD'),b'ref: refs/heads/master')

#Object storage layer
def hash_object (data, type_obj, write=True):
     size_obj = len(data)
     header = '{} {}'.format(type_obj,size_obj).encode()
     full_data = header + b'\x00' + data
     sha1 = hashlib.sha1(full_data).hexdigest()
     if write :
        path = os.path.join('.git', 'objects',sha1[:2],sha1[2:])
        if not os.path.exists(path):
             os.makedirs(os.path.dirname(path),exist_ok=True)
             write_file(path, zlib.compress(full_data))
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
    if not objects:
        raise ValueError ("object not found")
    if len(objects)>=2:
        raise ValueError ('multiple objects ({}) with {}'.format(len(objects),sha1_prefix))
    return os.path.join(obj_dir,objects[0])

def read_object(sha1):
    path = find_object(sha1)
    if not path:
        raise ValueError('error')
    full_data = zlib.decompress(read_file(path))
    null = full_data.index(b'\x00') 
    header = full_data[:null] 
    type_obj,size_obj = header.decode().split()
    data = full_data[null+1:]
    if (size_obj == len(data)):
        print('execute size {}, got {}'.format(size_obj,len(data)))
        return
    return type_obj,data

IndexEntry = collections.namedtuple('IndexEntry', [
    'ctime_s', 'ctime_n', 'mtime_s', 'mtime_n', 'dev', 'ino', 'mode',
    'uid', 'gid', 'size', 'sha1', 'flags', 'path',
])

def read_index ():
    try:
       path = os.path.join('git','index')
       data = read_file(path)
    except FileNotFoundError:
        return []
    checksum_data = data [:-20]
    checksum      = data [-20:]
    digest = hashlib.sha1(checksum_data).digest()
    assert digest == checksum
    signature, version, num_entries = struct.unpack('!4s2L', checksum_data[:12])
    assert signature == b'DIRC'
    assert version == 2

    entry_data = checksum_data [12:]
    entries = []
    pos = 0

    while pos + 62 < (len(entry_data)):
          fields_end = pos + 62
          fields = struct.unpack('!10L20s1H',entry_data[pos:fields_end])
          null_pos = entry_data.index(b'\x00',fields_end)
          path = entry_data[fields_end:null_pos]
          entry = IndexEntry(*(fields + (path.decode(),)))
          entries.append(entry)
          entry_len = ((62 + len(path) + 1 + 7)//8) * 8
          pos += entry_len
    assert len(entries) == num_entries
    return entries