# Main file
import tarfile, os
from Crypto.Cipher import AES
from Crypto import Random


def create_tar(source_path, output_path):
    with tarfile.open(output_path, 'w|') as tar:
        tar.add(source_path, arcname=os.path.basename(source_path))


def extract_tar(source_path, output_path):
    try:
        with tarfile.open(source_path, 'r|') as tar:
            
            import os
            
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar, path=output_path)
    except:
        print("Tar read error. Wrong key?")


def pad(bs, s):
    assert(type(s) == bytes)
    end_pad = (bs - len(s) % bs) * chr(bs - len(s) % bs)
    return s + bytes(end_pad, encoding="utf-8")


def unpad(s):
    assert(type(s) == bytes)
    return s[:-ord(s[len(s)-1:])]


def AES_encrypt(raw, key):
    raw = pad(16, raw)
    key = pad(16, bytes(key, "utf-8"))  # Ensure bytes
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    return iv + cipher.encrypt(raw)


def AES_decrypt(ciphertext, key):
    key = pad(16, bytes(key, "utf-8"))
    iv = ciphertext[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    return unpad(cipher.decrypt(ciphertext[16:]))


def AES_dir_encrypt(source_path, key, remove_int=True):
    create_tar(source_path, source_path + ".tar")

    # Split files and write AES blocks
    ft = open(source_path + ".tar", 'rb')
    BLOCK_SIZE = 2048

    with open(source_path + ".ab", 'wb') as f:  # .ab = AES blocks
        while True:
            block = ft.read(BLOCK_SIZE)
            print(block)
            if not block:
                break

            f.write(AES_encrypt(block, key))
        
    ft.close()
    return
    if remove_int:
        os.remove(source_path + ".tar")


def AES_dir_decrypt(source_path, key, remove_int=True):
    if source_path[-3:] == ".ab":
        source_path = source_path[:-3]

    # Decrypt AES blocks and combine together
    fab = open(source_path + ".ab", 'rb')
    BLOCK_SIZE = 2048
        
    with open(source_path + ".tar", 'wb') as f:
        while True:
            block = fab.read(BLOCK_SIZE)
            #print(block)
            if not block:
                break

            f.write(AES_decrypt(block, key))

    fab.close()


    extract_tar(source_path + ".tar", os.path.join(source_path, ".."))
    return
    if remove_int:
        os.remove(source_path + ".tar")

        
if __name__ == "__main__":
    pass
