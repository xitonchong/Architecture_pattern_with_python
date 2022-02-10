import hashlib 
import os
import shutil 
from pathlib import Path 



def sync(source, dest):
    # imperative shell step 1, gather inputs 
    source_hashes = read_paths_and_hashes(source) 
    dest_hashes = read_paths_and_hashes(dest)

    # step 2: call functional core
    actions = determine_actions(source_hashes, dest_hashes, source, dest) 

    # imperative shell step 3, apply outputs 
    for action, *paths, in actions:
        if action == "COPY":
            shutil.copy(*paths)
        if action == "MOVE":
            shutil.move(*paths)
        if action == "DELETE":
            os.remove(paths[0])


BLOCKSIZE = 65536

def hash_file(path):
    hasher = hashlib.sha1() 
    with path.open("rb") as f:
        buf = f.read(BLOCKSIZE)
        while buf:
            hasher.update(buf)
            buf = f.read(BLOCKSIZE)
    return hasher.hexdigest() 




def read_paths_and_hashes(root):
    hashes = {}
    for folder, _, files in os.walk(root):
        for fn in files:
            hashes[hash_file(Path(folder) / fn)] = fn # Path(folder) / fn => dir/file format in string 
    return hashes 


def determine_actions(source_hashes, dest_hashes, source_folder, dest_folder):
    for sha, filename in source_hashes.items(): 
        if sha not in dest_hashes:
            ''' there is a new file in source folder ''' 
            sourcepath = Path(source_folder) / filename 
            destpath = Path(dest_folder) / filename 
            yield "COPY", sourcepath, destpath 
        
        elif dest_hashes[sha] != filename: 
            '''  the file has changed name in source folder  '''
            newdestpath = Path(dest_folder) / filename 
            olddestpath = Path(dest_folder) / dest_hashes[sha] # dest filename 
            yield "MOVE", olddestpath, newdestpath

    ''' dest folder have files which source folder doesnt have: DELETE'''
    for sha, filename in dest_hashes.items():
        if sha not in source_hashes:
            deletepath = Path(dest_hashes) / filename 
            yield "DELETE", deletepath 
    # be careful to use yield instead of return, we do not want the function to exit before finding all 

