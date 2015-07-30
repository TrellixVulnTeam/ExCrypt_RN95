# Main file
import tarfile, os
from Crypto.Cipher import AES
from Crypto import Random


def create_tar(source_path, output_path):
    with tarfile.open(output_path, 'w') as tar:
        tar.add(source_path, arcname=os.path.basename(source_path))


def extract_tar(source_path, output_path):
    with tarfile.open(source_path, 'r') as tar:
        tar.extractall(path=output_path)


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

    with open(source_path + ".tar", 'rb') as tar:
        raw = tar.read()

    with open(source_path + ".aes", 'wb') as aes:
        aes.write(AES_encrypt(raw, key))

    if remove_int:
        os.remove(source_path + ".tar")


def AES_dir_decrypt(source_path, key, remove_int=True):
    aes_path = source_path
    if ".aes" not in source_path:
        aes_path = source_path + ".aes"

        
    with open(aes_path, 'rb') as aes:
        tar_file = AES_decrypt(aes.read(), key)

    with open(source_path + ".tar", 'wb') as tar:
        tar.write(tar_file)

    extract_tar(source_path + ".tar", os.path.join(source_path, ".."))
    
    if remove_int:
        os.remove(source_path + ".tar")
        
        
if __name__ == "__main__":
    pass
