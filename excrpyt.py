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
    return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)


def unpad(s):
    return s[:-ord(s[len(s)-1:])]


def AES_encrypt(raw, key):
    raw = pad(16, raw)
    key = pad(16, key)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(raw)


def AES_decrypt(ciphertext, key):
    key = pad(16, key)
    iv = ciphertext[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext[16:]))


def AES_dir_encrypt(source_path, key):
    create_tar(source_path, source_path + ".tar")

    with open(source_path + ".tar", 'r') as tar:
        raw = tar.read()

    with open(source_path + ".aes", 'wb') as aes:
        aes.write(AES_encrypt(raw, key))

    # Delete .tar?


def AES_dir_decrypt(source_path, key):
    with open(source_path + ".aes", 'rb') as aes:
        tar_file = AES_decrypt(aes.read(), key)

    with open(source_path + ".tar", 'wb') as tar:
        tar.write(tar_file)

    extract_tar(source_path + ".tar", '.')


if __name__ == "__main__":
    #AES_dir_encrypt("example", "hi")
    AES_dir_decrypt("example", "hi")
